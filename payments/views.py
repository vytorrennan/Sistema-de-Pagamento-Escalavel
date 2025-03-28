from django.shortcuts import render
import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Product, Order, OrderItem
from .tasks import process_payment

stripe.api_key = settings.STRIPE_SECRET_KEY

def product_list(request):
    products = Product.objects.all()
    orders = Order.objects.filter(user=request.user) if request.user.is_authenticated else []
    return render(request, 'payments/product_list.html', {'products': products, 'orders': orders})

@login_required
def checkout(request):
    if request.method == 'POST':
        # Criar um novo pedido
        order = Order.objects.create(
            user=request.user,
            total_amount=0
        )
        
        total = 0
        # Processar os itens selecionados
        for product_id, quantity in request.POST.items():
            if product_id.startswith('product_'):
                try:
                    product_id = int(product_id.replace('product_', ''))
                    quantity = int(quantity)
                    if quantity > 0:
                        product = Product.objects.get(id=product_id)
                        price = product.price * quantity
                        total += price
                        OrderItem.objects.create(
                            order=order,
                            product=product,
                            quantity=quantity,
                            price=price
                        )
                except (ValueError, Product.DoesNotExist):
                    continue

        if total == 0:
            order.delete()
            return redirect('product_list')

        order.total_amount = total
        order.save()

        # Criar sessão de pagamento do Stripe
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'brl',
                        'unit_amount': int(total * 100),  # Stripe usa centavos
                        'product_data': {
                            'name': f'Pedido #{order.id}',
                        },
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=request.build_absolute_uri(f'/payment/success/{order.id}/'),
                cancel_url=request.build_absolute_uri('/payment/cancel/'),
            )
            return redirect(checkout_session.url)
        except Exception as e:
            order.status = 'failed'
            order.save()
            return JsonResponse({'error': str(e)})

    products = Product.objects.all()
    return render(request, 'payments/checkout.html', {'products': products})

@login_required
def payment_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.status == 'pending':
        order.status = 'processing'
        order.save()
        # Iniciar processamento assíncrono do pagamento
        process_payment.delay(order.id)
    return render(request, 'payments/success.html', {'order': order})

@login_required
def payment_cancel(request):
    return render(request, 'payments/cancel.html')

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
import stripe
from .models import Order

stripe.api_key = settings.STRIPE_SECRET_KEY

@shared_task
def process_payment(order_id):
    try:
        order = Order.objects.get(id=order_id)
        
        # Simular processamento assíncrono
        import time
        time.sleep(5)  # Simula um processamento que leva 5 segundos
        
        # Atualizar status do pedido
        order.status = 'completed'
        order.save()
        
        # Enviar e-mail de confirmação
        print(f"Preparing to send email to: {order.user.email}")
        send_mail(
            subject=f'Confirmação do Pedido #{order.id}',
            message=f'''
Olá {order.user.username},

Seu pagamento foi processado com sucesso!

Detalhes do pedido:
- Número do pedido: {order.id}
- Valor total: R$ {order.total_amount}
- Data: {order.created_at.strftime('%d/%m/%Y %H:%M')}

Obrigado por sua compra!

Atenciosamente,
Equipe E-commerce
''',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[order.user.email],
            fail_silently=False,
        )
        
        return True
    except Order.DoesNotExist:
        return False
    except Exception as e:
        # Em caso de erro, marcar o pedido como falho
        order.status = 'failed'
        order.save()
        raise e
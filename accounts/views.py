# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

# Custom form to make email mandatory
class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Obrigatório. Informe um email válido.")

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after signup
            return redirect('product_list')  # Redirect to product list after signup
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})
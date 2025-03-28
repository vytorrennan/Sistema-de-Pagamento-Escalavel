#!/usr/bin/env python
import environ
import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DisplayLab.settings")
django.setup()
env = environ.Env()
environ.Env.read_env()
from django.contrib.auth.models import User

if User.objects.filter(username="Admin").first() is None:
    User.objects.create_superuser(
        "Admin",
        "admin@admin.com",
        "admin",
    )
    print("Nenhum user com o username do arquivo .env foi encontrado, logo ele foi criado")

from payments.models import Product

import os
from django.conf import settings
from payments.models import Product
from django.core.files import File

# Verifica se já existem produtos no banco de dados
if not Product.objects.exists():
    products = [
        {
            'name': 'Smartphone Galaxy S21',
            'description': 'Smartphone Samsung Galaxy S21 com 128GB de armazenamento e 8GB de RAM.',
            'image': 'products/image-147812a827ce414cbeecb5bb91eecb25-1-.jpg',
            'price': 3999.99
        },
        {
            'name': 'Notebook Dell Inspiron',
            'description': 'Notebook Dell Inspiron com processador Intel Core i5, 8GB de RAM e SSD de 256GB.',
            'image': 'products/notebook_dell_inspiron_3501_core_i5_1135g7_memoria_8gb_ssd_256gb_geforce_mx350.png',
            'price': 4599.99
        },
        {
            'name': 'Smart TV LG 55"',
            'description': 'Smart TV LG 55" 4K com HDR e sistema webOS.',
            'image': 'products/DZ-3.jpg',
            'price': 2999.99
        },
        {
            'name': 'Fone de Ouvido Sony WH-1000XM4',
            'description': 'Fone de ouvido sem fio com cancelamento de ruído.',
            'image': 'products/61oqO1AMbdL._AC_UF10001000_QL80_.jpg',
            'price': 1499.99
        },
        {
            'name': 'Console PlayStation 5',
            'description': 'Console PlayStation 5 com controle DualSense.',
            'image': 'products/images.jpg',
            'price': 4499.99
        }
    ]

    for product_data in products:
        # Tenta obter o produto ou criá-lo se não existir
        product, created = Product.objects.get_or_create(
            name=product_data['name'],
            defaults={
                'description': product_data['description'],
                'price': product_data['price']
            }
        )

        # Se o produto foi criado, associa a imagem
        if created:
            image_path = os.path.join(settings.MEDIA_ROOT, product_data['image'])
            if os.path.exists(image_path):
                with open(image_path, 'rb') as image_file:
                    product.image.save(
                        os.path.basename(image_path),
                        File(image_file),
                        save=True
                    )
            else:
                print(f"Imagem não encontrada: {image_path}")
    
    print("Nenhum produto foi encontrado então produtos de teste foram criados")
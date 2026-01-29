import random
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from apps.catalog.models import Category, Product

class Command(BaseCommand):
    help = 'Seeds the database with initial Categories and Products'

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding data...")

        # 1. Define Categories
        categories_data = [
            {'name': 'Electronics', 'desc': 'Gadgets, devices, and tech accessories.'},
            {'name': 'Fashion', 'desc': 'Clothing, shoes, and jewelry.'},
            {'name': 'Home & Garden', 'desc': 'Furniture, decor, and tools.'},
            {'name': 'Books', 'desc': 'Fiction, non-fiction, and educational material.'},
        ]

        for cat in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat['name'],
                defaults={'description': cat['desc'], 'slug': slugify(cat['name'])}
            )
            
            # 2. Add 10-15 Products per Category for a rich Catalog
            for i in range(1, 13):
                product_name = f"{category.name} Item {i}"
                Product.objects.get_or_create(
                    name=product_name,
                    category=category,
                    defaults={
                        'slug': slugify(f"{product_name}-{category.id}"),
                        'description': f"High-quality {category.name} product number {i}.",
                        'price': round(random.uniform(10.0, 500.0), 2), # Professional Decimal use
                        'stock': random.randint(5, 100),
                        'is_active': True
                    }
                )

        self.stdout.write(self.style.SUCCESS('Successfully seeded 4 Categories and 48 Products!'))


python manage.py seed_data

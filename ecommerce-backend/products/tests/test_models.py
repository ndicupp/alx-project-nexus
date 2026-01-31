import pytest
from products.models import Product, Category

@pytest.mark.django_db
def test_product_creation():
    category = Category.objects.create(name="Electronics", slug="electronics")
    product = Product.objects.create(
        category=category,
        name="Laptop",
        price=1200,
        stock=10
    )
    assert product.name == "Laptop"
    assert product.category.slug == "electronics"


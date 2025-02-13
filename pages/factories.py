import factory
from .models import Product, Comment

class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Faker('name')
    price = factory.Faker('pydecimal', left_digits=5, right_digits=2, positive=True, min_value=1, max_value=10000)
    # Ensure these fields match the Product model
    # description = factory.Faker('text')  # Remove or comment out if not in model
    # Add other fields as necessary

class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    product = factory.SubFactory(ProductFactory)
    text = factory.Faker('text')

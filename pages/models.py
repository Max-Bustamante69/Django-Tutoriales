from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # Ensure these fields match the factory
    # description = models.TextField()  # Add if necessary
    # Add other fields as necessary
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    #stringify the model
    def __str__(self):
        return self.name + ' ' + str(self.price) + ' ' + str(self.created_at) + ' ' + str(self.updated_at)

class Comment(models.Model):
    product = models.ForeignKey(Product, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()

# Create your models here.

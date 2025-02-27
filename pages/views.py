from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from .models import Product
from django.shortcuts import get_object_or_404

class HomePageView(TemplateView):
    template_name = 'home.html'

class AboutPageView(TemplateView):
    template_name = 'about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "About us - Online Store",
            "subtitle": "About us",
            "description": "This is an about page ...",
            "author": "Developed by: Your Name",
        })

        return context

class ContactPageView(TemplateView):
    template_name = 'contact.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Contact Us - Online Store",
            "subtitle": "Contact Information",
            "email": "info@onlinestore.com",
            "address": "123 E-Commerce Street, Digital City, 54321",
            "phone": "+1 (555) 123-4567"
        })
        
        return context



class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price']


    
    def clean_price(self):
        price = self.cleaned_data['price']
        if price <= 0:
            raise ValidationError("Price must be greater than zero.")
        return price

class ProductIndexView(View):
    template_name = 'products/index.html'

    def get(self, request):
        viewData = {}
        viewData["title"] = "Products - Online Store"
        viewData["subtitle"] =  "List of products"
        viewData["products"] = Product.objects.all()

        return render(request, self.template_name, viewData)

class ProductShowView(View):
    template_name = 'products/show.html'

    def get(self, request, id):
        # Check if the product ID is valid
        try:
            product_id = int(id)
            if product_id < 1:
                 raise ValueError("Product id must be 1 or greater")
        except (ValueError, IndexError): 
            return HttpResponseRedirect(reverse('home'))


   
        product = get_object_or_404(Product, pk=product_id)
        viewData = {}
    
        viewData["title"] = product.name + " - Online Store"
        viewData["subtitle"] =  product.name + " - Product information"
        viewData["product"] = product

        return render(request, self.template_name, viewData)
    

class ProductCreateView(View):
    template_name = 'products/create.html'

    def get(self, request):
        form = ProductForm()
        viewData = {}
        viewData["title"] = "Create product"
        viewData["form"] = form
        return render(request, self.template_name, viewData)

    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            # Proper redirection using reverse() to the product detail page
            return redirect(reverse('show', args=[form.instance.id]))
        else:
            viewData = {}
            viewData["title"] = "Create product"
            viewData["form"] = form
            return render(request, self.template_name, viewData)

class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'  # This will allow you to loop through 'products' in your template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Products - Online Store'
        context['subtitle'] = 'List of products'
        return context

class CartView(View):
    template_name = 'cart/index.html'
    
    def get(self, request):
        # Simulated database for products
        products = Product.objects.all()
        cart_product_data = request.session.get('cart_product_data', {})
        cart_products = [product for product in products if str(product.id) in cart_product_data]
        
        viewData = {}
        viewData["title"] = "Shopping Cart - Online Store"
        viewData["subtitle"] = "Your shopping cart"
        viewData["cart_products"] = cart_products
        viewData['cart_product_data'] = cart_product_data or {}
        viewData["products"] = products
        return render(request, self.template_name, viewData)
    
    def post(self, request, product_id):
        # Add product to cart in session
        cart_product_data = request.session.get('cart_product_data', {})
        cart_product_data[product_id] = cart_product_data.get(product_id, 0) + 1
        request.session['cart_product_data'] = cart_product_data

        return redirect('cart_index')
    


class CartRemoveAllView(View):
    def post(self, request):
        # Remove all products from cart in session
        if 'cart_product_data' in request.session:
            del request.session['cart_product_data']

        return redirect('cart_index')

def ImageViewFactory(image_storage):
    class ImageView(View):
        template_name = 'images/index.html'

        def get(self, request):
            image_url = request.session.get('image_url', '')
            return render(request, self.template_name, {'image_url': image_url})

        def post(self, request):
            image_url = image_storage.store(request)
            request.session['image_url'] = image_url
            return redirect('image_index')
    return ImageView

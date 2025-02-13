from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from django.views import View
from django.urls import reverse
from django import forms
from django.contrib import messages
from .utils import ImageLocalStorage

class HomePageView(TemplateView):
    template_name = 'pages/home.html'

class AboutPageView(TemplateView):
    template_name = 'pages/about.html'
    
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
    template_name = 'pages/contact.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Contact us - Online Store",
            "subtitle": "Contact Information",
            "email": "store@example.com",
            "address": "123 Main Street, City, Country",
            "phone": "+1 234 567 890"
        })
        return context

class Product:
    products = [
        {"id":"1", "name":"TV", "description":"Best TV"},
        {"id":"2", "name":"iPhone", "description":"Best iPhone"},
        {"id":"3", "name":"Chromecast", "description":"Best Chromecast"},
        {"id":"4", "name":"Glasses", "description":"Best Glasses"}
    ]

class ProductIndexView(View):
    template_name = 'products/index.html'
    
    def get(self, request):
        viewData = {}
        viewData["title"] = "Products - Online Store"
        viewData["subtitle"] = "List of products"
        viewData["products"] = Product.products
        return render(request, self.template_name, viewData)

class ProductShowView(View):
    template_name = 'products/show.html'
    
    def get(self, request, id):
        try:
            product = Product.products[int(id)-1]
        except (IndexError, ValueError):
            return HttpResponseRedirect(reverse('home'))
        viewData = {}
        viewData["title"] = product["name"] + " - Online Store"
        viewData["subtitle"] = product["name"] + " - Product information"
        viewData["product"] = product
        return render(request, self.template_name, viewData)

class ProductForm(forms.Form):
    name = forms.CharField(required=True)
    price = forms.FloatField(required=True)

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
            messages.success(request, 'Product created')
            return redirect('index')
        else:
            viewData = {}
            viewData["title"] = "Create product"
            viewData["form"] = form
            return render(request, self.template_name, viewData)


class CartView(View):
    template_name = 'cart/index.html'

    def get(self, request):
        # Simulated database for products
        products = {}
        products[121] = {'name': 'Tv samsung', 'price': '1000'}
        products[11] = {'name': 'Iphone', 'price': '2000'}
        # Get cart products from session
        cart_products = {}
        cart_product_data = request.session.get('cart_product_data', {})
        for key, product in products.items():
            if str(key) in cart_product_data.keys():
                cart_products[key] = product
        # Prepare data for the view
        view_data = {
            'title': 'Cart - Online Store',
            'subtitle': 'Shopping Cart',
            'products': products,
            'cart_products': cart_products
        }
        return render(request, self.template_name, view_data)

    def post(self, request, product_id):
        # Get cart products from session and add the new product
        cart_product_data = request.session.get('cart_product_data', {})
        cart_product_data[product_id] = product_id
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

class ImageViewNoDI(View):
    template_name = 'images/index.html'
    def get(self, request):
        image_url = request.session.get('image_url', '')
        return render(request, self.template_name, {'image_url': image_url})
    def post(self, request):
        image_storage = ImageLocalStorage()
        image_url = image_storage.store(request)
        request.session['image_url'] = image_url
        return redirect('image_index')

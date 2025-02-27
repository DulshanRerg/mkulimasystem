from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.decorators import role_required
from .models import Product
from .forms import ProductForm

def product_list(request):
    """
    Lists all product listings.
    """
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'products/product_list.html', {'products': products})

def product_detail(request, pk):
    """
    Shows details for a single product.
    """
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})


@login_required
@role_required(allowed_roles=['farmer'])
def create_product(request):
    """
    Allows a farmer to create a new product listing.
    """
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            return redirect('products:product_list')
    else:
        form = ProductForm()
    return render(request, 'products/product_create.html', {'form': form})


@login_required
def dashboard(request):
    user_products = Product.objects.filter(user=request.user)
    return render(request, 'products/dashboard.html', {'products': user_products})
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.decorators import role_required
from django.db.models import Q
from .models import Product
from .forms import ProductForm

def product_list(request):
    """
    Displays all products with advanced search and filtering.
    """
    query = request.GET.get('q', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    location = request.GET.get('location', '')
    category = request.GET.get('category', '')
    sort_by = request.GET.get('sort_by', '')
    products = Product.objects.all()
    # Search by crop name
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))

    # Filter by price range
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    # Filter by location
    if location:
        products = products.filter(location__icontains=location)

    # Filter by category
    if category:
        products = products.filter(category__icontains=category)

    # Sorting options
    if sort_by == 'newest':
        products = products.order_by('-created_at')
    elif sort_by == 'lowest_price':
        products = products.order_by('price')
    elif sort_by == 'highest_price':
        products = products.order_by('-price')
    return render(request, 'products/product_list.html', {'products': products})

def product_detail(request, pk):
    """
    Shows details for a single product.
    """
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product, 'user': request.user})

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
            product.farmer = request.user
            product.save()
            return redirect('products:product_list')
    else:
        form = ProductForm()
    return render(request, 'products/product_create.html', {'form': form})

@login_required
@role_required(allowed_roles=['farmer'])
def update_product(request, pk):
    """
    Allows a farmer to update a product listing.
    """
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products:product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/product_update.html', {'form': form})

@login_required
@role_required(allowed_roles=['farmer'])
def delete_product(request,pk):
    """
    Allows a farmer to delete a product listing.
    """
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect('products:product_list')

@login_required
def dashboard(request):
    if request.user.is_admin():
        return render(request, "dashboard/admin_dashboard.html")
    elif request.user.is_farmer():
        return render(request, "dashboard/farmer_dashboard.html")
    else:
        return render(request, "dashboard/buyer_dashboard.html")
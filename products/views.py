from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.decorators import role_required
from django.db.models import Q, Avg
from .models import Product, Review
from .forms import ProductForm, ReviewForm

def product_list(request):
    """
    Displays all products with advanced search and filtering.
    """
    products = Product.objects.all().annotate(average_rating=Avg('reviews__rating'))

    #  Farmers should see only their own products
    if request.user.role == 'farmer':
        products = products.filter(farmer=request.user)

    #  Apply Search Filter
    query = request.GET.get('q')
    if query:
        products = products.filter(name__icontains=query)  # Search by product name

    # ✅ Apply Price Filter
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    # ✅ Apply Location Filter
    location = request.GET.get('location')
    if location:
        products = products.filter(location__icontains=location)

    # ✅ Apply Category Filter
    category = request.GET.get('category')
    if category:
        products = products.filter(category__icontains=category)

    # ✅ Sorting
    sort_by = request.GET.get('sort_by')
    if sort_by == "lowest_price":
        products = products.order_by('price')  # Ascending order
    elif sort_by == "highest_price":
        products = products.order_by('-price')  # Descending order

    return render(request, 'products/product_list.html', {'products': products})

def product_detail(request, pk):
    """
    Shows details for a single product. 
    Allows buyers to rate and review products.
    """
    product = get_object_or_404(Product, pk=pk)
    username = product.farmer
    reviews = product.reviews.all()
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    # Check if buyer has already rated the farmer
    user_review = Review.objects.filter(user=request.user, product=product).first()
    
    # Handle review form submission
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect('products:product_detail', pk=pk)
    else:
        form = ReviewForm()
    return render(request, 'products/product_detail.html', {
        # Pass to template
        'product': product,
        'username': username,
        'reviews': reviews,
        'average_rating': round(average_rating, 1),
        'form': form,
        'user_review': user_review,
    })

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

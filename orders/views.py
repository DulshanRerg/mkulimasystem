from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order
from products.models import Product
from django.http import JsonResponse
import uuid

@login_required
def place_order(request, pk):
    """
    Allows a buyer to place an order for a product.
    """
    product = get_object_or_404(Product, id=pk)

    if request.method == "POST":
        quantity = int(request.POST.get('quantity', 1))
        total_price = quantity * product.price  # ✅ Calculate total price

        # ✅ Generate unique external_id
        external_id = f"ORDER-{uuid.uuid4().hex[:10]}"

        order = Order.objects.create(
            buyer=request.user,
            farmer=product.farmer,
            product=product,
            quantity=quantity,
            total_price=total_price,
            external_id=external_id,  # Assign external transaction ID
            status='pending'
        )
        return redirect('orders:order_detail', order_id=order.id)

    return render(request, 'orders/place_order.html', {'product': product})

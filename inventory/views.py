from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import F, Sum
from .forms import ProductForm
from .models import Product


@login_required
def dashboard(request):
    products = Product.objects.all()

    inventory_value = (
        products.aggregate(
            total=Sum(F("current_quantity") * F("unit_price"))
        )["total"]
        or 0
    )

    low_stock = sum(
        1 for product in products
        if product.status == "Low Stock"
    )

    out_stock = products.filter(current_quantity=0).count()

    context = {
        "total_products": products.count(),
        "inventory_value": inventory_value,
        "low_stock": low_stock,
        "out_stock": out_stock,
        "recent_products": products.order_by("-created_at")[:5],
    }

    return render(request, "inventory/dashboard.html", context)


@login_required
def product_list(request):
    products = Product.objects.all().order_by("name")

    query = request.GET.get("q", "").strip()
    category = request.GET.get("category", "").strip()

    if query:
        products = products.filter(name__icontains=query)

    if category:
        products = products.filter(category__icontains=category)

    categories = Product.objects.values_list(
        "category", flat=True
    ).distinct().order_by("category")

    return render(request, "inventory/product_list.html", {
        "products": products,
        "query": query,
        "selected_category": category,
        "categories": categories,
    })


@login_required
def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Product added successfully.")
            return redirect("product_list")
    else:
        form = ProductForm()

    return render(request, "inventory/product_form.html", {"form": form})


@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully.")
            return redirect("product_detail", pk=pk)
    else:
        form = ProductForm(instance=product)

    return render(request, "inventory/product_form.html", {
        "form": form,
        "product": product,
    })


@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        product_name = product.name
        product.delete()
        messages.success(request, f'"{product_name}" has been deleted.')
        return redirect("product_list")

    return render(request, "inventory/delete.html", {"product": product})


@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "inventory/product_detail.html", {"product": product})

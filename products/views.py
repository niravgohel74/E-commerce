from django.shortcuts import render, redirect
from products.models import *
from django.contrib.auth.models import User
from .models import *
from django.db.models import Q


# Create your views here.
def get_product(request, slug):
    try:
        product = Product.objects.get(slug=slug)
        context = {'product': product}
        if request.GET.get('size'):
            size = request.GET.get('size')
            price = product.get_product_price_by_size(size)
            context['selected_size'] = size
            context['updated_price'] = price

        return render(request, 'products/products.html', context = context)
    except Exception as e:
        print(e)

def search_view(request):
    query = request.GET.get('q')
    results = None

    if not query:
        return redirect('/')
    else:
        try:
            results = Product.objects.filter(
                Q(product_name__icontains=query) | 
                Q(product_description__icontains=query)
            )
        except Product.DoesNotExist:
            print('No results found')

    return render(request, 'products/search.html', {'results': results, 'query': query})

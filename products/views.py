from django.shortcuts import render,redirect
from products.models import Product
# Create your views here.


def get_product(request, slug):
    try:
        product = Product.objects.get(slug=slug)
        context = {'product': product}
        
        # Check if a size is selected
        selected_size = request.GET.get('size')
        if selected_size:
            context['selected_size'] = selected_size
            # Retrieve and pass the updated price based on the selected size
            updated_price = product.get_product_price_by_size(selected_size)
            context['updated_price'] = updated_price
        
        return render(request, 'product/product.html', context=context)
    except Exception as e:
        print(e)





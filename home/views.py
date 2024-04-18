from django.views import View
from products.models import Product

class IndexView(View):
    def get(self, request):
        products = Product.objects.all()
        context = {'products': products}
        return render(request, 'home/index.html', context)

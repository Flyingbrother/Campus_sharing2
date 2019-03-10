from django.shortcuts import render
from df_cart.models import *

# Create your views here.
def cart_count(request):
    if request.session. has_key('user_id'):
        carts = CartInfo.objects.filter(user_id=request.session['user_id'])
        counts = carts.count()
        return counts
    else:
        counts = 0
        return counts


from haystack.views import SearchView
class MySearchView(SearchView):
    def extra_context(self):

        context = super(MySearchView, self).extra_context()
        context['title'] = '搜索'
        context['guest_cart'] = 1
        context['counts'] = cart_count(self.request)
        return context

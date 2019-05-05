from django.shortcuts import render, redirect
from .models import *

# Create your views here.
def order_confirm(request):
    if 'total_q' in request.session:
        del request.session['total_q']
    if 'grand_total' in request.session:
        del request.session['grand_total']

    if 'user_id' in request.session:
        user = User.objects.get(id = request.session['user_id'])
    this_order = Orders.objects.create(total_amount = request.session['secret_total'], user = user)


    if 'og_total' in request.session:
        order_to_add = Orders.objects.get(id = this_order.id)
        original = Products.objects.create(name = "Original", quantity = request.session['og_total'])
        order_to_add.product.add(original)
        del request.session['og_total']

    if 'yaki_total' in request.session:
        order_to_add = Orders.objects.get(id = this_order.id)
        teriyaki = Products.objects.create(name = "Teriyaki", quantity = request.session['yaki_total'])
        order_to_add.product.add(teriyaki)
        del request.session['yaki_total']

    if 'bbq_total' in request.session:
        order_to_add = Orders.objects.get(id = this_order.id)
        bbq = Products.objects.create(name = "Texan BBQ", quantity = request.session['bbq_total'])
        order_to_add.product.add(bbq)
        del request.session['bbq_total']

    if 'spicy_total' in request.session:
        order_to_add = Orders.objects.get(id = this_order.id)
        spicy = Products.objects.create(name = "Spicy", quantity = request.session['spicy_total'])
        order_to_add.product.add(spicy)
        del request.session['spicy_total']

    if 'mango_total' in request.session:
        order_to_add = Orders.objects.get(id = this_order.id)
        mango = Products.objects.create(name = "Mango Habanero", quantity = request.session['mango_total'])
        order_to_add.product.add(mango)
        del request.session['mango_total']

    if 'cart' in request.session:
        del request.session['cart']

    return redirect('/confirmation')

def confirmation(request):
    if 'user_id' in request.session:
        this_user = User.objects.get(id = request.session['user_id'])
        context = {
            'user': this_user,
        }
    else:
        context = {}
    return render(request, "order_app/index.html", context)


def show_order(request, order_id):
    if 'user_id' not in request.session:
        messages.error(request, 'You must be logged in to view that page', extra_tags = 'not_logged_in')
        return redirect('/register')
    this_order = Orders.objects.get(id = order_id)
    products = this_order.product.values()
    context = {
        'all_products': products,
        'this_order': this_order,
        
    }
    return render(request, "order_app/show_order.html", context)
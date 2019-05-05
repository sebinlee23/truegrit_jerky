from django.shortcuts import render, redirect


def main(request):
    return render(request, "first_app/main.html")

def about(request):
    return render(request, "first_app/about.html")

def program(request):
    return render(request, "first_app/program.html")

def order(request):
    return render(request, "first_app/order.html")

def add_cart(request):
    if request.method == "POST":
        if 'total_q' not in request.session:
            request.session['total_q'] = 0
        if 'og_total' not in request.session:
            request.session['og_total'] = 0
        if 'yaki_total' not in request.session:
            request.session['yaki_total'] = 0
        if 'bbq_total' not in request.session:
            request.session['bbq_total'] = 0
        if 'spicy_total' not in request.session:
            request.session['spicy_total'] = 0
        if 'mango_total' not in request.session:
            request.session['mango_total'] = 0

        if request.POST['type'] == 'original':
            request.session['og_total'] += int(request.POST['quantity_original'])
        if request.POST['type'] == 'teriyaki':
            request.session['yaki_total'] += int(request.POST['quantity_teriyaki'])
        if request.POST['type'] == 'bbq':
            request.session['bbq_total'] += int(request.POST['quantity_bbq'])
        if request.POST['type'] == 'spicy':
            request.session['spicy_total'] += int(request.POST['quantity_spicy'])
        if request.POST['type'] == 'mango':
            request.session['mango_total'] += int(request.POST['quantity_mango'])

        request.session['total_q'] = request.session['og_total'] + request.session['yaki_total'] + request.session['bbq_total'] + request.session['spicy_total'] + request.session['mango_total']
        request.session['secret'] = request.session['og_total'] + request.session['yaki_total'] + request.session['bbq_total'] + request.session['spicy_total'] + request.session['mango_total']
        
        request.session['cart'] = {
            'Original': request.session['og_total'],
            'Teriyaki': request.session['yaki_total'],
            'Texan-BBQ': request.session['bbq_total'],
            'Spicy': request.session['spicy_total'],
            'Mango-Habanero': request.session['mango_total'],
        }
        request.session['grand_total'] = request.session['total_q'] * 4.99
        request.session['secret_total'] = request.session['total_q'] * 4.99
    return redirect('/shop')

def update(request, product_name):
    if request.method == "POST":
        if product_name == 'Original':
            request.session['og_total'] = int(request.POST['Original'])
        if product_name == 'Teriyaki':
            request.session['yaki_total'] = int(request.POST['Teriyaki'])
        if product_name == 'Texan-BBQ':
            request.session['bbq_total'] = int(request.POST['Texan-BBQ'])
        if product_name == 'Spicy':
            request.session['spicy_total'] = int(request.POST['Spicy'])
        if product_name == 'Mango-Habanero':
            request.session['mango_total'] = int(request.POST['Mango-Habanero'])

        request.session['total_q'] = request.session['og_total'] + request.session['yaki_total'] + request.session['bbq_total'] + request.session['spicy_total'] + request.session['mango_total']
        request.session['secret'] = request.session['og_total'] + request.session['yaki_total'] + request.session['bbq_total'] + request.session['spicy_total'] + request.session['mango_total']

        request.session['cart'] = {
            'Original': request.session['og_total'],
            'Teriyaki': request.session['yaki_total'],
            'Texan-BBQ': request.session['bbq_total'],
            'Spicy': request.session['spicy_total'],
            'Mango-Habanero': request.session['mango_total'],
        }
        request.session['grand_total'] = request.session['total_q'] * 4.99
        request.session['secret_total'] = request.session['total_q'] * 4.99
    return redirect('/cart')

def delete(request, product_name):
    if product_name == 'Original':
        request.session['og_total'] = 0
    if product_name == 'Teriyaki':
        request.session['yaki_total'] = 0
    if product_name == 'Texan-BBQ':
        request.session['bbq_total'] = 0
    if product_name == 'Spicy':
        request.session['spicy_total'] = 0
    if product_name == 'Mango-Habanero':
        request.session['mango_total'] = 0

    request.session['total_q'] = request.session['og_total'] + request.session['yaki_total'] + request.session['bbq_total'] + request.session['spicy_total'] + request.session['mango_total']
    
    request.session['cart'] = {
        'Original': request.session['og_total'],
        'Teriyaki': request.session['yaki_total'],
        'Texan-BBQ': request.session['bbq_total'],
        'Spicy': request.session['spicy_total'],
        'Mango-Habanero': request.session['mango_total'],
    }
    request.session['grand_total'] = request.session['total_q'] * 4.99
    return redirect('/cart')

def cart(request):
    return render(request, "first_app/cart.html")
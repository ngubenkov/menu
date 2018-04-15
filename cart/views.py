from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from cupons.forms import CuponApllyForm


@require_POST
def CartAdd(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'],
                                  update_quantity=cd['update'])
    return redirect('cart:CartDetail')

def CartSubmit(request):
    cart = Cart(request)

    product_list = cart.get_email_values()
    context = {
        'product_list': product_list
    }
    message = render_to_string('cart/order_email.html', context)
    subject, from_email, to_emails = "New order", settings.EMAIL_HOST_USER, ["frozmanik@gmail.com"]
    email = EmailMessage(subject, message, to=to_emails, from_email=from_email)
    email.content_subtype = 'html'
    email.send()
    cart.clear()
    return redirect('cart:CartDetail')

def CartRemove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:CartDetail')

def CartDetail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
                                        initial={
                                            'quantity': item['quantity'],
                                            'update': True
                                        })
    cupon_apply_form = CuponApllyForm()
    return render(request, 'cart/detail.html',
                 {'cart': cart, 'cupon_apply_form': cupon_apply_form})

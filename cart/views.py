from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string
from django.views.generic import TemplateView
from django.core.mail import EmailMessage
from django.conf import settings
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm, CommentForm
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


def CartSubmit(request):  # post request
    cart = Cart(request)
    product_list = cart.get_email_values()
    form = CommentForm(request.POST)
    if form.is_valid():
        text = form.cleaned_data['post']

    context = {
        'product_list': product_list,
        'text': text
    }

    message = render_to_string('cart/order_email.html', context)
    subject, from_email, to_emails = "New order", settings.EMAIL_HOST_USER, ["emenukitchen@gmail.com"]
    email = EmailMessage(subject, message, to=to_emails, from_email=from_email)
    email.content_subtype = 'html'
    email.send()
    cart.clear()

    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
                                        initial={
                                            'quantity': item['quantity'],
                                            'update': True
                                        })


    return render(request, 'cart/order_sent.html',
                 {'cart': cart, 'form': form})

def CartRemove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:CartDetail')


def CartDetail(request):  # get request
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
                                        initial={
                                            'quantity': item['quantity'],
                                            'update': True
                                        })

    form = CommentForm()
    return render(request, 'cart/detail.html',
                 {'cart': cart, 'form': form})

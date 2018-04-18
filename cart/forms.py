from django import forms


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int, label="quantity")
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
    #comment = forms.CharField(label = "comment",required = False)


class CommentForm(forms.Form):
    post =forms.CharField(required=False)

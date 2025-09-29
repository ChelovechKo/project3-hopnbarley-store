from django import forms


class CheckoutForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    phone = forms.CharField(max_length=30)
    city = forms.CharField(max_length=100)
    address = forms.CharField(widget=forms.Textarea, max_length=200)
    payment_method = forms.ChoiceField(
        choices=[('debit', 'Debit Card'), ('wallet', 'Digital Wallet'), ('cod', 'Cash On Delivery')],
        initial='debit'
    )

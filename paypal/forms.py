from django import forms
from paypal.models import PaypalSettings, PaypapPayment


class PaypalSettingsForm(forms.ModelForm):
    
    class Meta:
        model = PaypalSettings
        fields = PaypalSettings.FORM_FIELDS
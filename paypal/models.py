from django.db import models
from django.contrib.auth.models import User
from paypal import constants as Constants
from django.utils import timezone
import datetime
import uuid

# Create your models here.

class PaypalSettings(models.Model):
    client_id = models.TextField(null=True)
    app_name = models.CharField(max_length=Constants.CHARFIELD_MIN_LENGTH, blank=True)
    app_id = models.CharField(max_length=Constants.CHARFIELD_MIN_LENGTH, blank=True, null=True)
    secret = models.TextField(null=True)
    access_token = models.TextField(blank=True, null=True)
    token_added_at = models.DateTimeField(blank=True, null=True)
    token_type = models.CharField(max_length=Constants.CHARFIELD_MIN_LENGTH, blank=True, null=True)
    expires_in = models.IntegerField(blank=True, null=True)
    nonce = models.CharField(max_length=Constants.CHARFIELD_MIN_LENGTH, blank=True, null=True)
    scope = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    api_auth_content_type = models.CharField(max_length=Constants.CHARFIELD_MIN_LENGTH, blank=True, null=True)
    api_auth_grand_type = models.CharField(max_length=Constants.CHARFIELD_MIN_LENGTH, blank=True, null=True)
    api_root_url = models.TextField(max_length=Constants.PAYPAL_API_URL_LENGTH, blank=True, null=True)
    api_url = models.TextField(max_length=Constants.PAYPAL_API_URL_LENGTH, blank=True, null=True)
    auth_url = models.TextField(max_length=Constants.PAYPAL_API_URL_LENGTH, blank=True, null=True)
    success_url = models.TextField(max_length=Constants.REDIRECT_URL_LENGTH, blank=True, null=True)
    failed_url = models.TextField(max_length=Constants.REDIRECT_URL_LENGTH, blank=True, null=True)
    update_url = models.TextField(max_length=Constants.REDIRECT_URL_LENGTH, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    last_edited_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='added_paypal_settings', blank=False, null=False)
    changed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='changed_paypal_settings', blank=False, null=False)
    setting_uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    
    FORM_FIELDS = ['client_id','app_name', 'app_id','secret', 'access_token', 'token_added_at', 'token_type', 'expires_in', 'nonce', 'scope',
        'is_active','api_root_url', 'api_url', 'auth_url', 'success_url', 'failed_url', 'update_url', 'added_by', 'changed_by'
    ]
    
    def as_dict(self):
        changed_by = None
        if self.changed_by:
            changed_by = {
                'username': self.changed_by.username,
                'first_name': self.changed_by.first_name,
                'last_name': self.changed_by.last_name
            }
        return {
            'app_name': self.app_name,
            'client_id': self.client_id,
            'secret': self.secret,
            'created_at': self.created_at,
            'last_edited_at': self.last_edited_at,
            'added_by': {
                'username': self.added_by.username,
                'first_name': self.added_by.first_name,
                'last_name': self.added_by.last_name
            },
            'changed_by': changed_by
        }


class PaypapPayment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='paypal_payments', blank=False, null=False)
    amount = models.DecimalField(blank=False, null=False, max_digits=Constants.PRODUCT_PRICE_MAX_DIGITS, decimal_places=Constants.PRODUCT_PRICE_DECIMAL_PLACES)
    order_ref = models.IntegerField()
    transaction_id = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    validated = models.BooleanField(default=True)
    plateform_fee = models.DecimalField(max_digits=5,decimal_places=4, blank=True, null=True)
    commission =  models.DecimalField( max_digits=Constants.PRODUCT_PRICE_MAX_DIGITS, decimal_places=Constants.PRODUCT_PRICE_DECIMAL_PLACES, blank=True, null=True)
    success_url = models.TextField(max_length=Constants.REDIRECT_URL_LENGTH, blank=True, null=True)
    failed_url = models.TextField(max_length=Constants.REDIRECT_URL_LENGTH, blank=True, null=True)
    update_url = models.TextField(max_length=Constants.REDIRECT_URL_LENGTH, blank=True, null=True)
    failed_reason = models.IntegerField(blank=True, null=True)
    paypal_payment_uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    
    
    def as_dict(self):
        
        return {
            'user': {
                'username': self.user.username,
                'first_name': self.user.first_name,
                'last_name': self.user.last_name
            },
            'amount': self.amount,
            'order_ref': self.order_ref,
            'transaction_id': self.transaction_id,
            'created_at': self.created_at,
            'validated' : self.validated,
            'plateform_fee': self.plateform_fee,
            'commission': self.commission,
            'success_url': self.success_url,
            'failed_url': self.failed_url,
            'update_url' : self.update_url,
            'failed_reason' : self.failed_reason,
            'uuid': self.paypal_payment_uuid
        }
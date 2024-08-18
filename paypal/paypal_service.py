from django.contrib.auth.models import User
from django.db.models import F,Q,Count, Sum, FloatField
from django.db import transaction
from paypal.models import PaypalSettings, PaypapPayment
from paypal.forms import PaypalSettingsForm
from paypal import constants as Constants
from django.utils import timezone
import datetime
import base64
import requests
import logging


logger = logging.getLogger(__name__)



def get_setting():
    return PaypalSettings.objects.first()



def create_setting(user, data):
    form = PaypalSettingsForm(data)
    if form.is_valid():
        form.save()
        return {'success': True}
    else:
        logger.warning(f"Error on creating Paypal Setting : {form.errors.as_text()}")
        return {'success': False, 'errors': form.errors} 
    

def update_setting(user, data, paypal_setting):
    form = PaypalSettingsForm(data, instance=paypal_setting)
    if form.is_valid():
        form.save()
        return {'success': True}
    else:
        logger.warning(f"Error on updating Paypal Setting : {form.errors.as_text()}")
        return {'success': False, 'errors': form.errors} 


def auth_request():
    paypal_settings = PaypalSettings.objects.first()
    if paypal_settings is None:
        logger.warning(f"No paypal setting found. Please add paypal setting first")
        return
    
    if not paypal_settings.is_active:
        logger.warning(f"PayPal Setting found but is not activated. Please activate the setting first or add a new setting")
        return
    
    data = {
        'grant_type': Constants.PAYPAL_AUTH_GRANT_TYPE_HEADER
    }
    #auth = (paypal_settings.client_id, paypal_settings.secret)
    CLIENT_AUTH = Constants.PAYPAL_AUTH_HEADER_PREFIX + base64.b64encode(f"{paypal_settings.client_id}:{paypal_settings.secret}".encode()).decode()
    headers={
        'Content-Type': Constants.PAYPAL_AUTH_HEADER_CONTENT_TYPE,
        'Authorization': CLIENT_AUTH
    }
    auth_url = f"{paypal_settings.api_root_url}{paypal_settings.auth_url}"
    logger.debug(f'Sending auth request to url {paypal_settings.auth_url}')
    response = None
    request_date = timezone.now()
    try:
        response = requests.post(auth_url, data=data, headers=headers)
        logger.debug(f'auth request response : {response}')
        if not response:
            logger.error(f"Error on requesting a payment to the url {paypal_settings.auth_url} : status code {response.status_code} - error : {response}")
            return False
        response_data = response.json()
        logger.debug(f"PayPal Auth Response JSON : {response_data}")
        PaypalSettings.objects.filter(pk=paypal_settings.pk).update(
            token_added_at=request_date,
            scope=response_data['scope'], access_token=response_data['access_token'], token_type=response_data['token_type'], app_id=response_data['app_id'],
            expires_in=response_data['expires_in'], nonce=response_data['nonce']
        )
        return True
    except Exception as e:
        logger.error(f"Error on sending Payment request at url {paypal_settings.auth_url}")
        logger.exception(e)
    return False


def request_payment(data=None):
    paypal_settings = PaypalSettings.objects.first()
    if paypal_settings is None:
        logger.warning(f"No paypal setting found. Please add paypal setting first")
    
    data = {
        
    }
    
    
    return None
"""
M-Pesa integration using django_daraja library
"""
from django_daraja.mpesa.core import MpesaClient
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class DarajaMpesaService:
    """M-Pesa payment service using django_daraja"""
    
    def __init__(self):
        self.client = MpesaClient()
    
    def initiate_stk_push(self, phone_number, amount, consultation_id, description, callback_url):
        """
        Initiate STK Push for M-Pesa payment
        
        Args:
            phone_number: Customer phone number (254XXXXXXXXX format)
            amount: Amount in KES
            consultation_id: Consultation ID for reference
            description: Transaction description
            callback_url: Callback URL for payment notification
        
        Returns:
            dict: Response containing CheckoutRequestID or error
        """
        try:
            # Format phone number
            phone = self._format_phone(phone_number)
            
            # Initiate STK push
            response = self.client.stk_push(
                phone_number=phone,
                amount=int(amount),
                account_reference=f'CONSULT-{consultation_id}',
                transaction_desc=description[:40],  # Max 40 chars
                callback_url=callback_url
            )
            
            logger.info(f"STK Push initiated for {phone}: {response}")
            
            return {
                'success': True,
                'checkout_request_id': response.get('CheckoutRequestID'),
                'merchant_request_id': response.get('MerchantRequestID'),
                'response_code': response.get('ResponseCode'),
                'response_description': response.get('ResponseDescription'),
                'customer_message': response.get('CustomerMessage')
            }
        
        except Exception as e:
            logger.error(f"STK Push failed: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def query_transaction(self, checkout_request_id):
        """
        Query STK Push transaction status
        
        Args:
            checkout_request_id: CheckoutRequestID from STK push
        
        Returns:
            dict: Transaction status response
        """
        try:
            response = self.client.query_stk_push_status(
                checkout_request_id=checkout_request_id
            )
            
            logger.info(f"Transaction query result: {response}")
            
            return {
                'success': True,
                'data': response
            }
        
        except Exception as e:
            logger.error(f"Transaction query failed: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _format_phone(self, phone_number):
        """
        Format phone number to 254XXXXXXXXX format
        
        Args:
            phone_number: Phone number in various formats
        
        Returns:
            str: Formatted phone number
        """
        phone = phone_number.replace('+', '').replace(' ', '').replace('-', '')
        
        # Remove leading 0 and add country code
        if phone.startswith('0'):
            phone = '254' + phone[1:]
        elif not phone.startswith('254'):
            phone = '254' + phone
        
        return phone
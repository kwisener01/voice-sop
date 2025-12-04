import requests
import logging

logger = logging.getLogger(__name__)


class LindyService:
    """Service for sending callbacks to Lindy"""

    def __init__(self, webhook_url, webhook_secret=None):
        self.webhook_url = webhook_url
        self.webhook_secret = webhook_secret

    def notify_sop_completed(self, call_id, document_url, document_title, customer_info, sop_content=None):
        """
        Notify Lindy that SOP has been completed

        Args:
            call_id (str): VAPI call ID
            document_url (str): Google Doc URL (None if Lindy should create it)
            document_title (str): Document title
            customer_info (dict): Customer information
            sop_content (str): Full SOP text content for Lindy to create document

        Returns:
            dict: Response from Lindy
        """
        try:
            logger.info(f'Notifying Lindy about completed SOP for call: {call_id}')

            payload = {
                'event': 'sop_completed',
                'call_id': call_id,
                'document': {
                    'url': document_url,  # Will be None - Lindy creates the doc
                    'title': document_title,
                    'content': sop_content  # Full SOP content for Lindy
                },
                'customer': {
                    'name': customer_info.get('name'),
                    'email': customer_info.get('email'),
                    'phone': customer_info.get('phone'),
                    'contact_id': customer_info.get('contact_id'),
                    'company': customer_info.get('company')
                },
                'status': 'completed',
                'timestamp': self._get_timestamp()
            }

            headers = {
                'Content-Type': 'application/json'
            }

            if self.webhook_secret:
                headers['X-Webhook-Secret'] = self.webhook_secret

            response = requests.post(
                self.webhook_url,
                json=payload,
                headers=headers,
                timeout=30
            )

            response.raise_for_status()

            logger.info(f'Successfully notified Lindy: {response.status_code}')

            return {
                'success': True,
                'status_code': response.status_code,
                'response': response.json() if response.text else None
            }

        except requests.exceptions.RequestException as e:
            logger.error(f'Failed to notify Lindy: {str(e)}')
            return {
                'success': False,
                'error': str(e)
            }

    def notify_sop_started(self, call_id, customer_info):
        """
        Notify Lindy that SOP generation has started

        Args:
            call_id (str): VAPI call ID
            customer_info (dict): Customer information

        Returns:
            dict: Response from Lindy
        """
        try:
            logger.info(f'Notifying Lindy that SOP generation started for call: {call_id}')

            payload = {
                'event': 'sop_started',
                'call_id': call_id,
                'customer': {
                    'name': customer_info.get('name'),
                    'email': customer_info.get('email'),
                    'phone': customer_info.get('phone'),
                    'contact_id': customer_info.get('contact_id')
                },
                'status': 'processing',
                'timestamp': self._get_timestamp()
            }

            headers = {'Content-Type': 'application/json'}
            if self.webhook_secret:
                headers['X-Webhook-Secret'] = self.webhook_secret

            response = requests.post(
                self.webhook_url,
                json=payload,
                headers=headers,
                timeout=30
            )

            response.raise_for_status()
            return {'success': True, 'status_code': response.status_code}

        except requests.exceptions.RequestException as e:
            logger.error(f'Failed to notify Lindy (start): {str(e)}')
            return {'success': False, 'error': str(e)}

    def notify_error(self, call_id, error_message, customer_info=None):
        """
        Notify Lindy about an error during SOP generation

        Args:
            call_id (str): VAPI call ID
            error_message (str): Error description
            customer_info (dict): Optional customer information

        Returns:
            dict: Response from Lindy
        """
        try:
            logger.info(f'Notifying Lindy about error for call: {call_id}')

            payload = {
                'event': 'sop_error',
                'call_id': call_id,
                'error': error_message,
                'customer': customer_info if customer_info else {},
                'status': 'failed',
                'timestamp': self._get_timestamp()
            }

            headers = {'Content-Type': 'application/json'}
            if self.webhook_secret:
                headers['X-Webhook-Secret'] = self.webhook_secret

            response = requests.post(
                self.webhook_url,
                json=payload,
                headers=headers,
                timeout=30
            )

            response.raise_for_status()
            return {'success': True, 'status_code': response.status_code}

        except requests.exceptions.RequestException as e:
            logger.error(f'Failed to notify Lindy (error): {str(e)}')
            return {'success': False, 'error': str(e)}

    def send_custom_event(self, event_type, data):
        """
        Send custom event to Lindy

        Args:
            event_type (str): Event type
            data (dict): Event data

        Returns:
            dict: Response from Lindy
        """
        try:
            payload = {
                'event': event_type,
                'data': data,
                'timestamp': self._get_timestamp()
            }

            headers = {'Content-Type': 'application/json'}
            if self.webhook_secret:
                headers['X-Webhook-Secret'] = self.webhook_secret

            response = requests.post(
                self.webhook_url,
                json=payload,
                headers=headers,
                timeout=30
            )

            response.raise_for_status()
            return {'success': True, 'status_code': response.status_code}

        except requests.exceptions.RequestException as e:
            logger.error(f'Failed to send custom event to Lindy: {str(e)}')
            return {'success': False, 'error': str(e)}

    def _get_timestamp(self):
        """Get current timestamp in ISO format"""
        from datetime import datetime
        return datetime.utcnow().isoformat() + 'Z'

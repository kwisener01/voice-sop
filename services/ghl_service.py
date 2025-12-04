import requests
import logging

logger = logging.getLogger(__name__)


class GHLService:
    """Service for interacting with GoHighLevel API"""

    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://rest.gohighlevel.com/v1'
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }

    def send_document(self, contact_id, document_url, document_title):
        """
        Send document to contact via GHL

        Args:
            contact_id (str): GHL contact ID
            document_url (str): URL to the Google Doc
            document_title (str): Title of the document

        Returns:
            dict: Result of the operation
        """
        try:
            logger.info(f'Sending document to GHL contact: {contact_id}')

            # Send via SMS
            sms_result = self._send_sms(
                contact_id,
                f"Your SOP document '{document_title}' is ready! View it here: {document_url}"
            )

            # Send via Email
            email_result = self._send_email(
                contact_id,
                f"Your SOP: {document_title}",
                self._create_email_body(document_title, document_url)
            )

            # Add note to contact
            note_result = self._add_note(
                contact_id,
                f"SOP Document Created: {document_title}\nURL: {document_url}"
            )

            # Create task for follow-up
            task_result = self._create_task(
                contact_id,
                f"Follow up on SOP: {document_title}"
            )

            logger.info('Document sent to GHL successfully')

            return {
                'success': True,
                'sms_sent': sms_result['success'],
                'email_sent': email_result['success'],
                'note_added': note_result['success'],
                'task_created': task_result['success']
            }

        except Exception as e:
            logger.error(f'Failed to send document to GHL: {str(e)}')
            raise Exception(f'GHL API Error: {str(e)}')

    def _send_sms(self, contact_id, message):
        """Send SMS to contact"""
        try:
            response = requests.post(
                f'{self.base_url}/conversations/messages',
                headers=self.headers,
                json={
                    'contactId': contact_id,
                    'type': 'SMS',
                    'message': message
                },
                timeout=30
            )

            response.raise_for_status()
            return {'success': True, 'data': response.json()}

        except requests.exceptions.RequestException as e:
            logger.error(f'Failed to send SMS: {str(e)}')
            return {'success': False, 'error': str(e)}

    def _send_email(self, contact_id, subject, body):
        """Send email to contact"""
        try:
            # Get contact details first
            contact = self.get_contact(contact_id)
            email = contact.get('email')

            if not email:
                logger.warning(f'No email found for contact: {contact_id}')
                return {'success': False, 'error': 'No email address'}

            response = requests.post(
                f'{self.base_url}/conversations/messages',
                headers=self.headers,
                json={
                    'contactId': contact_id,
                    'type': 'Email',
                    'subject': subject,
                    'html': body,
                    'emailTo': email
                },
                timeout=30
            )

            response.raise_for_status()
            return {'success': True, 'data': response.json()}

        except requests.exceptions.RequestException as e:
            logger.error(f'Failed to send email: {str(e)}')
            return {'success': False, 'error': str(e)}

    def _add_note(self, contact_id, note_text):
        """Add note to contact"""
        try:
            response = requests.post(
                f'{self.base_url}/contacts/{contact_id}/notes',
                headers=self.headers,
                json={
                    'body': note_text
                },
                timeout=30
            )

            response.raise_for_status()
            return {'success': True, 'data': response.json()}

        except requests.exceptions.RequestException as e:
            logger.error(f'Failed to add note: {str(e)}')
            return {'success': False, 'error': str(e)}

    def _create_task(self, contact_id, title, due_days=7):
        """Create follow-up task"""
        try:
            from datetime import datetime, timedelta

            due_date = (datetime.now() + timedelta(days=due_days)).isoformat()

            response = requests.post(
                f'{self.base_url}/contacts/{contact_id}/tasks',
                headers=self.headers,
                json={
                    'title': title,
                    'dueDate': due_date,
                    'completed': False
                },
                timeout=30
            )

            response.raise_for_status()
            return {'success': True, 'data': response.json()}

        except requests.exceptions.RequestException as e:
            logger.error(f'Failed to create task: {str(e)}')
            return {'success': False, 'error': str(e)}

    def get_contact(self, contact_id):
        """Get contact details"""
        try:
            response = requests.get(
                f'{self.base_url}/contacts/{contact_id}',
                headers=self.headers,
                timeout=30
            )

            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f'Failed to get contact: {str(e)}')
            raise Exception(f'GHL API Error: {str(e)}')

    def update_contact(self, contact_id, data):
        """Update contact information"""
        try:
            response = requests.put(
                f'{self.base_url}/contacts/{contact_id}',
                headers=self.headers,
                json=data,
                timeout=30
            )

            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f'Failed to update contact: {str(e)}')
            raise Exception(f'GHL API Error: {str(e)}')

    def add_tag(self, contact_id, tag):
        """Add tag to contact"""
        try:
            response = requests.post(
                f'{self.base_url}/contacts/{contact_id}/tags',
                headers=self.headers,
                json={'tags': [tag]},
                timeout=30
            )

            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f'Failed to add tag: {str(e)}')
            raise Exception(f'GHL API Error: {str(e)}')

    def _create_email_body(self, title, url):
        """Create HTML email body"""
        return f"""
        <html>
        <body style="font-family: Arial, sans-serif; padding: 20px;">
            <h2 style="color: #333;">Your SOP Document is Ready!</h2>

            <p>Hello,</p>

            <p>We've created your Standard Operating Procedure document: <strong>{title}</strong></p>

            <div style="margin: 30px 0;">
                <a href="{url}"
                   style="background-color: #4CAF50;
                          color: white;
                          padding: 15px 32px;
                          text-align: center;
                          text-decoration: none;
                          display: inline-block;
                          font-size: 16px;
                          border-radius: 4px;">
                    View Your SOP Document
                </a>
            </div>

            <p>Or copy this link: <a href="{url}">{url}</a></p>

            <p style="margin-top: 30px; color: #666; font-size: 14px;">
                If you have any questions or need revisions, please don't hesitate to reach out.
            </p>

            <p style="color: #666; font-size: 14px;">
                Best regards,<br>
                Your SOP Team
            </p>
        </body>
        </html>
        """

    def trigger_workflow(self, contact_id, workflow_id):
        """Trigger a GHL workflow for contact"""
        try:
            response = requests.post(
                f'{self.base_url}/contacts/{contact_id}/workflow/{workflow_id}',
                headers=self.headers,
                timeout=30
            )

            response.raise_for_status()
            return {'success': True, 'data': response.json()}

        except requests.exceptions.RequestException as e:
            logger.error(f'Failed to trigger workflow: {str(e)}')
            raise Exception(f'GHL API Error: {str(e)}')

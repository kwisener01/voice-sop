import requests
import logging

logger = logging.getLogger(__name__)


class VAPIService:
    """Service for interacting with VAPI API"""

    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://api.vapi.ai'
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }

    def create_assistant(self, config):
        """
        Create a new VAPI assistant

        Args:
            config (dict): Assistant configuration
                - name: Assistant name
                - model: Model configuration
                - voice: Voice configuration
                - firstMessage: First message to user
                - serverUrl: Webhook URL for callbacks

        Returns:
            dict: Created assistant data including ID
        """
        try:
            logger.info(f'Creating VAPI assistant: {config.get("name")}')

            response = requests.post(
                f'{self.base_url}/assistant',
                headers=self.headers,
                json=config,
                timeout=30
            )

            response.raise_for_status()
            assistant = response.json()

            logger.info(f'Successfully created assistant with ID: {assistant.get("id")}')
            return assistant

        except requests.exceptions.RequestException as e:
            logger.error(f'Failed to create VAPI assistant: {str(e)}')
            raise Exception(f'VAPI API Error: {str(e)}')

    def get_assistant(self, assistant_id):
        """Get assistant by ID"""
        try:
            response = requests.get(
                f'{self.base_url}/assistant/{assistant_id}',
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f'Failed to get assistant: {str(e)}')
            raise Exception(f'VAPI API Error: {str(e)}')

    def update_assistant(self, assistant_id, config):
        """Update an existing assistant"""
        try:
            response = requests.patch(
                f'{self.base_url}/assistant/{assistant_id}',
                headers=self.headers,
                json=config,
                timeout=30
            )
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f'Failed to update assistant: {str(e)}')
            raise Exception(f'VAPI API Error: {str(e)}')

    def delete_assistant(self, assistant_id):
        """Delete an assistant"""
        try:
            response = requests.delete(
                f'{self.base_url}/assistant/{assistant_id}',
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            return {'success': True, 'message': f'Assistant {assistant_id} deleted'}

        except requests.exceptions.RequestException as e:
            logger.error(f'Failed to delete assistant: {str(e)}')
            raise Exception(f'VAPI API Error: {str(e)}')

    def list_assistants(self):
        """List all assistants"""
        try:
            response = requests.get(
                f'{self.base_url}/assistant',
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f'Failed to list assistants: {str(e)}')
            raise Exception(f'VAPI API Error: {str(e)}')

    def get_call_details(self, call_id):
        """Get details of a specific call"""
        try:
            response = requests.get(
                f'{self.base_url}/call/{call_id}',
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f'Failed to get call details: {str(e)}')
            raise Exception(f'VAPI API Error: {str(e)}')

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import logging

logger = logging.getLogger(__name__)


class GoogleDocsService:
    """Service for creating and managing Google Docs"""

    def __init__(self, credentials_path, folder_id=None):
        """
        Initialize Google Docs service

        Args:
            credentials_path (str): Path to Google service account credentials JSON
            folder_id (str): Optional Google Drive folder ID to store documents
        """
        self.credentials_path = credentials_path
        self.folder_id = folder_id
        self.scopes = [
            'https://www.googleapis.com/auth/documents',
            'https://www.googleapis.com/auth/drive'
        ]

        try:
            self.credentials = service_account.Credentials.from_service_account_file(
                credentials_path, scopes=self.scopes
            )
            self.docs_service = build('docs', 'v1', credentials=self.credentials)
            self.drive_service = build('drive', 'v3', credentials=self.credentials)
            logger.info('Google Docs service initialized successfully')

        except Exception as e:
            logger.error(f'Failed to initialize Google Docs service: {str(e)}')
            raise

    def create_document(self, title, content):
        """
        Create a new Google Doc with formatted content

        Args:
            title (str): Document title
            content (str): Markdown content to insert

        Returns:
            dict: Document info with id and url
        """
        try:
            logger.info(f'Creating Google Doc: {title}')

            # Create empty document
            doc = self.docs_service.documents().create(
                body={'title': title}
            ).execute()

            doc_id = doc['documentId']
            logger.info(f'Created document with ID: {doc_id}')

            # Insert content
            self._insert_content(doc_id, content)

            # Move to folder if specified
            if self.folder_id:
                self._move_to_folder(doc_id, self.folder_id)

            # Make document accessible
            self._set_permissions(doc_id)

            doc_url = f'https://docs.google.com/document/d/{doc_id}/edit'

            logger.info(f'Document created successfully: {doc_url}')

            return {
                'id': doc_id,
                'url': doc_url,
                'title': title
            }

        except HttpError as e:
            logger.error(f'Google Docs API error: {str(e)}')
            raise Exception(f'Failed to create Google Doc: {str(e)}')

    def _insert_content(self, doc_id, content):
        """Insert formatted content into document"""
        try:
            # Convert markdown to Google Docs requests
            requests = self._markdown_to_requests(content)

            if requests:
                self.docs_service.documents().batchUpdate(
                    documentId=doc_id,
                    body={'requests': requests}
                ).execute()

                logger.info('Content inserted successfully')

        except Exception as e:
            logger.error(f'Failed to insert content: {str(e)}')
            raise

    def _markdown_to_requests(self, markdown_content):
        """
        Convert markdown content to Google Docs API requests
        This is a simplified version - you may want to enhance this
        """
        requests = []

        # Simple approach: insert all text at beginning
        requests.append({
            'insertText': {
                'location': {'index': 1},
                'text': markdown_content
            }
        })

        # You could enhance this to:
        # - Parse markdown headings and apply heading styles
        # - Parse bold/italic and apply text formatting
        # - Parse lists and apply list formatting
        # - etc.

        return requests

    def _move_to_folder(self, doc_id, folder_id):
        """Move document to specified folder"""
        try:
            # Get current parents
            file = self.drive_service.files().get(
                fileId=doc_id,
                fields='parents'
            ).execute()

            previous_parents = ','.join(file.get('parents', []))

            # Move to new folder
            self.drive_service.files().update(
                fileId=doc_id,
                addParents=folder_id,
                removeParents=previous_parents,
                fields='id, parents'
            ).execute()

            logger.info(f'Document moved to folder: {folder_id}')

        except Exception as e:
            logger.warning(f'Failed to move document to folder: {str(e)}')

    def _set_permissions(self, doc_id, permission_type='anyone', role='reader'):
        """
        Set document permissions

        Args:
            doc_id (str): Document ID
            permission_type (str): 'anyone', 'user', or 'domain'
            role (str): 'reader', 'writer', or 'commenter'
        """
        try:
            permission = {
                'type': permission_type,
                'role': role
            }

            self.drive_service.permissions().create(
                fileId=doc_id,
                body=permission
            ).execute()

            logger.info(f'Permissions set: {permission_type} - {role}')

        except Exception as e:
            logger.warning(f'Failed to set permissions: {str(e)}')

    def update_document(self, doc_id, content, append=False):
        """
        Update existing document content

        Args:
            doc_id (str): Document ID
            content (str): New content
            append (bool): If True, append to existing content; if False, replace
        """
        try:
            if not append:
                # Delete all content first
                doc = self.docs_service.documents().get(documentId=doc_id).execute()
                end_index = doc['body']['content'][-1]['endIndex']

                requests = [{
                    'deleteContentRange': {
                        'range': {
                            'startIndex': 1,
                            'endIndex': end_index - 1
                        }
                    }
                }]

                self.docs_service.documents().batchUpdate(
                    documentId=doc_id,
                    body={'requests': requests}
                ).execute()

            # Insert new content
            self._insert_content(doc_id, content)

            logger.info(f'Document updated: {doc_id}')

        except Exception as e:
            logger.error(f'Failed to update document: {str(e)}')
            raise

    def get_document_content(self, doc_id):
        """Get document content as plain text"""
        try:
            doc = self.docs_service.documents().get(documentId=doc_id).execute()

            content = ''
            for element in doc.get('body', {}).get('content', []):
                if 'paragraph' in element:
                    for text_run in element['paragraph'].get('elements', []):
                        if 'textRun' in text_run:
                            content += text_run['textRun'].get('content', '')

            return content

        except Exception as e:
            logger.error(f'Failed to get document content: {str(e)}')
            raise

    def share_document(self, doc_id, email, role='reader'):
        """
        Share document with specific user

        Args:
            doc_id (str): Document ID
            email (str): User email
            role (str): 'reader', 'writer', or 'commenter'
        """
        try:
            permission = {
                'type': 'user',
                'role': role,
                'emailAddress': email
            }

            self.drive_service.permissions().create(
                fileId=doc_id,
                body=permission,
                sendNotificationEmail=True
            ).execute()

            logger.info(f'Document shared with {email} as {role}')

        except Exception as e:
            logger.error(f'Failed to share document: {str(e)}')
            raise

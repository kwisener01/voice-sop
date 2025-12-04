import hashlib
import secrets
from datetime import datetime
import re


def generate_secure_token(length=32):
    """Generate a secure random token"""
    return secrets.token_urlsafe(length)


def hash_string(value):
    """Hash a string using SHA256"""
    return hashlib.sha256(value.encode()).hexdigest()


def sanitize_filename(filename):
    """Sanitize filename to remove special characters"""
    # Remove special characters
    filename = re.sub(r'[^\w\s-]', '', filename)
    # Replace spaces with underscores
    filename = re.sub(r'\s+', '_', filename)
    return filename


def format_timestamp(dt=None):
    """Format timestamp in ISO format"""
    if dt is None:
        dt = datetime.utcnow()
    return dt.isoformat()


def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_phone(phone):
    """Validate phone number format"""
    # Remove all non-numeric characters
    phone_digits = re.sub(r'\D', '', phone)
    # Check if it's between 10-15 digits
    return 10 <= len(phone_digits) <= 15


def truncate_text(text, max_length=100, suffix='...'):
    """Truncate text to maximum length"""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def extract_customer_info(data):
    """Extract customer information from various data formats"""
    customer_info = {}

    # Try different possible fields
    customer_info['name'] = (
        data.get('name') or
        data.get('customerName') or
        data.get('customer_name') or
        data.get('contact', {}).get('name')
    )

    customer_info['email'] = (
        data.get('email') or
        data.get('customerEmail') or
        data.get('customer_email') or
        data.get('contact', {}).get('email')
    )

    customer_info['phone'] = (
        data.get('phone') or
        data.get('phoneNumber') or
        data.get('phone_number') or
        data.get('contact', {}).get('phone')
    )

    customer_info['company'] = (
        data.get('company') or
        data.get('companyName') or
        data.get('company_name') or
        data.get('contact', {}).get('company')
    )

    customer_info['contact_id'] = (
        data.get('contactId') or
        data.get('contact_id') or
        data.get('contact', {}).get('id')
    )

    # Remove None values
    return {k: v for k, v in customer_info.items() if v is not None}


def parse_transcript(transcript):
    """Parse conversation transcript and extract key information"""
    lines = transcript.split('\n')
    parsed = {
        'total_lines': len(lines),
        'speaker_turns': 0,
        'assistant_messages': [],
        'user_messages': []
    }

    for line in lines:
        if line.strip():
            # Try to detect speaker
            if line.startswith('Assistant:') or line.startswith('AI:'):
                parsed['assistant_messages'].append(line)
                parsed['speaker_turns'] += 1
            elif line.startswith('User:') or line.startswith('Customer:'):
                parsed['user_messages'].append(line)
                parsed['speaker_turns'] += 1

    return parsed


class ResponseFormatter:
    """Format API responses consistently"""

    @staticmethod
    def success(data, message='Success'):
        """Format success response"""
        return {
            'success': True,
            'message': message,
            'data': data,
            'timestamp': format_timestamp()
        }

    @staticmethod
    def error(error, message='An error occurred', status_code=500):
        """Format error response"""
        return {
            'success': False,
            'message': message,
            'error': str(error),
            'timestamp': format_timestamp()
        }, status_code

    @staticmethod
    def paginated(items, page=1, per_page=20, total=None):
        """Format paginated response"""
        if total is None:
            total = len(items)

        return {
            'success': True,
            'data': items,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'pages': (total + per_page - 1) // per_page
            },
            'timestamp': format_timestamp()
        }


def verify_webhook_signature(payload, signature, secret):
    """Verify webhook signature"""
    expected_signature = hashlib.sha256(
        (payload + secret).encode()
    ).hexdigest()

    return secrets.compare_digest(signature, expected_signature)

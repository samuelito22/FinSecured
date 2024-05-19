import logging
import requests
import os


def send_email_alert(subject, message):
    """
    Send an email alert using the MailerSend API.
    """
    mailersend_api_key = os.getenv('MAILERSEND_API_KEY')
    sender_email = os.getenv('SENDER_EMAIL')
    recipient_email = os.getenv('RECIPIENT_EMAIL')

    url = 'https://api.mailersend.com/v1/email'
    headers = {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Authorization': f'Bearer {mailersend_api_key}'
    }
    data = {
        'from': {'email': sender_email},
        'to': [{'email': recipient_email}],
        'subject': subject,
        'text': message,
        'html': message
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 202:
        logging.error(f"Failed to send email alert. Status code: {response.status_code}")

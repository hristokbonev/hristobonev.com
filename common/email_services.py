import sendgrid
import os
from dotenv import load_dotenv
from sendgrid.helpers.mail import Mail, Email, To, Content

load_dotenv()

sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))

def send_email(name: str, email: str, content: str):
    from_email = Email('nicktwickxxx@gmail.com')
    to_email = To('chkbonev@gmail.com')
    subject = f'From Personal Website: {name} {email}'
    content = Content("text/plain", content)
    mail = Mail(from_email, to_email, subject, content)
    sg = sendgrid.SendGridAPIClient(api_key=os.getenv("SENDGRID_API_KEY"))
    response = sg.client.mail.send.post(request_body=mail.get())
    return response.status_code
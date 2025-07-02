import imaplib
import email
from email.header import decode_header
import os
from dotenv import load_dotenv
from conversation import log_conversation, fetch_conversation
from generator import generate_agent_response
from email_utils import send_email

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def fetch_unread_emails():
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    imap.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    imap.select("inbox")

    status, messages = imap.search(None, '(UNSEEN)')
    mail_ids = messages[0].split()

    emails = []
    for num in mail_ids:
        status, msg_data = imap.fetch(num, "(RFC822)")
        raw_msg = msg_data[0][1]
        msg = email.message_from_bytes(raw_msg)

        sender = email.utils.parseaddr(msg["From"])[1]
        subject, _ = decode_header(msg["Subject"])[0]
        subject = subject.decode() if isinstance(subject, bytes) else subject

        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain" and part.get("Content-Disposition") is None:
                    body = part.get_payload(decode=True).decode()
                    break
        else:
            body = msg.get_payload(decode=True).decode()

        emails.append({"from": sender, "subject": subject, "body": body})

    imap.logout()
    return emails

def process_emails():
    for mail in fetch_unread_emails():
        sender = mail["from"]
        body = mail["body"]

        log_conversation(sender, "human", body)

        history = fetch_conversation(sender)
        reply = generate_agent_response(history, body)

        send_email(sender, "Re: Your Query", reply)
        log_conversation(sender, "agent", reply)

if __name__ == "__main__":
    process_emails()

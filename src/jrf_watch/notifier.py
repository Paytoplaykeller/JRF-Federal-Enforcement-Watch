from __future__ import annotations

import os
import smtplib
from email.message import EmailMessage
from pathlib import Path


def email_enabled() -> bool:
    return os.getenv("JRF_EMAIL_ENABLED", "").lower() == "true"


def send_alert(subject: str, body: str, attachment: Path | None = None) -> None:
    if not email_enabled():
        raise RuntimeError("Email sending disabled. Set JRF_EMAIL_ENABLED=true explicitly.")

    host = os.environ["JRF_SMTP_HOST"]
    port = int(os.getenv("JRF_SMTP_PORT", "587"))
    user = os.environ["JRF_SMTP_USER"]
    password = os.environ["JRF_SMTP_PASSWORD"]
    sender = os.environ["JRF_ALERT_FROM"]
    recipient = os.environ["JRF_ALERT_TO"]

    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = subject
    msg.set_content(body)

    if attachment is not None:
        msg.add_attachment(
            attachment.read_bytes(),
            maintype="application",
            subtype="octet-stream",
            filename=attachment.name,
        )

    with smtplib.SMTP(host, port, timeout=30) as smtp:
        smtp.starttls()
        smtp.login(user, password)
        smtp.send_message(msg)

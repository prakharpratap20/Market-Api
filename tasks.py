import os
import requests
from dotenv import load_dotenv
import jinja2

load_dotenv()

DOMAIN = os.getenv("MAILGUN_DOMAIN")
template_loader = jinja2.FileSystemLoader("templates")
template_env = jinja2.Environment(loader=template_loader)


def render_template(template_filename, **context):
    """
    Renders a Jinja template with the given context.
    """
    return template_env.get_template(template_filename).render(**context)


def send_simple_message(to, subject, body, html):
    """
    Sends an email using the Mailgun API.
    """
    return requests.post(
        f"https://api.mailgun.net/v3/{DOMAIN}/messages",
        auth=("api", os.getenv("MAILGUN_API_KEY")),
        data={
            "from": f"Jose Salvatierra <mailgun@{DOMAIN}>",
            "to": [to],
            "subject": subject,
            "text": body,
            "html": html,
        },
    )


def send_user_registration_email(email, username):
    """
    Sends a registration email to the user.
    """
    return send_simple_message(
        email,
        "Successfully signed up",
        f"Hi {username}! You have successfully signed up to the Stores API.",
        render_template("email/registration.html", username=username),
    )

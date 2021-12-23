from requests import Response, post
import os

class Mailgun:
    DOMAIN_NAME = os.environ.get("DOMAIN_NAME")
    API_KEY = os.environ.get("API_KEY")
    BASE_URL = f"https://api.mailgun.net/v3/{DOMAIN_NAME}/messages" 
    FROM_URL = f"<mailgun@{ DOMAIN_NAME }>"

   
    @classmethod
    def send_confirmation(cls, title: str, to_mail: str, subject: str, html_str: str ) -> Response:
            
            return post(
                cls.BASE_URL, 
                auth=("api", cls.API_KEY),
                data={
                    "from": f"{ title } {cls.FROM_URL}",
                    "to": to_mail,
                    "subject": subject,
                    "text":  html_str,
                    },
                )
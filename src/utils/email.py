from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

class Email:
    def __init__(self, settings: dict) -> None:
        self.__host = settings["host"]
        self.__port = settings["port"]
        self.__user = settings["user"]
        self.__password = settings["password"]
        self.__from = settings["from"]
        self.__to = settings["to"]
        self.__switch = settings["switch"]
        self.__prefix = "=="

    def __connect(self):
        try:
            smtp = smtplib.SMTP(host=self.__host, port=self.__port)
            smtp.starttls()
            smtp.ehlo()
            smtp.login(user=self.__user, password=self.__password)
            return smtp
        except:
            raise NameError("Could not connect to smtp")

    def __template(self, payload: dict) -> str:

        # Build the template

        name = payload["template"]["name"]
        try:
            with open(f"src/templates/{name}.html", "r") as f:
                template = f.read()
        except:
            raise NameError(f"Error reading template {name}")

        door = payload["template"]["payload"]

        for key in door:
            template = template.replace(self.__prefix + key, str(door[key]))

        # Build the components

        components = payload["components"]
        payload = []

        for component in components:
            name = component["name"]
            doors = component["payload"]

            # The component has its transport

            transport = {
                "name": name,
                "payload": ""
            }

            for door in doors:
                try:
                    with open(f"src/templates/components/{name}.html", "r") as f:
                        base = f.read()
                except:
                    raise NameError(f"Error reading component {name}")

                for key in door:
                    base = base.replace(self.__prefix + key, str(door[key]))
            
                transport["payload"] += base
            payload.append(transport)
        
        # Build the template with the components

        for x in payload:
            template = template.replace("component" + self.__prefix + x["name"], str(x["payload"]))

        return template

    def send(self, subject: str, payload: dict) -> None:
        if self.__switch == "ON":
            message = MIMEMultipart()
            message["Subject"] = subject
            message["From"] = self.__from
            message["To"] = ",".join(self.__to)

            template = self.__template(payload=payload)

            message.attach(MIMEText(template, "html"))
            smtp = self.__connect()

            try:
                smtp.sendmail(self.__from, self.__to, message.as_string())
            except:
                raise NameError("Error sending emails")

            smtp.quit()
            print("\nEmails sent")
        else:
            print("\nSending emails is off")
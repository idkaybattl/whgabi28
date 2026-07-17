import csv
import os
import random
import sys
import time
from email.mime.text import MIMEText
from smtplib import (
    SMTP_SSL as SMTP,  # this invokes the secure SMTP protocol (port 465, uses SSL)
)
from textwrap import dedent

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand
from django.core.validators import validate_email

User = get_user_model()
TEXT_SUBTYPE = "plain"
WEBSITE_DOMAIN = "whgabi28.de"


class Command(BaseCommand):
    help = "sends emails to users created with 'import_student_accounts' via its .csv output file"

    def add_arguments(self, parser):
        parser.add_argument("-f", "--filepath", type=str, help="path to .csv file")

    def handle(self, *args, **kwargs):
        filepath = kwargs["filepath"]

        if not filepath:
            raise Exception("No file path provided.")

        if not filepath.endswith(".csv"):
            raise Exception("Invalid file type. Only .csv files are allowed.")

        if not os.path.exists(filepath):
            raise Exception("File does not exist")

        with open(filepath, newline="", encoding="utf-8") as infile:
            reader = csv.DictReader(infile)
            rows = list(reader)

            # check if data is valid

            # check required columns are present
            required_columns = {
                "firstname",
                "lastname",
                "email",
                "username",
                "password",
            }
            if reader.fieldnames is None:
                raise ValueError("CSV is missing a header row")

            missing = required_columns - set(reader.fieldnames)
            if missing:
                raise ValueError(f"Missing columns in CSV: {missing}")

            # accumulate all errors
            errors: list[str] = []
            for row in rows:
                # email
                try:
                    validate_email(row["email"])
                except ValidationError as e:
                    errors.append(f"{row}: {e}")
                    continue

            if len(errors) > 0:
                print("Errors found in CSV file. Please correct them and try again.")
                print("Errors: ")
                for error in errors:
                    print(error)
                return

            # create users
            # only so that lsp doesnt complain
            if reader.fieldnames is None:
                raise ValueError("CSV must have headers")

            # getting mail account data:
            smtp_server = input("SMTP Server: ")
            sender = input("Sender: ")

            username = input("Username: ")
            password = input("Password: ")

            for row in rows:
                subject = f"Abi Verwaltungswebsite Anmeldedaten für: {row['firstname']} {row['lastname']}"
                content = dedent(f"""\
                Hi,
                unter {WEBSITE_DOMAIN} findest du eine App zur Verwaltung unseres Abijahrgangs.
                Einerseits wird darüber das zukünftige Punktesystem für den Abiball laufen, andererseits könnten dort auch z.B. Abstimmungen für das Abimotto oder weiteres stattfinden.
                Wenn Aktionen (insbesondere welche mit denen Geld für die Abikasse verdient werden soll) stattfinden, wie beispielsweise ein Waffelverkauf, sollte dieser dort eingetragen werden.

                Deine Anmeldedaten sind:
                    Nutzername (wie auf IServ): {row["username"]}
                    Passwort (vorübergehend):  {row["password"]}

                Ich werde über die Ferien vermutlich noch ein paar Sachen hinzufügen, aber auch danach bei Problemen, oder Featurevorschlägen sehr gerne bei mir melden.

                Viele Grüße
                Moritz
                """)

                try:
                    msg = MIMEText(content, TEXT_SUBTYPE)
                    msg["Subject"] = subject
                    msg["From"] = (
                        sender  # some SMTP servers will do this automatically, not all
                    )

                    conn = SMTP(smtp_server)
                    conn.set_debuglevel(False)
                    conn.login(username, password)
                    try:
                        conn.sendmail(sender, row["email"], msg.as_string())
                    finally:
                        conn.quit()

                except:
                    sys.exit(
                        "mail failed; %s" % "CUSTOM_ERROR"
                    )  # give an error message

                time.sleep(random.uniform(1.0, 2.5))
                print(f"sent email to {row['username']}")

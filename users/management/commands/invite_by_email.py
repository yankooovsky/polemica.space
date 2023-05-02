import logging
from datetime import datetime, timedelta

from django.core.management import BaseCommand

from notifications.email.invites import send_mass_email
from users.models.user import User

log = logging.getLogger(__name__)

EMAILS_LIMIT = 10


class Command(BaseCommand):
    help = "Send invite by email"

    def add_arguments(self, parser):
        parser.add_argument("--production", type=bool, required=False, default=False)

    def handle(self, *args, **options):
        emails_filename = "/app/gdpr/downloads/polemica_users_emails.csv"
        sended_filename = "/app/gdpr/downloads/polemica_users_emails_sended.csv"

        with open(emails_filename, "r") as f:
            lines = f.readlines()
            emails = [line.strip().split(";")[1] for line in lines[1:]]

        try:
            with open(sended_filename, "r") as f:
                lines = f.readlines()
                sended = {line.strip() for line in lines}
        except FileNotFoundError:
            sended = set()

        count = 0
        for email in emails:
            if email in sended:
                continue

            count += 1
            if count > EMAILS_LIMIT:
                break

            sended.add(email)

            with open(sended_filename, "w") as f:
                f.write("\n".join(sended))

            if not options.get("production"):
                self.stdout.write(f"Try to send email to {email}...")
                continue

            self.stdout.write(f"Sending email to {email}...")

            days = 90
            now = datetime.utcnow()
            user, is_created = User.objects.get_or_create(
                email=email,
                defaults=dict(
                    membership_platform_type=User.MEMBERSHIP_PLATFORM_DIRECT,
                    full_name=email[:email.find("@")],
                    membership_started_at=now,
                    membership_expires_at=now + timedelta(days=days),
                    created_at=now,
                    updated_at=now,
                    moderation_status=User.MODERATION_STATUS_INTRO,
                ),
            )
            try:
                print(send_mass_email(user))
            except Exception as e:
                print(e)

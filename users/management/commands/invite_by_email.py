import logging
from datetime import datetime, timedelta

from django.core.management import BaseCommand

from notifications.email.invites import send_mass_email
from users.models.user import User

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Send invite by email"

    def add_arguments(self, parser):
        parser.add_argument("--email", type=str, required=False)

    def handle(self, *args, **options):
        email = options["email"]

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
        send_mass_email(user)

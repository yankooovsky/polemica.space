from django.template import loader

from notifications.email.sender import send_club_email
from users.models.user import User


def send_invited_email(from_user: User, to_user: User):
    invite_template = loader.get_template("emails/invited.html")
    send_club_email(
        recipient=to_user.email,
        subject=f"🚀 Вас пригласили в Клуб",
        html=invite_template.render({"from_user": from_user, "to_user": to_user}),
        tags=["invited"]
    )


def send_invite_renewed_email(from_user: User, to_user: User):
    invite_template = loader.get_template("emails/invite_renewed.html")
    send_club_email(
        recipient=to_user.email,
        subject=f"🚀 Вам оплатили аккаунт в Клубе",
        html=invite_template.render({"from_user": from_user, "to_user": to_user}),
        tags=["invited"]
    )


def send_invite_confirmation(from_user: User, to_user: User):
    invite_template = loader.get_template("emails/invite_confirm.html")
    send_club_email(
        recipient=from_user.email,
        subject=f"👍 Вы оплатили для '{to_user.email}' аккаунт в Клубе",
        html=invite_template.render({"from_user": from_user, "to_user": to_user}),
        tags=["invited"]
    )


def send_mass_email(to_user: User):
    invite_template = loader.get_template("emails/mass-mailing/invite45days.html")
    send_club_email(
        recipient=to_user.email,
        subject=f"🚀 Вас пригласили в Polemica Community",
        html=invite_template.render({"to_user": to_user}),
        tags=["invited"]
    )

"""event handlers for announcmeent.engine package"""

from plone import api
from email.message import EmailMessage
from announcement.engine import _

from .contrib.mail import send_mail


def noitifyAboutPublishReject(announcement, event):
    """
    Notifies announcement creator about publish/reject transition
    """
    transition_id = event.action
    lang = api.portal.get_registry_record('plone.default_language')
    translator = api.portal.get_tool('translation_service')

    #  data checks for email sending
    if transition_id not in (_('publish'), _('reject')):
        return

    owner = api.user.get(
        userid=announcement.getOwner().getId()
        )
    
    if not owner:
        return
    
    recipient = owner.getProperty('email')

    if not recipient:
        return

    # compose message contents
    subject = f"""{announcement.title} ::> {translator.translate(
            _(transition_id), target_language=lang, default=f"{transition_id + 'ed'}"
        )}"""

    body = api.content.get_view(
            name="announcement_transition_template",
            context=announcement,
            request=announcement.REQUEST,
        )(announcement=announcement, action=transition_id)

    # compose smtp message
    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = api.portal.get_registry_record('plone.email_from_name')
    msg["To"] = recipient

    msg.replace_header("Content-Type", 'text/html; charset="utf-8"')

    send_mail(msg, encoding="utf-8")


def notifyAboutAnnouncementCreation(announcement, event):
    """
    Event handler notifies about new announcement
    creation on email indcated in parent annoucement_category
    """
    announcement_category = announcement.getParentNode()

    if not announcement_category:
        return False

    recipient = announcement_category.notification_email

    if not recipient:
        return False

    subject = "New announcement"
    message = f"New announcement was created, is available by: {announcement.absolute_url()}"

    api.portal.send_email(
        recipient=recipient,
        sender=api.portal.get_registry_record('plone.email_from_name'),
        subject=subject,
        body=message
    )

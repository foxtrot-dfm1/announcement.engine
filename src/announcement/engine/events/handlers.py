"""event handlers for announcmeent.engine package"""

from plone import api
from announcement.engine import _

ANNOUNCEMENT_TRANSITION_MSG_MAP = {
    _('publish'): _(
        'announcement_publish_message',
        default="Announcement was published, see"
        ),
    _('reject'): _(
        'announcement_reject_message',
        default="Announcement was rejected, see"
        ) 
}

def noitifyAboutPublishReject(announcement, event):
    """
    Notifies announcement creator about publish/reject transition
    """
    transition_id = event.action
    lang = api.portal.get_registry_record('plone.default_language')
    translator = api.portal.get_tool('translation_service')

    if transition_id not in (ANNOUNCEMENT_TRANSITION_MSG_MAP.keys()):
        return False

    recipient = api.user.get(
        userid=announcement.getOwner().getId()
        ).getProperty('email')
    
    if not recipient:
        return False

    # If u have any idea how to refactor this, text me <kysilroman99@gmail.com> ☃
    subject = f"""{announcement.title} ::> {translator.translate(
            _(transition_id), target_language=lang, default=f"{transition_id + 'ed'}"
        )}"""

    message = f"""{translator.translate(
            ANNOUNCEMENT_TRANSITION_MSG_MAP[transition_id],
            target_language=lang
        )} : {announcement.absolute_url()}"""

    api.portal.send_email(
        recipient=recipient,
        sender=api.portal.get_registry_record('plone.email_from_name'),
        subject=subject,
        body=message
    )

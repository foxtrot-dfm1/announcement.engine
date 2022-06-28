"""event handlers for announcmeent.engine package"""

from plone import api


def noitifyAboutPublishReject(announcement, event):
    """
    Notifies announcement creator about publish/reject transition
    """
    transition_id = event.action

    if transition_id not in ('publish', 'reject'):
        return False

    recipient = api.user.get(
        userid=announcement.getOwner().getId()
        ).getProperty('email')
    
    if not recipient:
        return False

    subject = f"{announcement.title} ::> {transition_id + 'ed'}"
    message = f"Announcment was {transition_id + 'ed'}, see: {announcement.absolute_url()}"

    api.portal.send_email(
        recipient=recipient,
        sender=api.portal.get_registry_record('plone.email_from_name'),
        subject=subject,
        body=message
    )

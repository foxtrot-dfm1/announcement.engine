"""Announcement Category C.T."""
from plone.schema import Email 
from plone.supermodel import model
from zope.interface import implementer
from plone.dexterity.content import Container


class IAnnouncementCategory(model.Schema):
    """Announcement Category C.T. Interface"""

    notification_email = Email(
        title="Notification email",
        required=False
    )

@implementer(IAnnouncementCategory)
class AnnouncementCategory(Container):
    """Announcement instance class"""

"""Announcement Category C.T."""
from plone.schema import Email 
from plone.supermodel import model
from zope.interface import implementer
from plone.dexterity.content import Container
from announcement.engine import _

class IAnnouncementCategory(model.Schema):
    """Announcement Category C.T. Interface"""

    notification_email = Email(
        title=_("Notification email"),
        required=False
    )

@implementer(IAnnouncementCategory)
class AnnouncementCategory(Container):
    """Announcement instance class"""

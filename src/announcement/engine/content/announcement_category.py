"""Announcement Category C.T."""
from plone.supermodel import model
from zope.interface import implementer
from plone.dexterity.content import Container


class IAnnouncementCategory(model.Schema):
    """Announcement Category C.T. Interface"""

@implementer(IAnnouncementCategory)
class AnnouncementCategory(Container):
    """Announcement instance class"""

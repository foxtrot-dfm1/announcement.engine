"""Announcement Category C.T."""
from zope import schema
from zope.interface import implementer
from plone.supermodel import model
from plone.namedfile.field import NamedBlobImage
from plone.app.textfield import RichText
from plone.dexterity.content import Container


class IAnnouncementCategory(model.Schema):
    """Announcement Category C.T. Interface"""

@implementer(IAnnouncementCategory)
class AnnouncementCategory(Container):
    """Announcement instance class"""

"""Announcement C.T."""
from zope import schema
from zope.interface import implementer
from plone.supermodel import model
from plone.namedfile.field import NamedBlobImage
from plone.app.textfield import RichText
from plone.dexterity.content import Container

class IAnnouncementArea(model.Schema):
    """Announcement C.T. Interface"""

@implementer(IAnnouncementArea)
class AnnouncementArea(Container):
    """Announcement instance class"""

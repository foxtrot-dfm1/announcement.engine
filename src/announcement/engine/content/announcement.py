"""Announcement C.T."""
from zope import schema
from zope.interface import implementer
from plone.supermodel import model
from plone.dexterity.content import Container

class IAnnouncement(model.Schema):
    """Announcement C.T. Interface"""

    external_link = schema.URI(
        title="External link",
        required=False
    )

@implementer(IAnnouncement)
class Announcement(Container):
    """Announcement instance class"""

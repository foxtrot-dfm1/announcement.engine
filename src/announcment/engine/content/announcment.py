"""Announcment C.T."""
from zope import schema
from zope.interface import implementer
from plone.supermodel import model
from plone.namedfile.field import NamedBlobImage
from plone.app.textfield import RichText
from plone.dexterity.content import Container

class IAnnouncment(model.Schema):
    """Announcment C.T. Interface"""

    title = schema.TextLine(
        title="Title",
    )

    description = schema.Text(
        title="Description",
        max_length=512
    )

    external_link = schema.URI(
        title="External link",
        required=False
    )

    image = NamedBlobImage(
        title="Image",
        required=False
    )

    image_dscription = schema.Text(
        title="Image description",
        required=False
    )

    text = RichText(
        title="Extended description of announcment",
        max_length=1000,
        required=False
    )

@implementer(IAnnouncment)
class Announcment(Container):
    """Announcment instance class"""

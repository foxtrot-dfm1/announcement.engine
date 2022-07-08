"""Helpers for mail handling"""
import logging
from plone import api

def send_mail(msg, encoding):
    """Mail sending tool"""
    try:
        api.portal.get_tool(name="MailHost").send(msg, charset=encoding)
    except Exception as e:
        log = logging.getLogger("MailDataManager")
        log.exception(e)

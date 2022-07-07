#Pythonic libraries
import unittest
from email import message_from_string

#Plone
from plone import api
from plone.registry.interfaces import IRegistry
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from zope.component import getUtility

from Acquisition import aq_base
from zope.component import getSiteManager
from Products.CMFPlone.tests.utils import MockMailHost
from Products.MailHost.interfaces import IMailHost

import transaction

from announcement.engine.testing import \
    ANNOUNCEMEMNT_ENGINE_FUNCTIONAL_TESTING


class TestNotifyAboutAnnouncementCreation(unittest.TestCase):
    layer = ANNOUNCEMEMNT_ENGINE_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.portal._original_MailHost = self.portal.MailHost
        self.portal.MailHost = mailhost = MockMailHost('MailHost')

        self.registry = getUtility(IRegistry)
        self.registry["plone.email_from_address"] = "site_addr@plone.com"
        self.registry["plone.email_from_name"] = "Plone test site"

        sm = getSiteManager(context=self.portal)
        sm.unregisterUtility(provided=IMailHost)
        sm.registerUtility(mailhost, provided=IMailHost)

        transaction.commit()

        setRoles(self.portal, TEST_USER_ID, ['Contributor'])

    def tearDown(self):
        self.portal.MailHost = self.portal._original_MailHost

        sm = getSiteManager(context=self.portal)

        sm.unregisterUtility(provided=IMailHost)
        sm.registerUtility(aq_base(self.portal._original_MailHost),
                           provided=IMailHost)

    def test_email_not_sent_if_no_category_email(self):
        category = api.content.create(
            self.portal, type='announcement_category', id='category_n_email'
        )

        api.content.create(
            container=category,
            type='announcement',
            id='test'
        )

        self.assertEqual(len(self.portal.MailHost.messages), 0)
    
    def test_email_not_sent_if_no_category_parent(self):
        api.content.create(
            container=self.portal,
            type='announcement',
            id='test'
        )

        self.assertEqual(len(self.portal.MailHost.messages), 0)

    def test_positive(self):
        category_with_email = api.content.create(
            self.portal, type='announcement_category',
            id='category_email', notification_email="test_notify@test.com"
        )

        api.content.create(
            container=category_with_email,
            type='announcement',
            title='test'
        )

        self.assertEqual(len(self.portal.MailHost.messages), 1)

        message = message_from_string(
            self.portal.MailHost.messages[0].decode('utf-8')
            )

        self.assertEqual(message['To'], category_with_email.notification_email)
        self.assertEqual(message['From'], self.registry["plone.email_from_address"])
        self.assertEqual(message['Content-Type'], 'text/html; charset="utf-8"')
        self.assertEqual(message['Subject'], 'New announcement')

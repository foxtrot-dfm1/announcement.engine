#Pythonic libraries
import unittest

#Plone
from plone import api
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from announcement.engine.testing import \
    ANNOUNCEMEMNT_ENGINE_INTEGRATION_TESTING


class TestAnnouncementCreateView(unittest.TestCase):
    layer = ANNOUNCEMEMNT_ENGINE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.test_item = api.content.create(self.portal, 'announcement',
                                            title='announcement_test')

    def test_view_contains_text(self):
        view = api.content.get_view(
            name='announcement_transition_template',
            context=self.test_item,
            request=self.request
        )

        transitions = ('publish', 'reject')

        for transition in transitions:
            self.assertIn(transition + 'ed',
                          view(announcement=self.test_item, action=transition))
            self.assertIn(self.test_item.absolute_url(), 
                          view(announcement=self.test_item, action=transition))
from announcement.engine.content.announcement import IAnnouncement  # NOQA E501
from announcement.engine.testing import ANNOUNCEMENT_ENGINE_INTEGRATION_TESTING  # noqa
from plone import api
from plone.app.testing import setRoles, TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject, queryUtility

import unittest


class TestAnnouncementIntegrationTest(unittest.TestCase):

    layer = ANNOUNCEMENT_ENGINE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            'announcement_category',
            self.portal,
            'parent_container',
            title='Parent container',
        )
        self.parent = self.portal[parent_id]

    def test_ct_announcement_a_schema(self):
        fti = queryUtility(IDexterityFTI, name='announcement')
        schema = fti.lookupSchema()
        self.assertEqual(IAnnouncement, schema)

    def test_ct_announcement_a_fti(self):
        fti = queryUtility(IDexterityFTI, name='announcement')
        self.assertTrue(fti)

    def test_ct_announcement_a_factory(self):
        fti = queryUtility(IDexterityFTI, name='announcement')
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            IAnnouncement.providedBy(obj),
            u'IAnnouncement not provided by {0}!'.format(
                obj,
            ),
        )

    def test_ct_annoucement_a_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.parent,
            type='announcement',
            id='announcement',
        )

        self.assertTrue(
            IAnnouncement.providedBy(obj),
            u'IAnnouncement not provided by {0}!'.format(
                obj.id,
            ),
        )

        parent = obj.__parent__
        self.assertIn('announcement', parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn('announcement', parent.objectIds())

    def test_ct_annoucement_a_globally_not_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='announcement')
        self.assertFalse(
            fti.global_allow,
            u'{0} is globally addable!'.format(fti.id)
        )
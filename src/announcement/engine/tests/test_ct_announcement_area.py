# -*- coding: utf-8 -*-
from announcement.engine.content.announcement_area import IAnnouncementArea  # NOQA E501
from announcement.engine.testing import ANNOUNCEMENT_ENGINE_INTEGRATION_TESTING  # noqa
from plone import api
from plone.api.exc import InvalidParameterError
from plone.app.testing import setRoles, TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject, queryUtility
from zExceptions.unauthorized import Unauthorized

import unittest


class TestAnnouncementAreaIntegrationTest(unittest.TestCase):

    layer = ANNOUNCEMENT_ENGINE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.parent = self.portal

    def test_ct_announcement_area_schema(self):
        fti = queryUtility(IDexterityFTI, name='announcement_area')
        schema = fti.lookupSchema()
        self.assertEqual(IAnnouncementArea, schema)

    def test_ct_announcement_area_fti(self):
        fti = queryUtility(IDexterityFTI, name='announcement_area')
        self.assertTrue(fti)

    def test_ct_announcement_area_factory(self):
        fti = queryUtility(IDexterityFTI, name='announcement_area')
        factory = fti.factory
        obj = createObject(factory)
        #import pdb; pdb.set_trace()
        self.assertTrue(
            IAnnouncementArea.providedBy(obj),
            u'IAnnouncementArea not provided by {0}!'.format(
                obj,
            ),
        )

    def test_ct_announcement_category_cant_add_contributor(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        
        with self.assertRaises(Unauthorized):
            api.content.create(
                container=self.parent,
                type='announcement_area',
                id='announcement_area',
            )

    def test_ct_announcement_area_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        obj = api.content.create(
            container=self.portal,
            type='announcement_area',
            id='announcement_area',
        )

        self.assertTrue(
            IAnnouncementArea.providedBy(obj),
            u'IAnnouncementArea not provided by {0}!'.format(
                obj.id,
            ),
        )

        parent = obj.__parent__
        self.assertIn('announcement_area', parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn('announcement_area', parent.objectIds())

    def test_ct_announcement_area_globally_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        fti = queryUtility(IDexterityFTI, name='announcement_area')
        self.assertTrue(
            fti.global_allow,
            u'{0} is not globally addable!'.format(fti.id)
        )

    def test_ct_announcement_area_filter_content_type_true(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        fti = queryUtility(IDexterityFTI, name='announcement_area')
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            fti.id,
            self.portal,
            'announcement_area_id',
            title='announcement_area container',
        )
        self.parent = self.portal[parent_id]
        with self.assertRaises(InvalidParameterError):
            api.content.create(
                container=self.parent,
                type='Document',
                title='My Content',
            )
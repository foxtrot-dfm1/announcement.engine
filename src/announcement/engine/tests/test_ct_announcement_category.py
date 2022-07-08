# -*- coding: utf-8 -*-
from announcement.engine.content.announcement_category import (
    IAnnouncementCategory  # NOQA E501,
)
from announcement.engine.testing import ANNOUNCEMENT_ENGINE_INTEGRATION_TESTING  # noqa
from plone import api
from plone.api.exc import InvalidParameterError
from plone.app.testing import setRoles, TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject, queryUtility

import unittest


class TestAnnouncementCategoryIntegrationTest(unittest.TestCase):

    layer = ANNOUNCEMENT_ENGINE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            'announcement_area',
            self.portal,
            'parent_container',
            title='Parent container',
        )
        self.parent = self.portal[parent_id]

    def test_ct_announcement_category_schema(self):
        fti = queryUtility(IDexterityFTI, name='announcement_category')
        schema = fti.lookupSchema()
        self.assertEqual(IAnnouncementCategory, schema)

    def test_ct_announcement_category_fti(self):
        fti = queryUtility(IDexterityFTI, name='announcement_category')
        self.assertTrue(fti)

    def test_ct_announcement_category_factory(self):
        fti = queryUtility(IDexterityFTI, name='announcement_category')
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            IAnnouncementCategory.providedBy(obj),
            u'IAnnouncementCategory not provided by {0}!'.format(
                obj,
            ),
        )

    def test_ct_announcement_category_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        obj = api.content.create(
            container=self.parent,
            type='announcement_category',
            id='announcement_category',
        )

        self.assertTrue(
            IAnnouncementCategory.providedBy(obj),
            u'IAnnouncementCategory not provided by {0}!'.format(
                obj.id,
            ),
        )

        parent = obj.__parent__
        self.assertIn('announcement_category', parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn('announcement_category', parent.objectIds())

    def test_ct_announcement_category_globally_not_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        fti = queryUtility(IDexterityFTI, name='announcement_category')
        self.assertFalse(
            fti.global_allow,
            u'{0} is globally addable!'.format(fti.id)
        )

    def test_ct_announcement_category_filter_content_type_true(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        fti = queryUtility(IDexterityFTI, name='announcement_category')
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            fti.id,
            self.portal,
            'announcement_category_id',
            title='announcement_category container',
        )
        self.parent = self.portal[parent_id]
        with self.assertRaises(InvalidParameterError):
            api.content.create(
                container=self.parent,
                type='Document',
                title='My Content',
            )
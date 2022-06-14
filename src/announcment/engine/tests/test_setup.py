# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from announcment.engine.testing import (
    ANNOUNCMENT_ENGINE_INTEGRATION_TESTING  # noqa: E501,
)
from plone import api
from plone.app.testing import setRoles, TEST_USER_ID

import unittest


try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    get_installer = None


class TestSetup(unittest.TestCase):
    """Test that announcment.engine is properly installed."""

    layer = ANNOUNCMENT_ENGINE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if announcment.engine is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'announcment.engine'))

    def test_browserlayer(self):
        """Test that IAnnouncmentEngineLayer is registered."""
        from announcment.engine.interfaces import (
            IAnnouncmentEngineLayer)
        from plone.browserlayer import utils
        self.assertIn(
            IAnnouncmentEngineLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = ANNOUNCMENT_ENGINE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstallProducts(['announcment.engine'])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if announcment.engine is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'announcment.engine'))

    def test_browserlayer_removed(self):
        """Test that IAnnouncmentEngineLayer is removed."""
        from announcment.engine.interfaces import \
            IAnnouncmentEngineLayer
        from plone.browserlayer import utils
        self.assertNotIn(
            IAnnouncmentEngineLayer,
            utils.registered_layers())

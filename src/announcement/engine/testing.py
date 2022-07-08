# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import (
    applyProfile,
    FunctionalTesting,
    IntegrationTesting,
    PloneSandboxLayer,
)
from plone.testing import z2

import announcement.engine


class AnnouncementEngineLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=announcement.engine)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'announcement.engine:default')


ANNOUNCEMENT_ENGINE_FIXTURE = AnnouncementEngineLayer()


ANNOUNCEMENT_ENGINE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(ANNOUNCEMENT_ENGINE_FIXTURE,),
    name='AnnouncementEngineLayer:IntegrationTesting',
)


ANNOUNCEMENT_ENGINE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(ANNOUNCEMENT_ENGINE_FIXTURE,),
    name='AnnouncementEngineLayer:FunctionalTesting',
)


ANNOUNCEMENT_ENGINE_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        ANNOUNCEMENT_ENGINE_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='AnnouncementEngineLayer:AcceptanceTesting',
)

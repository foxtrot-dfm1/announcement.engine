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

import announcment.engine


class AnnouncmentEngineLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=announcment.engine)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'announcment.engine:default')


ANNOUNCMENT_ENGINE_FIXTURE = AnnouncmentEngineLayer()


ANNOUNCMENT_ENGINE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(ANNOUNCMENT_ENGINE_FIXTURE,),
    name='AnnouncmentEngineLayer:IntegrationTesting',
)


ANNOUNCMENT_ENGINE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(ANNOUNCMENT_ENGINE_FIXTURE,),
    name='AnnouncmentEngineLayer:FunctionalTesting',
)


ANNOUNCMENT_ENGINE_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        ANNOUNCMENT_ENGINE_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='AnnouncmentEngineLayer:AcceptanceTesting',
)

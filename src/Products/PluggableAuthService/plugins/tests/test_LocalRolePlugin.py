##############################################################################
#
# Copyright (c) 2001 Zope Foundation and Contributors
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this
# distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
import unittest

from Acquisition import Implicit
from OFS.ObjectManager import ObjectManager

from ...tests.conformance import IRolesPlugin_conformance


class FauxObject(Implicit):

    def __init__(self, id=None):
        self._id = id


class FauxContainer(FauxObject, ObjectManager):
    pass


class FauxRoot(FauxContainer):

    isTopLevelPrincipiaApplicationObject = 1

    def getPhysicalRoot(self):
        return self


class FauxUser(Implicit):

    def __init__(self, id, name=None, roles={}):
        self._id = id
        self._name = name
        self._roles = roles

    def getId(self):
        return self._id


class LocalRolePluginTestCase(unittest.TestCase, IRolesPlugin_conformance):

    def _getTargetClass(self):
        from ...plugins.LocalRolePlugin import LocalRolePlugin

        return LocalRolePlugin

    def _makeOne(self, id='test', *args, **kw):
        return self._getTargetClass()(id, *args, **kw)

    def _makeTree(self):
        rc = FauxObject('rc')
        root = FauxRoot('root').__of__(rc)
        folder = FauxContainer('folder').__of__(root)
        object = FauxObject('object').__of__(folder)

        return rc, root, folder, object

    def test_no_local_roles(self):
        rc, root, folder, object = self._makeTree()

        lrp = self._makeOne('no_roles').__of__(root)

        user = FauxUser('loser').__of__(root)

        self.assertEqual(lrp.getRolesForPrincipal(user), None)

    def test_some_local_roles(self):
        rc, root, folder, object = self._makeTree()

        root.__ac_local_roles__ = {'some_manager': ['Manager']}

        lrp = self._makeOne('roles').__of__(root)

        user = FauxUser('some_manager').__of__(root)

        self.assertEqual(lrp.getRolesForPrincipal(user), ['Manager'])

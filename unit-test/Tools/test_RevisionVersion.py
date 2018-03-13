####################################################################################################
#
# Babel - An Electronic Document Management System
# Copyright (C) 2014 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
####################################################################################################

####################################################################################################

import unittest

####################################################################################################

from Babel.Tools.RevisionVersion import RevisionVersion

####################################################################################################

class TestRevisionVersion(unittest.TestCase):

    ##############################################

    def __init__(self, method_name):

        super(TestRevisionVersion, self).__init__(method_name)

    ##############################################

    def test(self):

        v0_str = 'v3.2.1'
        v0_tuple = (3, 2, 1)

        self.assertEqual(RevisionVersion(v0_str), RevisionVersion(v0_tuple))
        self.assertEqual(str(RevisionVersion(v0_str)), v0_str)

        self.assertTrue(RevisionVersion('v3.2.1') > RevisionVersion('v2.3.2'))
        self.assertTrue(RevisionVersion('v3.2.1') > RevisionVersion('v3.1.2'))
        self.assertTrue(RevisionVersion('v3.2.1') > RevisionVersion('v3.2.0'))

        self.assertTrue(RevisionVersion('v3.2.1') >= RevisionVersion('v2.3.2'))
        self.assertTrue(RevisionVersion('v3.2.1') >= RevisionVersion('v3.2.1'))
        self.assertTrue(RevisionVersion('v3.2.1') >= RevisionVersion('v3.1.2'))
        self.assertTrue(RevisionVersion('v3.2.1') >= RevisionVersion('v3.2.0'))
        self.assertFalse(RevisionVersion('v3.2.0') >= RevisionVersion('v3.2.1'))
        self.assertFalse(RevisionVersion('v3.2.1') >= RevisionVersion('v3.3.0'))

        self.assertTrue(RevisionVersion('v2.3.2') < RevisionVersion('v3.2.1'))
        self.assertTrue(RevisionVersion('v3.1.2') < RevisionVersion('v3.2.1'))
        self.assertTrue(RevisionVersion('v3.2.0') < RevisionVersion('v3.2.1'))

        self.assertTrue(RevisionVersion('v2.3.2') <= RevisionVersion('v3.2.1'))
        self.assertTrue(RevisionVersion('v3.2.1') <= RevisionVersion('v3.2.1'))
        self.assertTrue(RevisionVersion('v3.1.2') <= RevisionVersion('v3.2.1'))
        self.assertTrue(RevisionVersion('v3.2.0') <= RevisionVersion('v3.2.1'))
        self.assertFalse(RevisionVersion('v3.2.1') <= RevisionVersion('v3.2.0'))

####################################################################################################

if __name__ == '__main__':

    unittest.main()

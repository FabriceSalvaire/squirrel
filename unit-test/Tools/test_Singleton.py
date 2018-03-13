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

from Babel.Tools.Singleton import *

####################################################################################################

@singleton
class Foo(object):

    ##############################################

    def __init__(self, arg1, arg2, key1=1, key2=2):

        print("Foo: type self", type(self))
        print("Foo: type Foo", type(Foo))

        self.arg1 = arg1
        self.arg2 = arg2
        self.key1 = key1
        self.key2 = key2

####################################################################################################

class Bar(object):

    ##############################################

    def __init__(self, arg1, arg2, key1=1, key2=2):

        print("Bar: type self", type(self))
        print("Bar: type Bar", type(Bar))

        self.arg1 = arg1
        self.arg2 = arg2
        self.key1 = key1
        self.key2 = key2

####################################################################################################

print('Making Baz')
#@singleton
class Baz(Bar, metaclass=MetaSingleton):
#class Baz(monostate, Bar):

    def __init__(self, arg1, arg2, arg3, **kwargs):

        print("Baz: type self", type(self))
        print("Baz: type Baz", type(Baz))

        super(Baz, self).__init__(arg1, arg2, **kwargs)

        self.arg3 = arg3

####################################################################################################

class TestSingleton(unittest.TestCase):

    def test(self):

        print('\nFoo instantiation')
        foo = Foo(1, 2, key2=4)
        self.assertEqual(foo.arg1, 1)
        self.assertEqual(foo.arg2, 2)
        self.assertEqual(foo.key1, 1)
        self.assertEqual(foo.key2, 4)
        print('\nFoo instantiation')
        foo2 = Foo(10, 20, key1=30)
        self.assertIs(foo, foo2)
        self.assertEqual(foo.arg1, 1)

        print('\nBaz instantiation')
        baz = Baz(1, 2, 3, key2=4)
        self.assertEqual(baz.arg3, 3)
        print('\nBaz instantiation')
        baz2 = Baz(10, 20, 30, key1=30)
        self.assertIs(baz, baz2)
        self.assertEqual(baz.arg1, 1)

        print('\nBaz.__dict__', Baz.__dict__)
        print('\nbaz.__dict__', baz.__dict__)

####################################################################################################

if __name__ == '__main__':

    unittest.main()

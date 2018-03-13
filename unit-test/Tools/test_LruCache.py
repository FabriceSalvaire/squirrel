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

from Babel.Tools.LruCache import LruCache

####################################################################################################

def even(n):
    return n & 1 == 0

####################################################################################################

live_objects = {}

####################################################################################################

class Obj(object):

    def __init__(self, i):

        self.i = i
        live_objects[self.key()] = i

    def __lt__(self, other):
        return self.i < other.i

    def __del__(self):
        del live_objects[self.key()]
        print('Delete', str(self))

    def __str__(self):
        return 'Obj %u' % (self.i)

    def key(self):
        return self.i

    def size(self):
        return 1

####################################################################################################

class ObjMemory(Obj):

    def __init__(self, i):

        Obj.__init__(self, i)

        self.factor = 1

    def __str__(self):
        return 'Obj %u size = %u' % (self.i, self.size())

    def size(self):
        if even(self.i):
            return 10 * self.factor
        else:
            return 5 * self.factor

####################################################################################################

class TestLruCache(unittest.TestCase):

    ##############################################

    def test_history(self):

        print('\nTest History Mode')

        live_objects.clear()

        lru_cache = LruCache(constraint=5)

        for i in range(5):
            lru_cache.add(Obj(i))
        self.assertEqual(len(lru_cache), 5)
        print(lru_cache)

        obj = lru_cache.acquire(6)
        self.assertIsNone(obj)

        obj1 = lru_cache.acquire(1)
        print(lru_cache)
        self.assertEqual(obj1.key(), 1)
        self.assertEqual(lru_cache._younger._obj, obj1)
        self.assertEqual(lru_cache._younger._reference_counter, 1)

        obj3 = lru_cache.acquire(3)
        print(lru_cache)
        self.assertEqual(obj3.key(), 3)
        self.assertEqual(lru_cache._younger._obj, obj3)
        self.assertEqual(lru_cache._younger._reference_counter, 1)

        cache_element = lru_cache._cache_dict[1]
        obj11 = lru_cache.acquire(1)
        print(lru_cache)
        self.assertEqual(cache_element._reference_counter, 2)
        lru_cache.release(1)
        del obj11
        print(lru_cache)
        self.assertEqual(cache_element._reference_counter, 1)
        del cache_element

        for i in range(5, 10):
            lru_cache.add(Obj(i))
        print(lru_cache)
        self.assertEqual(len(lru_cache), 10)

        objs = {}
        for i in 9, 8, 7, 6:
            objs[i] = lru_cache.acquire(i)
        print(lru_cache)

        lru_cache.recycle()
        print(lru_cache)
        self.assertEqual(len(lru_cache), 6)
        for i in 0, 2, 4, 5:
            self.assertTrue(i not in live_objects)

        for i in 6, 7:
            lru_cache.release(i)
            del objs[i]
        print(lru_cache)
        lru_cache.recycle()
        print(lru_cache)
        self.assertEqual(len(lru_cache), 5)
        for i in 7,:
            self.assertTrue(i not in live_objects)

        print("Cleanup")
        print(objs)
        del objs
        del obj1
        del obj3
        lru_cache.reset()
        print(lru_cache)
        self.assertEqual(len(live_objects), 0)

    ##############################################

    def test_memory(self):

        print('\nTest Memory Mode')

        live_objects.clear()

        lru_cache = LruCache(constraint=50)

        for i in range(8):
            lru_cache.add(ObjMemory(i))
        self.assertEqual(len(lru_cache), 8)
        self.assertEqual(lru_cache.size(), 4*(5+10))
        print(lru_cache)

        lru_cache.recycle()
        print(lru_cache)
        self.assertEqual(len(lru_cache), 7)
        self.assertEqual(lru_cache.size(), lru_cache.constraint)
        for i in 0,:
            self.assertTrue(i not in live_objects)

####################################################################################################

if __name__ == '__main__':

    unittest.main()

####################################################################################################
# 
# Babel - A Bibliography Manager 
# Copyright (C) Salvaire Fabrice 2013 
# 
####################################################################################################

####################################################################################################

import unittest

####################################################################################################

from Babel.Tools.Container import Ring

####################################################################################################

class TestRing(unittest.TestCase):

    ##############################################

    def test_delete(self):

        ring = Ring(range(3), closed=True)

        self.assertEqual(ring.current_index, 0)
        self.assertEqual(ring.current_item, 0)

        ring.next()
        self.assertEqual(ring.current_index, 1)
        self.assertEqual(ring.current_item, 1)

        ring.next()
        self.assertEqual(ring.current_index, 2)
        self.assertEqual(ring.current_item, 2)

        ring.next()
        self.assertEqual(ring.current_index, 0)
        self.assertEqual(ring.current_item, 0)

        ring.previous()
        self.assertEqual(ring.current_index, 2)
        self.assertEqual(ring.current_item, 2)

        ring.previous()
        self.assertEqual(ring.current_index, 1)
        self.assertEqual(ring.current_item, 1)

        ring.previous()
        self.assertEqual(ring.current_index, 0)
        self.assertEqual(ring.current_item, 0)
        
        ring.delete(0)
        self.assertEqual(ring.current_index, 0)
        self.assertEqual(ring.current_item, 1)

        ring.delete(1)
        self.assertEqual(ring.current_index, 0)
        self.assertEqual(ring.current_item, 2)

        ring.delete(2)
        self.assertIsNone(ring.current_index)

        ring = Ring(range(3), closed=True)

        ring.delete(2)
        self.assertEqual(ring.current_index, 0)
        self.assertEqual(ring.current_item, 0)

        ring.next()
        ring.delete(0)
        self.assertEqual(ring.current_index, 0)
        self.assertEqual(ring.current_item, 1)

        ring = Ring(range(3), closed=True)

        ring.next()
        ring.next()
        ring.delete(2)
        self.assertEqual(ring.current_index, 0)
        self.assertEqual(ring.current_item, 0)
        
####################################################################################################

if __name__ == '__main__':

    unittest.main()

####################################################################################################
#
# End
#
####################################################################################################

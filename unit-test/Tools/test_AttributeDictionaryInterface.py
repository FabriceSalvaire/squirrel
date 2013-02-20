####################################################################################################
# 
# Babel - A Bibliography Manager 
# Copyright (C) Salvaire Fabrice 2013 
# 
####################################################################################################

####################################################################################################

import unittest

####################################################################################################

from Babel.Tools.AttributeDictionaryInterface import (ExtendedDictionaryInterface,
                                                      ReadOnlyAttributeDictionaryInterface,
                                                      AttributeDictionaryInterface,
                                                      AttributeDictionaryInterfaceDescriptor)

####################################################################################################

class TestExtendedDictionaryInterface(unittest.TestCase):

    ##############################################
        
    def test(self):

        extended_dictionary = ExtendedDictionaryInterface()

        extended_dictionary['key1'] = 1
        self.assertEqual(extended_dictionary['key1'], 1)
        self.assertEqual(extended_dictionary.key1, 1)

        extended_dictionary.key2 = 1
        # self.assertEqual(extended_dictionary['key2'], 1) # Fixme: ?
        self.assertEqual(extended_dictionary.key2, 1)

####################################################################################################

class ReadOnlyAttributeDictionaryInterfaceExample(ReadOnlyAttributeDictionaryInterface):

    ##############################################
    
    def __init__(self):

        super(ReadOnlyAttributeDictionaryInterfaceExample, self).__init__()

        for i in (1, 2):
            self._dictionary['attribute' + str(i)] = int(i)

####################################################################################################

class AttributeDictionaryInterfaceExample(AttributeDictionaryInterface):

    ##############################################
    
    def __init__(self):

        super(AttributeDictionaryInterfaceExample, self).__init__()

        for i in (1, 2):
            self._dictionary['attribute' + str(i)] = int(i)

####################################################################################################

class DescriptorExample(object):

    ##############################################
    
    def __init__(self, value):

        self.value = value

    ##############################################
    
    def get(self):

        return self.value

    ##############################################
    
    def set(self, value):

        self.value = value

####################################################################################################

class AttributeDictionaryInterfaceDescriptorExample(AttributeDictionaryInterfaceDescriptor):

    ##############################################
    
    def __init__(self):

        super(AttributeDictionaryInterfaceDescriptorExample, self).__init__()

        for i in (1, 2):
            self._dictionary['attribute' + str(i)] = DescriptorExample(i)


####################################################################################################

class TestReadOnlyBase(object):

    ##############################################
        
    def test_base(self):
        
        self.assertTrue('attribute1' in self.obj)
        self.assertEqual(self.obj.attribute1, 1)
        self.assertEqual(self.obj['attribute1'], 1)
        self.assertEqual(self.obj.attribute2, 2)
        with self.assertRaises(NotImplementedError):
            self.obj.attribute2 = 22

####################################################################################################

class TestReadOnlyAttributeDictionaryInterface(unittest.TestCase, TestReadOnlyBase):

    ##############################################
        
    def setUp(self):
        
        self.obj = ReadOnlyAttributeDictionaryInterfaceExample()

    ##############################################
        
    def test_iter(self):

        self.assertListEqual(sorted(list(iter(self.obj))), [1, 2])

####################################################################################################

class TestBase(object):

    ##############################################
        
    def test_base(self):
        
        self.assertTrue('attribute1' in self.obj)
        self.assertEqual(self.obj.attribute1, 1)
        self.assertEqual(self.obj['attribute1'], 1)
        self.assertEqual(self.obj.attribute2, 2)
        self.obj.attribute2 = 22
        self.assertEqual(self.obj.attribute2, 22)
        #self.obj.attribute3 = 3
        #self.assertEqual(self.obj.attribute3, 3)

####################################################################################################

class TestAttributeDictionaryInterface(unittest.TestCase, TestBase):

    ##############################################
        
    def setUp(self):
        
        self.obj = AttributeDictionaryInterfaceExample()

    ##############################################
        
    def test_iter(self):

        self.assertListEqual(sorted(list(iter(self.obj))), [1, 2])

####################################################################################################

class TestAttributeDictionaryInterfaceDescriptor(unittest.TestCase, TestBase):

    ##############################################
        
    def setUp(self):
        
        self.obj = AttributeDictionaryInterfaceDescriptorExample()

    ##############################################
        
    def test_iter(self):

        self.assertListEqual(sorted([x.get() for x in iter(self.obj)]), [1, 2])

####################################################################################################

if __name__ == '__main__':

    unittest.main()

####################################################################################################
#
# End
#
####################################################################################################

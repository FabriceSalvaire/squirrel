####################################################################################################
# 
# Babel - A Bibliography Manager 
# Copyright (C) Salvaire Fabrice 2013 
# 
####################################################################################################

####################################################################################################
#
#                                              Audit
#
# - 22/03/2013 Fabrice
#   read only
#
####################################################################################################

####################################################################################################

class ExtendedDictionaryInterface(dict):

    # Fixme: This class don't work as expected

    """ This class implements an extended dictionary interface.

    Example::

      extended_dictionary = ExtendedDictionaryInterface()

      extended_dictionary['key1'] = 1
      print extended_dictionary['key1']
      print extended_dictionary.key1

      # Unusal use case
      extended_dictionary.key2 = 1
      print extended_dictionary.key2
      # print extended_dictionary['key2'] # Not Implemented

    """

    ##############################################
    
    def __setitem__(self, key, value):

        if key not in self and key not in self.__dict__:
            dict.__setitem__(self, key, value)
            setattr(self, key, value)
        else:
            raise KeyError

####################################################################################################

class ReadOnlyAttributeDictionaryInterface(object):

    """ This class implements a read-only attribute and dictionary interface.

    Example::

      attribute_dictionary = ReadOnlyAttributeDictionaryInterface()

      attribute_dictionary._dictionary['a'] = 1
      attribute_dictionary._dictionary['b'] = 2

      print attribute_dictionary['a']
      print attribute_dictionary.b

      'a' in attribute_dictionary
      list(attribute_dictionary)
      # will return [1, 2]

    """

    ##############################################
    
    def __init__(self):

        object.__setattr__(self, '_dictionary', dict())

    ##############################################
    
    def __getattr__(self, name):

        """ Get the value from its name. """

        return self._dictionary[name]

    ##############################################

    __getitem__ = __getattr__

    ##############################################
    
    def __iter__(self):

        """ Iterate over the dictionary. """

        return self.iterkeys()

    ##############################################
    
    def iteritems(self):

        return self._dictionary.iteritems()

    ##############################################
    
    def iterkeys(self):

        return self._dictionary.iterkeys()

    ##############################################
    
    def itervalues(self):

        return self._dictionary.itervalues()

    ##############################################
    
    def __contains__(self, name):

        """ Test if *name* is in the dictionary. """

        return name in self._dictionary

    ##############################################
    
    def __setattr__(self, name, value):

        raise NotImplementedError

    ##############################################

    __setitem__ = __setattr__

####################################################################################################

class AttributeDictionaryInterface(ReadOnlyAttributeDictionaryInterface):

    """ This class implements an attribute and dictionary interface.

    Example::

      attribute_dictionary = AttributeDictionaryInterface()

      attribute_dictionary['a'] = 1
      print attribute_dictionary['a']

      attribute_dictionary.b = 2
      print attribute_dictionary.b

      'a' in attribute_dictionary
      list(attribute_dictionary)
      # will return [1, 2]

    """

    ##############################################
    
    def __setattr__(self, name, value):

        """ Set the value from its name. """

        self._dictionary[name] = value

    ##############################################

    __setitem__ = __setattr__

####################################################################################################

class AttributeDictionaryInterfaceDescriptor(AttributeDictionaryInterface):

    """ This class implements an attribute and dictionary interface using Descriptor.

    Example::

      class DescriptorExample(object):
          def __init__(self, value):
              self.value = value
          def get(self):
              return self.value
          def set(self, value):
              self.value = value
      
      attribute_dictionary = AttributeDictionaryInterfaceDescriptor()
      attribute_dictionary._dictionary['attribute1'] = DescriptorExample(1)
      
      attribute_dictionary['attribute1'] = 2
      print attribute_dictionary['attribute1']

      attribute_dictionary.attribute1 = 3
      print attribute_dictionary.attribute1

    """
    
    ##############################################
    
    def _get_descriptor(self, name):

        return self._dictionary[name]

    ##############################################
    
    def __getattr__(self, name):

        return self._get_descriptor(name).get()

    ##############################################
    
    def __setattr__(self, name, value):

        return self._get_descriptor(name).set(value)

    ##############################################

    __getitem__ = __getattr__
    __setitem__ = __setattr__

####################################################################################################
# 
# End
# 
####################################################################################################

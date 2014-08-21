####################################################################################################
# 
# Babel - A Bibliography Manager
# Copyright (C) Salvaire Fabrice 2014
# 
####################################################################################################

####################################################################################################

class Ring(object):

    ##############################################

    def __init__(self, iterable=(), closed=True):

        self._items = list(iterable)
        self._closed = bool(closed)

        if self._items:
            self._current_index = 0
        else:
            self._current_index = None

    ##############################################

    @property
    def closed(self):
        return self._closed

    ##############################################

    @closed.setter
    def closed(self, value):
        self._closed = bool(value)

    ##############################################

    def _last_index(self):
        return len(self._items) -1

    ##############################################

    @property
    def current_index(self):
        return self._current_index

    ##############################################

    @property
    def current_item(self):

        if self._current_index is not None:
            return self._items[self._current_index]
        else:
            raise IndexError

    ##############################################

    def next(self):

        if self._current_index is None:
            raise StopIteration()

        if self._current_index < self._last_index():
            self._current_index += 1
        elif self._closed:
            self._current_index = 0
        else:
            raise StopIteration()

        return self.current_item

    ##############################################

    def previous(self):

        if self._current_index is None:
            raise StopIteration()

        if self._current_index > 0:
            self._current_index -= 1
        elif self._closed:
            self._current_index = self._last_index()
        else:
            raise StopIteration()

        return self.current_item

    ##############################################

    def add(self, item):

        self._items.append(item)

        if self._current_index is None:
            self._current_index = 0

    ##############################################

    def delete(self, item):

        index = self._items.index(item)
        if index != -1:
            if len(self._items) == 1:
                self._current_index = None
            else:
                try:
                    self.next()
                except StopIteration:
                    self.previous()
            del self._items[index]
            return True
        else:
            return False

    ##############################################

    def sort(self, cmp=None, reverse=False):

        current_item = self.current_item
        self._items.sort(cmp=cmp, reverse=reverse)
        self._current_index = self._items.index(current_item)

####################################################################################################
# 
# End
# 
####################################################################################################

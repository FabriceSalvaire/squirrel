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

__all__ = [
    'Ring',
]

####################################################################################################

class EmptyRingError(Exception):
    pass

####################################################################################################

class Ring:

    """Implement a circular list."""

    ##############################################

    def __init__(self, iterable=(), closed=True):

        self._items = list(iterable)
        self._closed = bool(closed)

        if self._items:
            self._current_index = 0
        else:
            self._current_index = None

    ##############################################

    def _last_index(self):
        return len(self._items) -1

    ##############################################

    def __bool__(self):
        return bool(self._items)

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

    def __getitem__(self, slice_):
        return self._items[slice_]

    ##############################################

    @property
    def closed(self):
        return self._closed

    @closed.setter
    def closed(self, value):
        self._closed = bool(value)

    ##############################################

    @property
    def current_index(self):
        return self._current_index

    @current_index.setter
    def current_index(self, index):

        if 0 <= index <= self._last_index():
            self._current_index = index
        else:
            raise IndexError

    ##############################################

    @property
    def current_item(self):

        if self._current_index is not None:
            return self._items[self._current_index]
        else:
            raise EmptyRingError()

    ##############################################

    def __next__(self):

        if self._current_index is None:
            raise StopIteration()

        if self._current_index < self._last_index():
            self._current_index += 1
        elif self._closed:
            # self._current_index = (self._current_index + 1) % len(self._items)
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
            # self._current_index = (self._current_index - 1) % len(self._items)
            self._current_index = self._last_index()
        else:
            raise StopIteration()

        return self.current_item

    ##############################################

    def add(self, item):

        self._items.append(item) # at the trail

        if self._current_index is None:
            self._current_index = 0

    ##############################################

    def delete(self, item):

        return self.delete_index(self._items.index(item))

    ##############################################

    def delete_index(self, index):

        if index != -1:
            del self._items[index]
            if len(self._items):
                if index < self._current_index:
                    # self.previous()
                    self._current_index -= 1
                elif index == self._current_index and index == len(self._items):
                    if self._closed:
                        self._current_index = 0
                    else:
                        self._current_index = self._last_index()
                # elif index > self._current_index:
                #   nothing to do
            else:
                self._current_index = None
            return True
        else:
            return False

    ##############################################

    def sort(self, key=None, reverse=False):

        current_item = self.current_item
        self._items.sort(key=key, reverse=reverse)
        self._current_index = self._items.index(current_item)

    ##############################################

    def find(self, item):
        self._current_index = self._items.index(item)

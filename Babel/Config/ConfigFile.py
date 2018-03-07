####################################################################################################
#
# Babel - A Bibliography Manager
# Copyright (C) 2017 Fabrice Salvaire
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

import logging

from . import Config

####################################################################################################

class ConfigFile:

    _logger = logging.getLogger(__name__)

    ##############################################

    @classmethod
    def create(cls, args):

        template = '''
################################################################################
#
# Babel Configuration
#
################################################################################

document_root_path = '{0.document_root_path}'
'''

        path = cls.path()
        cls._logger.info('Create config file {}'.format(path))
        content = template.format(args).lstrip()
        Config.Path.make_user_directory()
        with open(path, 'w') as fh:
            fh.write(content)

    ##############################################

    def __init__(self):

        try:
            with open(self.path()) as fh:
                code = fh.read()
        except FileNotFoundError:
            raise NameError("You must first create a configuration file using the init command")

        namespace = {}
        exec(code, {}, namespace)
        for key, value in namespace.items():
            setattr(self, key, value)

    ##############################################

    @classmethod
    def path(cls):

        return  str(Config.Path.join_config_directory('config.py'))

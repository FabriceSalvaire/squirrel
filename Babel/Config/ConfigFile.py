####################################################################################################
#
# Babel - An Electronic Document Management System
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

import importlib.util as importlib_util
import logging

from . import DefaultConfig

####################################################################################################

class ConfigFile:

    _logger = logging.getLogger(__name__)

    ##############################################

    @classmethod
    def default_path(cls):
        return  str(DefaultConfig.Path.join_config_directory('config.py'))

    ##############################################

    @classmethod
    def create(cls, args):

        template = '''
################################################################################
#
# Babel Configuration
#
################################################################################

import Babel.Config.DefaultConfig as DefaultConfig

################################################################################

class Path(DefaultConfig.Path):

    DOCUMENT_ROOT_PATH = '{0.document_root_path}'
'''

        path = args.config or cls.default_path()
        cls._logger.info('Create config file {}'.format(path))
        content = template.format(args).lstrip()
        DefaultConfig.Path.make_user_directory()
        with open(path, 'w') as fh:
            fh.write(content)

    ##############################################

    def __init__(self, config_path=None):

        path = config_path or self.default_path()
        self._logger.info('Load config from {}'.format(path))

        try:
            with open(path) as fh:
                code = fh.read()
        except FileNotFoundError:
            raise NameError("You must first create a configuration file using the init command")

        # This code as issue with code in class definition ???
        # namespace = {'__file__': path}
        # # code_object = compile(code, path, 'exec')
        # exec(code, {}, namespace)
        # for key, value in namespace.items():
        #     setattr(self, key, value)

        spec = importlib_util.spec_from_file_location('Config', path)
        Config = importlib_util.module_from_spec(spec)
        spec.loader.exec_module(Config)

        for key in DefaultConfig.__all__:
            if hasattr(Config, key):
                src = Config
            else:
                src = DefaultConfig
            value = getattr(src, key)
            setattr(self, key, value)
            # resolve ConfigFile_ClassName in DefaultConfig
            setattr(DefaultConfig, 'ConfigFile_' + key, value)

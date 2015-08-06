# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

import fnmatch
import os
import sys
import logging

from six import iteritems

from .util import ensure_iterable

logger = logging.getLogger(__name__)


class AppLoader(object):
    """
    Import all subpackages/modules from the app's main directory.
    .. code-block::
        from flask_apploader import AppLoader

        def model_callback(modules):
            # Given /myapp/models/foo.py, outputs 'myapp.models.foo'
            for x in modules:
                print(x.__name__)

        app_loader = AppLoader(callbacks={'models': model_callback})

        def create_app():
            app = Flask(__name__)
            app_loader.init_app(app)
    """
    def __init__(self, app=None, groups=None, callbacks=None, load_on_init=None):
        """
        :param dict groups:
            Define groups of UNIX glob patterns (list or tuple) to be matched against module paths.
            Defaults to 'models' = '*model*' and 'views' = '*view*'.
        :param dict callbacks:
            Functions to call after groups are loaded.
            Callbacks will be passed a list of module objects that comprise the group.
            Keys should match those in `groups`.
        :param list load_on_init:
            Groups to be loaded during :meth:`init_app`.
            Defaults to ['models'].
        """
        self.groups = groups or {
            'models': ['*model*'],
            'views': ['*view*']}
        self.callbacks = callbacks or {}
        self.load_on_init = load_on_init or ['models']

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        self.find_modules()
        for x in self.load_on_init:
            self.load_group(x)

    def load_group(self, group):
        modules = []

        module_paths = self.grouped_module_paths.get(group, [])
        for module_path in module_paths:
            if module_path not in sys.modules:
                logger.debug("Importing module: %s", module_path)
                __import__(module_path)
            modules.append(sys.modules[module_path])

        self._execute_callbacks(group, modules)
        return modules

    def _execute_callbacks(self, group, *args, **kwargs):
        for callback in ensure_iterable(self.callbacks.get(group, [])):
            callback(*args, **kwargs)

    def find_modules(self):
        """
        Walk the app's dir and grab any modules that match the predefined patterns.
        """
        # set up a place to hold the modules, using the same keys as the patterns
        self.grouped_module_paths = dict((x, []) for x in self.groups.keys())

        for directory, dirnames, filenames in os.walk(self.app.root_path):
            # /path/to/myapp/foo --> myapp/foo
            rel_dir = os.path.relpath(directory,
                os.path.join(self.app.root_path, '../')).replace('\\', '/')

            if rel_dir.endswith('__pycache__'):
                continue

            mod_base = rel_dir.replace('/', '.').strip('.')

            for mod_name in (v[:-3] for v in filenames if v.endswith('.py')):
                if mod_name == '__init__':
                    mod_name = ''
                mod_path = '{}.{}'.format(mod_base, mod_name).strip('.')

                #print(directory, rel_dir, mod_base, mod_name, mod_path)
                for group, patterns in iteritems(self.groups):
                    if any(fnmatch.fnmatch(mod_path, x) for x in patterns):
                        self.grouped_module_paths[group].append(mod_path)

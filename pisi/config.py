# SPDX-FileCopyrightText: 2005-2011 TUBITAK/UEKAE, 2013-2017 Ikey Doherty, Solus Project
# SPDX-License-Identifier: GPL-2.0-or-later

"""
eopkg Configuration module is used for gathering and providing
regular eopkg configurations.
"""

import copy
import os
import os.path
from importlib import resources

import pisi
import pisi.configfile
import pisi.util
from pisi import context as ctx
from pisi import translate as _


class Error(pisi.Error):
    pass


class Options(object):
    def __getattr__(self, name):
        if name not in self.__dict__:
            return None
        else:
            return self.__dict__[name]

    def __setattr__(self, name, value):
        self.__dict__[name] = value


class Config(object, metaclass=pisi.util.Singleton):
    """Config Singleton"""

    def __init__(self, options=Options()):
        self.set_options(options)
        confpath = "/usr/share/defaults/eopkg/eopkg.conf"
        possible = [
            str(resources.files("pisi.data").joinpath("eopkg.conf")),
            "/etc/eopkg/eopkg.conf",
        ]
        for path in possible:
            if os.path.exists(path):
                confpath = path
                break
        self.values = pisi.configfile.ConfigurationFile(confpath)

        # get the initial environment variables. this is needed for
        # build process.
        self.environ = copy.deepcopy(os.environ)

    def set_options(self, options):
        self.options = options

        # Reset __dest_dir to re-read from options
        self.__dest_dir = None

    def set_option(self, opt, val):
        setattr(self.options, opt, val)

    def get_option(self, opt):
        if self.options:
            if hasattr(self.options, opt):
                return getattr(self.options, opt)
        return None

    # directory accessor functions
    # here is how it goes
    # x_dir: system wide directory for storing info type x
    # pkg_x_dir: per package directory for storing info type x

    def dest_dir(self):
        if self.__dest_dir is None:
            destdir = self.get_option("destdir")
            if destdir:
                self.__dest_dir = os.path.abspath(destdir)
            else:
                self.__dest_dir = self.values.general.destinationdirectory

            if not os.path.exists(self.__dest_dir):
                ctx.ui.warning(
                    _("Destination directory %s does not exist. " "Creating it.")
                    % self.__dest_dir
                )
                os.makedirs(self.__dest_dir)

        return self.__dest_dir

    def subdir(self, path):
        subdir = pisi.util.join_path(self.dest_dir(), path)

        # If the directory does not exist, try to create it.
        try:
            pisi.util.ensure_dirs(subdir)
        except OSError:
            pass

        return subdir

    def log_dir(self):
        return self.subdir(self.values.dirs.log_dir)

    def lib_dir(self):
        return self.subdir(self.values.dirs.lib_dir)

    def info_dir(self):
        return self.subdir(self.values.dirs.info_dir)

    def history_dir(self):
        return self.subdir(self.values.dirs.history_dir)

    def lock_dir(self):
        return self.subdir(self.values.dirs.lock_dir)

    def packages_dir(self):
        return self.subdir(self.values.dirs.packages_dir)

    def archives_dir(self):
        return self.subdir(self.values.dirs.archives_dir)

    def cache_root_dir(self):
        return self.subdir(self.values.dirs.cache_root_dir)

    def cached_packages_dir(self):
        return self.subdir(self.values.dirs.cached_packages_dir)

    def compiled_packages_dir(self):
        return self.subdir(self.values.dirs.compiled_packages_dir)

    def debug_packages_dir(self):
        return self.subdir(self.values.dirs.debug_packages_dir)

    def index_dir(self):
        return self.subdir(self.values.dirs.index_dir)

    def tmp_dir(self):
        sysdir = self.subdir(self.values.dirs.tmp_dir)
        if "USER" in os.environ:
            userdir = self.subdir("/tmp/eopkg-" + os.environ["USER"])
        else:
            userdir = self.subdir("/tmp/eopkg-root")
        # check write access
        if os.access(sysdir, os.W_OK):
            return sysdir
        else:
            return userdir


# TODO: remove this
config = Config()

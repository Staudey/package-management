# SPDX-FileCopyrightText: 2005-2011 TUBITAK/UEKAE, 2013-2017 Ikey Doherty, Solus Project
# SPDX-License-Identifier: GPL-2.0-or-later

# standard python modules
import os
from glob import glob
from gettext import translation

__trans = translation("pisi", fallback=True)
_ = __trans.gettext

# Pisi Modules
import pisi.context as ctx

# ActionsAPI Modules
import pisi.actionsapi
import pisi.actionsapi.get as get
from pisi.actionsapi.shelltools import export
from pisi.actionsapi.shelltools import isEmpty
from pisi.actionsapi.shelltools import system


class ConfigureError(pisi.actionsapi.Error):
    def __init__(self, value=""):
        pisi.actionsapi.Error.__init__(self, value)
        self.value = value
        ctx.ui.error(value)


class CompileError(pisi.actionsapi.Error):
    def __init__(self, value=""):
        pisi.actionsapi.Error.__init__(self, value)
        self.value = value
        ctx.ui.error(value)


class InstallError(pisi.actionsapi.Error):
    def __init__(self, value=""):
        pisi.actionsapi.Error.__init__(self, value)
        self.value = value
        ctx.ui.error(value)


class RunTimeError(pisi.actionsapi.Error):
    def __init__(self, value=""):
        pisi.actionsapi.Error.__init__(self, value)
        self.value = value
        ctx.ui.error(value)


def get_config(config):
    return (
        os.popen("ruby -rrbconfig -e 'puts Config::CONFIG[\"%s\"]'" % config)
        .read()
        .strip()
    )


def get_ruby_version():
    return get_config("ruby_version")


def get_rubylibdir():
    return get_config("rubylibdir")


def get_sitedir():
    return get_config("sitedir")


def get_ruby_install_name():
    return get_config("ruby_install_name")


def get_gemhome():
    (rubylibdir, ruby_version) = os.path.split(get_rubylibdir())

    return os.path.join(get.installDIR(), rubylibdir.lstrip("/"), "gems", ruby_version)


def get_sitelibdir():
    return get_config("sitelibdir")


def auto_dodoc():
    from pisi.actionsapi.pisitools import dodoc

    docs = (
        "AUTHORS",
        "CHANGELOG",
        "CONTRIBUTORS",
        "Change*",
        "KNOWN_BUGS",
        "MAINTAINERS",
        "NEWS",
        "README*",
        "History.txt",
    )

    for doc_glob in docs:
        for doc in glob(doc_glob):
            if not isEmpty(doc):
                dodoc(doc)


def install(parameters=""):
    """does ruby setup.rb install"""
    if system(
        "ruby -w setup.rb --prefix=/%s --destdir=%s %s"
        % (get.defaultprefixDIR(), get.installDIR(), parameters)
    ):
        raise InstallError(_("Install failed."))

    auto_dodoc()


def rake_install(parameters=""):
    """execute rake script for installation"""
    if system(
        "rake -t -l %s %s"
        % (os.path.join("/", get.defaultprefixDIR(), "lib"), parameters)
    ):
        raise InstallError(_("Install failed."))

    auto_dodoc()


def run(parameters=""):
    """executes parameters with ruby"""
    export("DESTDIR", get.installDIR())

    if system("ruby %s" % parameters):
        raise RuntimeError(_("Running 'ruby %s' failed.") % parameters)

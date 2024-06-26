# SPDX-FileCopyrightText: 2005-2011 TUBITAK/UEKAE, 2013-2017 Ikey Doherty, Solus Project
# SPDX-License-Identifier: GPL-2.0-or-later

# ActionsAPI Modules
from pisi.actionsapi import get
from pisi.actionsapi import cmaketools
from pisi.actionsapi import shelltools

basename = "kde4"

prefix = "/%s" % get.defaultprefixDIR()
libdir = "%s/lib" % prefix
bindir = "%s/bin" % prefix
modulesdir = "%s/%s" % (libdir, basename)
libexecdir = "%s/libexec" % modulesdir
iconsdir = "%s/share/icons" % prefix
applicationsdir = "%s/share/applications/%s" % (prefix, basename)
mandir = "/%s" % get.manDIR()
sharedir = "%s/share/%s" % (prefix, basename)
appsdir = "%s/apps" % sharedir
configdir = "%s/config" % sharedir
sysconfdir = "/etc"
servicesdir = "%s/services" % sharedir
servicetypesdir = "%s/servicetypes" % sharedir
includedir = "%s/include/%s" % (prefix, basename)
docdir = "/%s/%s" % (get.docDIR(), basename)
htmldir = "%s/html" % docdir
wallpapersdir = "%s/share/wallpapers" % prefix


def configure(parameters="", installPrefix=prefix, sourceDir=".."):
    """parameters -DLIB_INSTALL_DIR="hede" -DSOMETHING_USEFUL=1"""

    shelltools.makedirs("build")
    shelltools.cd("build")

    cmaketools.configure(
        "-DDATA_INSTALL_DIR:PATH=%s \
            -DINCLUDE_INSTALL_DIR:PATH=%s \
            -DCONFIG_INSTALL_DIR:PATH=%s \
            -DLIBEXEC_INSTALL_DIR:PATH=%s \
            -DSYSCONF_INSTALL_DIR:PATH=%s \
            -DHTML_INSTALL_DIR:PATH=%s \
            -DMAN_INSTALL_DIR:PATH=%s \
            -DCMAKE_SKIP_RPATH:BOOL=ON \
            -DLIB_INSTALL_DIR:PATH=%s %s"
        % (
            appsdir,
            includedir,
            configdir,
            libexecdir,
            sysconfdir,
            htmldir,
            mandir,
            libdir,
            parameters,
        ),
        installPrefix,
        sourceDir,
    )

    shelltools.cd("..")


def make(parameters=""):
    cmaketools.make("-C build %s" % parameters)


def install(parameters="", argument="install"):
    cmaketools.install("-C build %s" % parameters, argument)

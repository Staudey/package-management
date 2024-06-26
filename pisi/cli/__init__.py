# SPDX-FileCopyrightText: 2005-2011 TUBITAK/UEKAE, 2013-2017 Ikey Doherty, Solus Project
# SPDX-License-Identifier: GPL-2.0-or-later

import locale
import re
import sys
import tty

import pisi
import pisi.ui
import pisi.util
from pisi import context as ctx
from pisi import translate as _


class Error(pisi.Error):
    pass


class Exception(pisi.Exception):
    pass


def printu(obj, err=False):
    if not isinstance(obj, str):
        obj = str(obj)
    if err:
        out = sys.stderr
    else:
        out = sys.stdout
    out.write(obj)
    out.flush()


class CLI(pisi.ui.UI):
    "Command Line Interface"

    def __init__(self, show_debug=False, show_verbose=False):
        super(CLI, self).__init__(show_debug, show_verbose)
        self.warnings = 0
        self.errors = 0

    def close(self):
        pisi.util.xterm_title_reset()

    def output(self, msg, err=False, verbose=False):
        if (verbose and self.show_verbose) or (not verbose):
            if isinstance(msg, bytes):
                msg = msg.decode("utf-8")
            if err:
                out = sys.stderr
            else:
                out = sys.stdout
            out.write(msg)
            out.flush()

    def formatted_output(self, msg, verbose=False, noln=False, column=":"):
        key_width = 20
        line_format = "%(key)-20s%(column)s%(rest)s"
        term_height, term_width = pisi.util.get_terminal_size()

        def find_whitespace(s, i):
            while s[i] not in (" ", "\t"):
                i -= 1
            return i

        def align(s):
            align_width = term_width - key_width - 2
            s_width = len(s)
            new_s = ""
            index = 0
            while True:
                next_index = index + align_width
                if next_index >= s_width:
                    new_s += s[index:]
                    break
                next_index = find_whitespace(s, next_index)
                new_s += s[index:next_index]
                index = next_index
                if index < s_width:
                    new_s += "\n" + " " * (key_width + 1)
            return new_s

        new_msg = ""
        for line in msg.split("\n"):
            key, _column, rest = line.partition(column)
            rest = align(rest)
            new_msg += line_format % {"key": key, "column": _column, "rest": rest}
            if not noln:
                new_msg = "%s\n" % new_msg
        msg = new_msg
        self.output(str(msg), verbose=verbose)

    def info(self, msg, verbose=False, noln=False):
        # TODO: need to look at more kinds of info messages
        # let's cheat from KDE :)
        if not noln:
            msg = "%s\n" % msg
        self.output(str(msg), verbose=verbose)

    def warning(self, msg, verbose=False):
        msg = str(msg)
        self.warnings += 1
        if ctx.log:
            ctx.log.warning(msg)
        if ctx.get_option("no_color"):
            self.output(_("Warning: ") + msg + "\n", err=True, verbose=verbose)
        else:
            self.output(
                pisi.util.colorize(msg + "\n", "brightyellow"),
                err=True,
                verbose=verbose,
            )

    def error(self, msg):
        msg = str(msg)
        self.errors += 1
        if ctx.log:
            ctx.log.error(msg)
        if ctx.get_option("no_color"):
            self.output(_("Error: ") + msg + "\n", err=True)
        else:
            self.output(pisi.util.colorize(msg + "\n", "brightred"), err=True)

    def action(self, msg, verbose=False):
        # TODO: this seems quite redundant?
        msg = str(msg)
        if ctx.log:
            ctx.log.info(msg)
        self.output(pisi.util.colorize(msg + "\n", "green"))

    def choose(self, msg, opts):
        msg = str(msg)
        prompt = msg + pisi.util.colorize(" (%s)" % "/".join(opts), "red")
        while True:
            s = input(prompt)
            for opt in opts:
                if opt.startswith(str(s)):
                    return opt

    def confirm(self, msg: str):
        if ctx.config.options and ctx.config.options.yes_all:
            return True

        yes_expr = re.compile(locale.nl_langinfo(locale.YESEXPR))
        no_expr = re.compile(locale.nl_langinfo(locale.NOEXPR))

        while True:
            tty.tcflush(sys.stdin.fileno(), 0)
            prompt = msg + pisi.util.colorize(_(" (yes/no)"), "red")
            s = input(prompt)

            if yes_expr.search(s):
                return True

            if no_expr.search(s):
                return False

    def display_progress(self, **ka):
        """display progress of any operation"""
        if ka["operation"] in ["removing", "rebuilding-db"]:
            return
        elif ka["operation"] == "fetching":
            totalsize = "%.1f %s" % pisi.util.human_readable_size(ka["total_size"])
            out = "\r%-30.50s (%s)%3d%% %9.2f %s [%s]" % (
                ka["filename"],
                totalsize,
                ka["percent"],
                ka["rate"],
                ka["symbol"],
                ka["eta"],
            )
            self.output(out)
        else:
            self.output("\r%s (%d%%)" % (ka["info"], ka["percent"]))

        if ka["percent"] == 100:
            self.output(pisi.util.colorize(_(" [complete]\n"), "gray"))

    def status(self, msg=None):
        if msg:
            msg = str(msg)
            self.output(pisi.util.colorize(msg + "\n", "brightgreen"))
            pisi.util.xterm_title(msg)

    def notify(self, event, **keywords):
        if event == pisi.ui.installed:
            msg = _("Installed %s") % keywords["package"].name
        elif event == pisi.ui.removed:
            msg = _("Removed %s") % keywords["package"].name
        elif event == pisi.ui.upgraded:
            msg = _("Upgraded %s") % keywords["package"].name
        elif event == pisi.ui.configured:
            msg = _("Configured %s") % keywords["package"].name
        elif event == pisi.ui.extracting:
            msg = _("Extracting the files of %s") % keywords["package"].name
        else:
            msg = None
        if msg:
            self.output(pisi.util.colorize(msg + "\n", "cyan"))
            if ctx.log:
                ctx.log.info(msg)

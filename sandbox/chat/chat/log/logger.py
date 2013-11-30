# Copyright (c) 2013 Appspand, Inc.

import errno
import logging
import logging.handlers
import os
import sys
import time

from tornado.escape import _unicode
from tornado.util import unicode_type, basestring_type

try:
    import curses
except ImportError:
    curses = None


access = logging.getLogger("tornado.access")
application = logging.getLogger("tornado.application")
general = logging.getLogger("tornado.general")


def _stderr_supports_color():
    color = False
    if curses and sys.stderr.isatty():
        try:
            curses.setupterm()
            if curses.tigetnum("colors") > 0:
                color = True
        except Exception:
            pass
    return color


class LogFormatter(logging.Formatter):
    """Log formatter used in Appspand.

    Key features of this formatter are:

    * Color support when logging to a terminal that supports it.
    * Timestamps on every log line.
    * Robust against str/bytes encoding problems.
    """

    def __init__(self, task_id=0, color=True, *args, **kwargs):
        super(LogFormatter, self).__init__(*args, **kwargs)

        self._task_id = task_id
        self._color = color and _stderr_supports_color()
        if self._color:
            fg_color = (curses.tigetstr("setaf") or
                        curses.tigetstr("setf") or "")
            if (3, 0) < sys.version_info < (3, 2, 3):
                fg_color = unicode_type(fg_color, "ascii")
            self._colors = {
                logging.DEBUG: unicode_type(curses.tparm(fg_color, 4),  # Blue
                                            "ascii"),
                logging.INFO: unicode_type(curses.tparm(fg_color, 2),  # Green
                                           "ascii"),
                logging.WARNING: unicode_type(curses.tparm(fg_color, 3),  # Yellow
                                              "ascii"),
                logging.ERROR: unicode_type(curses.tparm(fg_color, 1),  # Red
                                            "ascii"),
            }
            self._normal = unicode_type(curses.tigetstr("sgr0"), "ascii")

    def format(self, record):
        try:
            record.message = record.getMessage()
        except Exception as e:
            record.message = "Bad message (%r): %r" % (e, record.__dict__)
        assert isinstance(record.message, basestring_type)

        record.task_id = self._task_id
        record.asctime = time.strftime(
            "%y%m%d %H:%M:%S", self.converter(record.created))
        prefix = "[%(task_id)d %(levelname)1.1s %(asctime)s %(module)s:%(lineno)d]" % \
            record.__dict__
        if self._color:
            prefix = (self._colors.get(record.levelno, self._normal) +
                      prefix + self._normal)

        def safe_unicode(s):
            try:
                return _unicode(s)
            except UnicodeDecodeError:
                return repr(s)

        formatted = prefix + " " + safe_unicode(record.message)
        if record.exc_info:
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            lines = [formatted.rstrip()]
            lines.extend(safe_unicode(ln) for ln in record.exc_text.split('\n'))
            formatted = '\n'.join(lines)
        return formatted.replace("\n", "\n    ")


def enable_pretty_logging(logger=None, options=None, task_id=0):
    if options is None:
        return
    if options["logging"] == "none":
        return

    if logger is None:
        logger = logging.getLogger()

    logger.setLevel(getattr(logging, options["logging"].upper()))

    if options["log_file_prefix"]:
        channel = logging.handlers.RotatingFileHandler(
            filename=options["log_file_prefix"],
            maxBytes=options["log_file_max_size"],
            backupCount=options["log_file_num_backups"])
        channel.setFormatter(LogFormatter(task_id=0, color=False))
        logger.addHandler(channel)

    if (options["log_to_stderr"] or
            (options["log_to_stderr"] is None and not logger.handlers)):
        channel = logging.StreamHandler()
        channel.setFormatter(LogFormatter(task_id=0, color=True))
        logger.addHandler(channel)


def _build_canonical_file_path(base_path, filename):
    try:
        if not os.path.isdir(base_path):
            os.makedirs(base_path, 0755)
    except OSError as e:
        if e.errno == errno.EEXIST and os.path.isdir(base_path):
            pass
        else:
            raise

    canonical_file_path = base_path
    if not canonical_file_path.endswith("/"):
        canonical_file_path += "/"
    canonical_file_path += filename

    return canonical_file_path


def init(config, task_id):
    options = dict(
        log_file_max_size=1024 * 1024,
        log_file_num_backups=100,
        log_to_stderr=False
    )

    canonical_file_path = _build_canonical_file_path(base_path=config.logging.access.path,
                                                     filename=config.logging.access.filename)
    options["logging"] = config.logging.access.level
    options["log_file_prefix"] = canonical_file_path
    enable_pretty_logging(logger=access, options=options, task_id=task_id)

    canonical_file_path = _build_canonical_file_path(base_path=config.logging.application.path,
                                                     filename=config.logging.application.filename)
    options["logging"] = config.logging.application.level
    options["log_file_prefix"] = canonical_file_path
    enable_pretty_logging(logger=application, options=options, task_id=task_id)

    canonical_file_path = _build_canonical_file_path(base_path=config.logging.general.path,
                                                     filename=config.logging.general.filename)
    options["logging"] = config.logging.general.level
    options["log_file_prefix"] = canonical_file_path
    enable_pretty_logging(logger=general, options=options, task_id=task_id)

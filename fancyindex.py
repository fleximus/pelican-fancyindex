# -*- coding: utf-8 -*-
'''
FancyIndex Generator
-------

The FancyIndex plugin generates file listings.
'''

from __future__ import unicode_literals, print_function

from pelican import signals
from pelican.generators import (Generator, _FileLoader)

import os
import time
import logging
import pprint

__author__ = "Felix Ehlers"
__license__ = "BSD 2-Clause"
__version__ = "v0.7.0"

logger = logging.getLogger(__name__)


class FancyIndex(object):
    files = []

    def __init__(self, name, root):
        self.name = name
        self.root = root


class FancyIndexFile(object):
    def __init__(self, name, url, type, size, modified):
        self.name = name
        self.url = url
        self.type = type
        self.size = size
        self.modified = modified


class FancyIndexGenerator(Generator):
    """Generate index.html on the output dir, for all files and dirs found
    rst"""

    def __init__(self, *args, **kwargs):
        super(FancyIndexGenerator, self).__init__(*args, **kwargs)

        self.fancyindex_input_path = os.path.join(self.settings['FANCYINDEX_INPUT_PATH'])
        self.fancyindex_output_path = os.path.join(self.output_path, self.settings['FANCYINDEX_OUTPUT_PATH'])

    def generate_context(self):
        fancyindexes = []
        fancyindex = []

        for root, dirs, files in os.walk(self.settings['FANCYINDEX_INPUT_PATH']):
            for name in dirs:
                dir_relpath = os.path.relpath(os.path.join(root, name), self.fancyindex_input_path)
                logger.info('FancyIndex: Adding dir ' + dir_relpath + ' to context')
                fancyindexes.append(dir_relpath)

        fancyindexes.sort()

        self.context['fancyindexes'] = fancyindexes

        # fancyindex.append(FancyIndexFile('dummy.txt', 'file', '23 Bytes', '01.01.1970'))
        self.context['fancyindex'] = fancyindexes

    def human(self, size):
        B = "B"
        KB = "KB"
        MB = "MB"
        GB = "GB"
        TB = "TB"
        UNITS = [B, KB, MB, GB, TB]
        HUMANFMT = "%i %s"
        HUMANRADIX = 1024.

        for u in UNITS[:-1]:
            if size < HUMANRADIX:
                return HUMANFMT % (size, u)
            size /= HUMANRADIX

        return HUMANFMT % (size, UNITS[-1])

    def generate_output(self, writer):
        if not os.path.exists(self.fancyindex_output_path):
            try:
                os.mkdir(self.fancyindex_output_path)
            except OSError:
                logger.error("Couldn't create the fancyindex output folder in " + output_path)

        for findex in self.context['fancyindexes']:
            fancydir = os.path.join(self.fancyindex_output_path, findex)
            if not os.path.exists(fancydir):
                try:
                    os.mkdir(fancydir)
                except OSError:
                    logger.error("Couldn't create folder " + fancydir)

            fancyindex_file = fancydir + '/' + self.settings['FANCYINDEX_SAVE_AS']
            path = os.path.join(self.fancyindex_input_path, findex)

            root_path = findex[:findex.index(os.sep)] if os.sep in findex else findex
            fancyindex = FancyIndex(findex, root_path)
            fancyindex.files = []

            # add parent folder link if possible
            if findex.find('/') != -1:
                fancyindex.files.append(FancyIndexFile("..", os.path.join(findex, ".."), 'directory', '-',
                                                       time.strftime('%d.%m.%Y', time.localtime(
                                                           os.stat(os.path.join(path, '..')).st_mtime))))

            for f in os.listdir(path):
                file = os.path.join(path, f)
                url = os.path.join(findex, os.path.basename(file))
                stat = os.stat(os.path.join(path, file))
                type = 'directory' if os.path.isdir(file) else 'file'
                size = self.human(stat.st_size)
                modified = time.strftime('%d.%m.%Y', time.localtime(stat.st_mtime))
                fancyindex.files.append(FancyIndexFile(f, url, type, size, modified))

            # sort files by type (direcories before files) and by name
            fancyindex.files.sort(key=lambda k: (k.type, k.name))

            self.context['fancyindex'] = fancyindex
            del fancyindex
            writer.write_file(fancyindex_file, self.get_template('fancyindex'), self.context)
            del self.context['fancyindex']

        del self.context['fancyindexes']


def get_generators(generators):
    return FancyIndexGenerator


def register():
    signals.get_generators.connect(get_generators)

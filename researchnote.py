#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
File: researchnote.py
Author: Loïc Séguin-Charbonneau
Description: Manage a research notebook using reStructuredText files.

License: BSD license

"""

from __future__  import print_function

import argparse
import ConfigParser
import re
import os
import string
import subprocess
import sys
import time
import unidecode


__version__ = '0.1'


NOTE_FILE_RE = r'\d{4,4}-\d{2,2}-\d{2,2}_[\w\-\+]*\.'


def _(astring):
    """Should be used for localization."""
    return astring


def create_note(args, config):
    """Create a new note.

    This creates a new file named ``YYYY-MM-DD_A_note_title.rst`` with the
    current date. The file contains the following template

        A note name
        ===========

        :date: YYYY-MM-DD
        :author: Author Name
        :tags:

    Once the file is created, the user's preferred text editor is launched to
    edit the file.

    """
    title = unicode(' '.join(args.title), 'utf-8')
    date = time.strftime('%Y-%m-%d', time.localtime())
    notes_dir = config['notes_dir']
    note_format = config['note_format']
    file_title = get_new_note_filename(title, date, notes_dir, note_format)
    note_file = open(file_title, 'w')
    note_file.write(title.encode('utf-8'))
    note_file.write('\n' + len(title) * '=' + '\n\n')
    note_file.write(':date: {}\n:author: {}\n:tags: '.format(date,
                    config['author']))
    note_file.close()
    if config['editor']:
        subprocess.call(config['editor'].split() + [file_title])
        post_edit(file_title)
    else:
        print('Created file {}'.format(file_title))


def post_edit(fname):
    """Copy all figures referenced in fname into the notes_dir/images folder
    and adjust figure references accordingly.
    
    """
    f = open(fname)
    for line in f:
        pass


def get_new_note_filename(title, date, notes_dir, note_format):
    """Return a file name for a new note with specified title and date."""
    file_title = unidecode.unidecode(title)
    file_title = file_title.translate(string.maketrans('', ''),
            string.punctuation)
    file_title = file_title.replace(' ', '_')
    file_title = os.path.join(notes_dir,
            date.replace('/', '-') + '_' + file_title)
    i = 0
    while True:
        try:
            if i:
                open('{}_{}.{}'.format(file_title, str(i), note_format))
            else:
                open('{}.{}'.format(file_title, note_format))
            i += 1
        except IOError:
            if i:
                file_title += '_{}.{}'.format(str(i), note_format)
            else:
                file_title += '.{}'.format(note_format)
            break

    return file_title


def edit_note(args, config):
    """Edit the note referred to by ``args.identifier``.

    The identifier can either be a note title, a date, a filename or a note
    number.

    """
    identifier = ' '.join(args.identifier)
    fname = ''
    notes_dir = config['notes_dir']
    note_format = config['note_format']
    try:
        numid = int(identifier)
        fname, numid = get_note_list(notes_dir, note_format)[numid - 1]
    except ValueError:
        fnames_numids = get_note_list(notes_dir, note_format)
        notes = [(fname,) + read_note_info(open(fname)) for
                 fname, numid in fnames_numids]
        for fname, date, title in notes:
            if date == identifier or identifier in title:
                break

    if not fname:
        print("Can't find note matching identifier {}".format(identifier),
                file=sys.stderr)
        return

    if config['editor']:
        subprocess.call(config['editor'].split() + [fname])
    else:
        print("EDITOR not defined, can't open file for editing.",
              file=sys.stderr)


def read_note_info(note_file):
    """Read the note contained in note_file and return the date and the title.

    """
    title = note_file.readline().strip()
    line = note_file.readline()
    while line and ':date:' not in line.lower():
        line = note_file.readline()
    date = line.split(':')[-1].strip()
    return date, title


def get_note_list(notes_dir, note_format):
    """Open notes_dir and find all notes. Return a list of notes paths."""
    listdir = os.listdir(notes_dir)
    notes = []
    for fname in listdir:
        if re.compile(NOTE_FILE_RE + note_format).match(fname):
            notes.append(os.path.join(notes_dir, fname))
    notes = sorted(notes)
    return zip(notes, range(1, len(notes) + 1))


def list_notes(args, config):
    """List all notes in chronological order."""
    notes = get_note_list(config['notes_dir'], config['note_format'])
    notes = [read_note_info(open(fname)) + (numid,) for fname, numid in notes]
    if args.reverse:
        notes.reverse()
    for date, title, numid in notes:
        print('{:3d}   {}   {}'.format(numid, date, title))


def read_config(fname='~/.researchnoterc'):
    """Read configuration file.

    The default location for the configuration file is ``~/.researchnoterc``.
    This file is in INI format and contains information about the author, the
    location of the notebook and the editor used to create and edit notes.

    """
    configs = {
            'author': '',
            'editor': os.environ.get('EDITOR', ''),
            'notes_dir': os.getcwd(),
            'note_format': 'rst'
            }
    try:
        config = ConfigParser.ConfigParser(configs)
        config.read(os.path.expanduser(fname))
        configs['author'] = config.get('ResearchNote', 'author')
        configs['editor'] = config.get('ResearchNote', 'editor')
        configs['notes_dir'] = os.path.expanduser(config.get('ResearchNote', 'notes_dir'))
        configs['note_format'] = config.get('ResearchNote', 'note_format')
    except ConfigParser.NoSectionError:
        # Configuration file is badly formatted
        pass
    return configs


def run(argv=sys.argv[1:]):
    """Parse the command line arguments and run the appropriate command."""
    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument('-c', '--config', default='~/.researchnoterc',
            help=_('configuration file to use'))

    clparser = argparse.ArgumentParser(description=_('Manage a research ' +
            'notebook using reStructuredText files.'), parents=[parent_parser])
    clparser.add_argument('-v', '--version', action='version',
            version='%(prog)s ' + __version__)

    subparsers = clparser.add_subparsers()
    createparser = subparsers.add_parser(_('create'),
            help=_('create a new note'), parents=[parent_parser])
    createparser.add_argument('title', nargs='+')
    createparser.set_defaults(func=create_note)

    editparser = subparsers.add_parser(_('edit'),
            help=_('edit an existing note'), parents=[parent_parser])
    editparser.add_argument('identifier', nargs='+')
    editparser.set_defaults(func=edit_note)

    listparser = subparsers.add_parser(_('list'), help=_('list all notes'),
            parents=[parent_parser])
    listparser.add_argument('-r', '--reverse', action='store_true',
            help=_('show newest notes first'))
    listparser.set_defaults(func=list_notes)

    args = clparser.parse_args(argv)
    args.func(args, read_config(args.config))


if __name__ == '__main__':
    run(sys.argv[1:])

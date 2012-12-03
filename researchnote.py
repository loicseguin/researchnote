#!/usr/bin/env python
#-*- coding: utf-8 -*-


from __future__  import print_function

import argparse
import ConfigParser
import re
import os
import subprocess
import sys
import time
import unidecode


__version__ = '0.1'


NOTE_FILE_RE = r'\d{4,4}-\d{2,2}-\d{2,2}_[\w\-\+]*\.rst'


def _(astring):
    """Should be used for localization."""
    return astring


def create_note(args):
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
    date = time.strftime('%Y/%m/%d', time.localtime())
    author, editor, notes_dir = read_config(args.config)
    file_title = unidecode.unidecode(
            title).replace(',', '').replace('.', '').replace(' ', '_')
    file_title = os.path.join(notes_dir, date + '_' + file_title)
    i = 0
    while True:
        try:
            if i:
                open(file_title + '_' + str(i) + '.rst')
            else:
                open(file_title + '.rst')
            i += 1
        except IOError:
            if i:
                file_title += '_' + str(i) + '.rst'
            else:
                file_title += '.rst'
            note_file = open(file_title, 'w')
            break

    note_file.write(title.encode('utf-8'))
    note_file.write('\n' + len(title) * '=' + '\n\n')
    note_file.write(':date: {}\n:author: {}\n:tags: '.format(date, author))
    note_file.close()
    if editor:
        subprocess.call(editor.split() + [file_title])
    else:
        print('Created file {}'.format(file_title))


def edit_note(args):
    """Edit the note referred to by ``args.identifier``.
    
    The identifier can either be a note title, a date, a filename or a note
    number.

    """
    author, editor, notes_dir = read_config(args.config)
    identifier = ' '.join(args.identifier)
    fname = ''
    try:
        numid = int(identifier)
        fname, numid = get_note_list(notes_dir)[numid - 1]
    except ValueError:
        fnames_numids = get_note_list(notes_dir)
        notes = [(fname,) + read_note_info(open(fname)) for
                 fname, numid in fnames_numids]
        for fname, date, title in notes:
            if date == identifier or identifier in title:
                break

    if not fname:
        print("Can't find note matching identifier {}".format(identifier),
                file=sys.stderr)
        return

    if editor:
        subprocess.call(editor.split() + [fname])
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


def get_note_list(notes_dir):
    """Open notes_dir and find all notes. Return a list of notes paths."""
    listdir = os.listdir(notes_dir)
    notes = []
    for fname in listdir:
        if re.compile(NOTE_FILE_RE).match(fname):
            notes.append(os.path.join(notes_dir, fname))
    notes = sorted(notes)
    return zip(notes, range(1, len(notes) + 1))


def list_notes(args):
    """List all notes in chronological order."""
    author, editor, notes_dir = read_config(args.config)
    notes = get_note_list(notes_dir)
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
    author = ''
    editor = os.environ.get('EDITOR', '')
    notes_dir = os.getcwd()
    try:
        config = ConfigParser.ConfigParser({'author': author, 'editor': editor,
            'notes_dir': notes_dir})
        config.read(os.path.expanduser(fname))
        author = config.get('ResearchNote', 'author')
        editor = config.get('ResearchNote', 'editor')
        notes_dir = os.path.expanduser(config.get('ResearchNote', 'notes_dir'))
    except IOError:
        # Could not open configuration file
        pass
    except ConfigParser.NoSectionError:
        # Configuration file is badly formatted
        pass
    return author, editor, notes_dir


def run(argv=sys.argv[1:]):
    """Parse the command line arguments and run the appropriate command."""
    clparser = argparse.ArgumentParser(description=_('Manage a research ' +
            'notebook using reStructuredText files.'))
    clparser.add_argument('-v', '--version', action='version',
            version='%(prog)s ' + __version__)
    clparser.add_argument('-c', '--config', default='~/.researchnoterc',
            help=_('configuration file to use'))

    subparsers = clparser.add_subparsers()
    createparser = subparsers.add_parser(_('create'),
            help=_('create a new note'))
    createparser.add_argument('title', nargs='+')
    createparser.set_defaults(func=create_note)

    editparser = subparsers.add_parser(_('edit'),
            help=_('edit an existing note'))
    editparser.add_argument('identifier', nargs='+')
    editparser.set_defaults(func=edit_note)

    listparser = subparsers.add_parser(_('list'), help=_('list all notes'))
    listparser.add_argument('-r', '--reverse', action='store_true',
            help=_('show newest notes first'))
    listparser.set_defaults(func=list_notes)

    args = clparser.parse_args(argv)
    args.func(args)


if __name__ == '__main__':
    run(sys.argv[1:])

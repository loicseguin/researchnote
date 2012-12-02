researchnote
============

Manage a research notebook using reStructuredText files.

Recommended settings
--------------------

Add the following aliases to your ``.bash_profile``:

    alias rnc="researchnote create"
    alias rne="researchnote edit"
    alias rnl="researchnote list"

ResearchNote will try to read a configuration file named ``.researchnoterc`` in
the user's home folder. If this configuration file is not present, it is wise
to set the ``EDITOR`` environment variable:

    export EDITOR=vim

The configuration file can contain the following values:

    author = "Your Name"
    editor = "vim"
    notes_dir = "/path/to/research/notes"


Create a note
-------------

Create a note with

    researchnote create NOTE NAME

This will touch a new file in the ``notes_dir`` directory and create a note
skeleton in that file. If the ``EDITOR`` is set, it is used to open the file
for editing. The basic skeleton looks as follows:

    A note name
    ===========

    :date: 2012-12-02
    :author: Your Name
    :tags: 

New files are named using the ``YYYY-MM-DD_A_note_name.rst`` template.


Editing a note
--------------

It is possible to edit a note with

    researchnote edit IDENTIFIER

where ``IDENTIFIER`` is either a note name, a date or a file name.


Listing all notes
-----------------

To list all notes, use

    researchnote list

This will list note titles and dates in chronological order.


Deleting a note
---------------

No! Don't do that! It is very bad practice to delete research
notes. ResearchNote does not allow to delete notes.


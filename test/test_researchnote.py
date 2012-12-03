#-*- coding: utf-8 -*-


import StringIO
import researchnote
from nose.tools import assert_equal


class TestResearchNote:
    def setUp(self):
        self.researchnoterc = """\
[ResearchNote]
author = Loïc Séguin-Charbonneau
notes_dir = ~/PhD/Notebook
editor = vim
"""
        self.note1 = """\
Fitting SDSS spectra
====================

:date: 2012/10/30
:author: Loïc Séguin-Charbonneau
:tags: SDSS, fit

Spectra can be fetched from the Sloan Digital Sky Survey (SDSS) database using
the ``sloany`` command line utility. This programs takes an SQL query as input
and sends this query to the database server. If the ``-f`` flag is passed, the
spectra are fetched from the database. The directory ``~/SDSS`` contains 10501
raw spectra. These spectra are contained in FITS files whose format is
described on the SDSS website. The files are named
``spec-PPPP-MMMMM-FFFF.fits`` where PPPP corresponds to the plate number, MMMMM
is the MJD date and FFFF is the fiber id.
"""

        self.note2 = """\
Problem with SDSS J1406-0119
============================

:date: 2012/10/28
:author: Loïc Séguin-Charbonneau
:tags: SDSS

There seems to be a problem with the object SDSS J1406-0119. There are two
long names that correspond to this short name::


    J1406-0119   J1406-0119   22.22   sdss/J140619.82-011933.1   3   sdss/J140619.82-011933.1   3
    J1406-0119   J1406-0119   22.22   sdss/J140619.96-011932.4   3   sdss/J140619.96-011932.4   3

Indeed, a simple search in the ``METADATA`` files (``~/SDSS/*/METADATA``) finds
the following to spectra::

    spec-0915-52443-0607.fits    J140619.96-011932.4    J1406-0119
    spec-4038-55363-0792.fits    J140619.82-011933.1    J1406-0119

It turns out this is a single object. This object has been measured by both the
BOSS spectrometer and the SDSS (SEGUE 1 or 2) spectrometer.
"""

        self.note3 = """\
Problem with SDSS J1406-0119
============================

:patate: 2012/10/28
:author: Loïc Séguin-Charbonneau
:tags: SDSS

There seems to be a problem with the object SDSS J1406-0119. There are two
long names that correspond to this short name.
"""

    def test_read_valid_note_info(self):
        note_file = StringIO.StringIO(self.note1)
        date, title = researchnote.read_note_info(note_file)
        assert_equal(date, '2012/10/30')
        assert_equal(title, 'Fitting SDSS spectra')

    def test_read_invalid_note_info(self):
        note_file = StringIO.StringIO(self.note3)
        date, title = researchnote.read_note_info(note_file)
        assert_equal(date, '')
        assert_equal(title, 'Problem with SDSS J1406-0119')

    
    


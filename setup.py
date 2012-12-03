#-*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name='ResearchNote',
    version='0.1dev',
    license='BSD',
    long_description=open('README.md').read(),
    author="Loïc Séguin-Charbonneau",
    author_email="loicseguin@gmail.com",
    py_modules=['researchnote'],
    scripts=['researchnote']
)

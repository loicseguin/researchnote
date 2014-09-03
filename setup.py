#-*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='ResearchNote',
    version='0.2dev',
    license='BSD',
    long_description=open('README.md').read(),
    author="Loïc Séguin-Charbonneau",
    author_email="loicseguin@gmail.com",
    py_modules=['researchnote'],
    scripts=['researchnote'],
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3"],
    use_2to3=True
)

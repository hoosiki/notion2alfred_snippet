#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

with open('README.md') as readme_file:
    readme = readme_file.read()

install_requireent = []

setup_requires = [
    'pandas',
    'config2',
    'notion',
    'notion_as_db'
]

install_requires = [
    'pandas',
    'config2',
    'notion',
    'notion_as_db'
]

setup(
    name='notion2alfred_snippet',
    author='Junsang Park',
    author_email='publichey@gmail.com',
    url='https://github.com/hoosiki/notion2alfred_snippet.git',
    version='0.0.1',
    long_description=readme,
    long_description_content_type="text/markdown",
    description='Package for automation in generating alfred snippet from notion pages',
    packages=find_packages(),
    license='BSD',
    include_package_date=False,
    setup_requires=setup_requires,
    install_requires=install_requires,
    download_url='https://github.com/hoosiki/notion-as-db/blob/master/dist/notion2alfred_snippet-0.0.1.tar.gz'
)

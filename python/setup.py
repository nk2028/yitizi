# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

assert path.exists(path.join(here, 'src/yitizi/yitizi.json')), \
    'You must run the build script first'

with open(path.join(here, 'README.md'), encoding='utf8') as f:
    long_description = f.read()

setup(
    name='yitizi',
    version='0.1.0',
    description='Input a Chinese character. Output all the variant characters of it.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/nk2028/yitizi',
    author='Ngiox Khyen 2028 Project',
    author_email='support@nk2028.shn.hk',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Linguistic',
        'Natural Language :: Chinese (Traditional)',
        'Natural Language :: Chinese (Simplified)',
        'Natural Language :: Japanese',
        'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: JavaScript',
    ],
    keywords='chinese chinese-character natural-language-processing',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    package_data={
        'yitizi': ['yitizi.json'],
    },
    include_package_data=True,
    python_requires='>=3.5, <4',
    install_requires=[],
    entry_points={},
    project_urls={
        'Bug Reports': 'https://github.com/nk2028/yitizi/issues',
        'Source': 'https://github.com/nk2028/yitizi',
    },
    zip_safe=False
)

#!/usr/bin/env python

# Copyright 2015, Yahoo Inc.
# Licensed under the terms of the Apache License, Version 2.0.
# See the LICENSE file associated with the project for terms.
import os
import json
from setuptools import setup


# Package Metadata filename
METADATA_FILENAME = 'lopq/package_metadata.json'
BASEPATH = os.path.dirname(os.path.abspath(__file__))


# Long description of package
def get_package_description():
    with open("DESCRIPTION.md", "r") as description:
        return "".join(description.readlines())


LONG_DESCRIPTION = get_package_description()

# Create a dictionary of our arguments, this way this script can be imported
# without running setup() to allow external scripts to see the setup settings.
setup_arguments = {
    'name': 'lopq',
    'version': '1.0.0',
    'author': 'Clayton Mellina,Yannis Kalantidis,Huy Nguyen',
    'author_email': 'clayton@yahoo-inc.com',
    'url': 'http://github.com/yahoo/lopq',
    'license': 'Apache-2.0',
    'keywords': ['lopq', 'locally optimized product quantization',
                 'product quantization', 'compression', 'ann',
                 'approximate nearest neighbor', 'similarity search'],
    'packages': ['lopq'],
    'long_description': LONG_DESCRIPTION,
    'description': 'Python code for training and deploying Locally Optimized'
                   'Product Quantization (LOPQ) for approximate nearest'
                   'neighbor search of high dimensional data.',
    'classifiers': [
            'Development Status :: 5 - Production/Stable',
            'License :: OSI Approved :: Apache Software License',
            'Intended Audience :: Developers',
            'Intended Audience :: Science/Research',
            'Natural Language :: English',
            'Operating System :: MacOS :: MacOS X',
            'Operating System :: Microsoft :: Windows',
            'Operating System :: POSIX',
            'Operating System :: POSIX',
            'Operating System :: Unix',
            'Programming Language :: Python :: 2.7',
            'Topic :: Scientific/Engineering',
            'Topic :: Software Development'
    ],
    'package_data': {
        'lopq': ['package_metadata.json']
    },
    'platforms': 'Windows,Linux,Solaris,Mac OS-X,Unix',
    'include_package_data': True,
    'install_requires': ['protobuf>=2.6',
                         'numpy>=1.9',
                         'scipy>=0.14',
                         'scikit-learn>=0.18',
                         'lmdb>=0.87']
}


class Git(object):
    """
    Simple wrapper class to the git command line tools
    """
    version_list = ['0', '7', '0']

    def __init__(self, version=None):
        if version:
            self.version_list = version.split('.')

    @property
    def version(self):
        """
        Generate a Unique version value from the git information
        :return:
        """
        git_rev = len(os.popen('git rev-list HEAD').readlines())
        if git_rev != 0:
            self.version_list[-1] = '%d' % git_rev
        version = '.'.join(self.version_list)
        return version

    @property
    def branch(self):
        """
        Get the current git branch
        :return:
        """
        return os.popen('git rev-parse --abbrev-ref HEAD').read().strip()

    @property
    def hash(self):
        """
        Return the git hash for the current build
        :return:
        """
        return os.popen('git rev-parse HEAD').read().strip()

    @property
    def origin(self):
        """
        Return the fetch url for the git origin
        :return:
        """
        for item in os.popen('git remote -v'):
            split_item = item.strip().split()
            if split_item[0] == 'origin' and split_item[-1] == '(push)':
                return split_item[1]


def add_scripts_to_package():
    """
    Update the "scripts" parameter of the setup_arguments with any scripts
    found in the "scripts" directory.
    :return:
    """
    global setup_arguments

    if os.path.isdir('scripts'):
        setup_arguments['scripts'] = [
            os.path.join('scripts', f) for f in os.listdir('scripts')
        ]


def get_and_update_package_metadata():
    """
    Update the package metadata when the package is being built.
    :return:metadata - Dictionary of metadata information
    """
    global setup_arguments
    global METADATA_FILENAME

    if not os.path.exists('.git') and os.path.exists(METADATA_FILENAME):
        with open(METADATA_FILENAME) as fh:
            metadata = json.load(fh)
    else:
        git = Git(version=setup_arguments['version'])
        metadata = {
            'version': git.version,
            'git_hash': git.hash,
            'git_origin': git.origin,
            'git_branch': git.branch
        }
        with open(METADATA_FILENAME, 'w') as fh:
            json.dump(metadata, fh)
    return metadata


if __name__ == '__main__':
    # We're being run from the command line so call setup with our arguments
    metadata = get_and_update_package_metadata()
    setup_arguments['version'] = metadata['version']
    setup(**setup_arguments)

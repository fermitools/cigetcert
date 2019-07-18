# -*- coding: utf-8 -*-
#
# Except where noted, this source file is Copyright (c) 2015-2016, FERMI
#   NATIONAL ACCELERATOR LABORATORY.  All rights reserved.
#
# For details of the Fermitools (BSD) license see COPYING or
#  http://fermitools.fnal.gov/about/terms.html
#
# Author: Dave Dykstra dwd@fnal.gov

"""Package configuration for cigetcert
"""

import os.path
import re

from setuptools import setup


def find_version(path, varname="__version__"):
    """Parse the version metadata in the given file.
    """
    with open(path, 'r') as fp:
        version_file = fp.read()
    version_match = re.search(
        r"^{} = ['\"]([^'\"]*)['\"]".format(varname),
        version_file,
        re.M,
    )
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    # metadata
    name="cigetcert",
    version=find_version("cigetcert", varname="version"),
    description="Get an X.509 certificate with SAML ECP and store proxies",
    author="Dave Dykstra",
    author_email="cigetcert-support@fnal.gov",
    url="https://github.com/fermitools/cigetcert",
    license="BSD-3-Clause",
    long_description=open("README", "r").read(),
    long_description_content_type="text/plain",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: Unix",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Scientific/Engineering",
    ],
    # contents
    scripts=[
        "cigetcert",
    ],
    data_files=[
        (os.path.join("share", "man", "man1"), ["cigetcert.1"]),
    ],
    # dependencies
    setup_requires=[
        "setuptools",
    ],
    install_requires=[
        "lxml",
        "M2Crypto",
        "pykerberos",
        "pyOpenSSL",
    ],
)

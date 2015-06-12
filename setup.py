# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright © 2013 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
import os
from setuptools import setup, find_packages
from version import get_version

version = get_version()

setup(name='gs.group.stats',
    version=version,
    description="Statistics for GroupServer groups",
    long_description=open("README.rst").read() + "\n" +
                      open(os.path.join("docs", "HISTORY.rst")).read(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        "Environment :: Web Environment",
        "Framework :: Zope2",
        "Intended Audience :: Developers",
        'License :: OSI Approved :: Zope Public License',
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux"
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
      ],
    keywords='stats groupserver group',
    author='Richard Waid',
    author_email='richard@onlinegroups.net',
    url='http://groupserver.org/',
    license='ZPL 2.1',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['gs', 'gs.group'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'pytz',
        'sqlalchemy',
        'zope.browserpage',
        'zope.cachedescriptors',
        'zope.component',
        'zope.datetime',
        'zope.interface',
        'zope.tal',
        'zope.tales',
        'zope.schema',
        'gs.cache',
        'gs.config',
        'gs.content.layout',
        'gs.database',
        'gs.group.base',
        'gs.group.member.base',
        'gs.group.member.join',
        'gs.group.member.leave.base',
        'gs.group.member.log',
        'gs.viewlet',
        'Products.GSProfile',
        'Products.XWFCore',
    ],
    entry_points="""
    # -*- Entry points: -*-
    """,)

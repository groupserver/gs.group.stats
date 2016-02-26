# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright © 2013, 2016 OnlineGroups.net and Contributors.
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
from __future__ import unicode_literals, absolute_import, print_function
from zope.schema import ASCIILine
from zope.contentprovider.interfaces import IContentProvider


class IGSGroupStatsContentProvider(IContentProvider):
    groupId = ASCIILine(
        title='Group Identifier',
        description='The identifier for the group',
        required=True)

    siteId = ASCIILine(
        title='Site Identifier',
        description='The identifier for the site',
        required=True)

    pageTemplateFileName = ASCIILine(
        title="Page Template File Name",
        description='The name of the ZPT file that is used to render the status message.',
        required=False,
        default=b"browser/templates/stats.pt")

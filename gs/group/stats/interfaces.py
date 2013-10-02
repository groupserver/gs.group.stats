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
from zope.schema import ASCIILine
from zope.contentprovider.interfaces import IContentProvider


class IGSGroupStatsContentProvider(IContentProvider):
    groupId = ASCIILine(title=u'Group Identifier',
        description=u'The identifier for the group',
        required=True)

    siteId = ASCIILine(title=u'Site Identifier',
        description=u'The identifier for the site',
        required=True)

    pageTemplateFileName = ASCIILine(title=u"Page Template File Name",
        description=u'The name of the ZPT file that is used to '
        u'render the status message.',
        required=False,
        default="browser/templates/stats.pt")

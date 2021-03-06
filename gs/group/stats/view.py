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
from __future__ import absolute_import, unicode_literals, print_function
from zope.cachedescriptors.property import Lazy
from gs.group.base import GroupPage
from .messagequery import MessageQuery


class GSGroupStatsView(GroupPage):

    def __init__(self, context, request):
        super(GSGroupStatsView, self).__init__(context, request)

    @Lazy
    def messageQuery(self):
        retval = MessageQuery(self.context)
        return retval

    @Lazy
    def stats(self):
        retval = self.messageQuery.posting_stats(self.siteInfo.get_id(), [self.groupInfo.get_id()])
        return retval

    @Lazy
    def years(self):
        years = sorted(self.stats.keys())
        years.reverse()
        return years

    def get_months(self, year):
        retval = self.stats.get(year, {})
        return retval

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
from __future__ import absolute_import
from zope.cachedescriptors.property import Lazy
from zope.component import createObject
from .messagequery import MessageQuery
from .queries import MembersAtDate


class GroupPostingStats(object):

    def __init__(self, groupInfo):
        self.groupInfo = groupInfo
        self.context = groupInfo.groupObj

    @Lazy
    def siteInfo(self):
        retval = createObject('groupserver.SiteInfo', self.context)
        return retval

    def update(self):
        return None

    def digestMembers(self):
        mad = MembersAtDate(self.context)
        return mad.members_on_digest(self.siteInfo.id, self.groupInfo.id)

    def webonlyMembers(self):
        mad = MembersAtDate(self.context)
        return mad.members_on_webonly(self.siteInfo.id, self.groupInfo.id)

    @Lazy
    def postStats(self):
        retval = self.query.posts_per_day(self.groupInfo.id)
        retval.sort(key=lambda x: x['date'])
        return retval

    @Lazy
    def query(self):
        retval = MessageQuery(self.context)
        return retval

    @Lazy
    def postsExist(self):
        retval = False
        if self.postStats:
            retval = len(self.postStats) > 0
        assert type(retval) == bool
        return retval

    @Lazy
    def minPerDay(self):
        retval = 0
        if self.postStats:
            retval = min([s['n_posts'] for s in self.postStats])
        return retval

    @Lazy
    def maxPerDay(self):
        retval = 0
        if self.postStats:
            retval = max([s['n_posts'] for s in self.postStats])
        return retval

    @Lazy
    def meanPerDay(self):
        deltaT = self.postStats[-1]['date'] - self.postStats[0]['date']
        if deltaT.days > 0:
            nPosts = float(sum([s['n_posts'] for s in self.postStats]))
            mean = nPosts / deltaT.days
        else:
            mean = 0.0
        assert type(mean) == float
        return mean

    @Lazy
    def intMeanPerDay(self):
        return int(self.meanPerDay + 0.5)

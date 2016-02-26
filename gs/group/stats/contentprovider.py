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
from zope.component import createObject
from zope.contentprovider.interfaces import UpdateNotCalled
from zope.pagetemplate.pagetemplatefile import PageTemplateFile
from gs.group.member.base import FullMembers
from gs.viewlet import SiteContentProvider  # --=mpj17=-- Deliberly *site*
from .posting import GroupPostingStats


class GroupStatsContentProvider(SiteContentProvider):

    def __init__(self, context, request, view):
        super(GroupStatsContentProvider, self).__init__(context, request, view)
        self.__updated = False

    def update(self):
        self.__updated = True
        self.groupPostingStats = GroupPostingStats(self.groupInfo)
        self.groupPostingStats.update()
        self.fullMembers = FullMembers(self.groupInfo.groupObj)

    def render(self):
        if not self.__updated:
            raise UpdateNotCalled
        pageTemplate = PageTemplateFile(self.pageTemplateFileName)
        return pageTemplate(view=self)

    #########################################
    # Non standard methods below this point #
    #########################################

    @Lazy
    def groupInfo(self):
        # The group-stats are special. This content provider is often
        #   called from outside the group context. Because of this it
        #   can be passed the identifier for the group, and it uses
        #   that to find the group and render the right statistics.
        if hasattr(self, 'groupId') and self.groupId:
            retval = createObject('groupserver.GroupInfo', self.context, self.groupId)
        else:
            # We have no groupId passed in from the surrounding page
            #   template, so lets assume that we are in the context
            #   of a group.
            retval = createObject('groupserver.GroupInfo', self.context)
        assert retval
        return retval

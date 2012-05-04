#coding=utf-8
from operator import add
from zope.component import createObject
from zope.cachedescriptors.property import Lazy
from gs.content.base.page import SitePage
from queries import GroupStatsQuery

import datetime
from zope.datetime import parseDatetimetz

class GroupStats(SitePage):
    def __init__(self, context, request):
        SitePage.__init__(self, context, request)
        self.interval_start = parseDatetimetz(request['interval_start'])
        self.interval_end = parseDatetimetz(request['interval_end'])

        self.groupInfo = createObject('groupserver.GroupInfo', self.context)

    @Lazy
    def groupStatsQuery(self):
        da = self.context.zsqlalchemy
        retval = GroupStatsQuery(da)
        return retval

    def posts(self):
        return self.groupStatsQuery.posts(self.siteInfo.id, self.groupInfo.id,
                                          self.interval_start,
                                          self.interval_end)     
    
    def active_topics(self):
        return self.groupStatsQuery.active_topics(self.siteInfo.id, self.groupInfo.id,
                                           self.interval_start,
                                           self.interval_end)
   
    def authors(self):
        return self.groupStatsQuery.authors(self.siteInfo.id, self.groupInfo.id,
                                           self.interval_start,
                                           self.interval_end)

    def new_topics(self):
        return self.groupStatsQuery.new_topics(self.siteInfo.id, self.groupInfo.id,
                                           self.interval_start,
                                           self.interval_end)
 
    @Lazy
    def content(self):
        site_root = self.context.site_root()
        retval = site_root.Content
        return retval

    def add_siteInfo_to_items(self, items):
        retval = []
        for i in items:
            try:
                site = getattr(self.content, i['siteId'])
            except AttributeError, ae:
                # Ignore the sites that do not exist any more
                pass
            else:
                d = i
                d['siteInfo'] = createObject('groupserver.SiteInfo', site)
                retval.append(d)
        assert type(retval) == list
        return retval

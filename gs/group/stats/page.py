#coding=utf-8
from operator import add
from zope.component import createObject
from zope.cachedescriptors.property import Lazy
from gs.content.base.page import SitePage
from queries import GroupStatsQuery

class GroupStats(SitePage):

    @Lazy
    def jerryQuery(self):
        da = self.context.zsqlalchemy
        retval = GroupStatsQuery(da)
        return retval
    
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

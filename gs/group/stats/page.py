#coding=utf-8
from operator import add
from zope.component import createObject
from zope.cachedescriptors.property import Lazy
from gs.content.base.page import SitePage
from queries import GroupStatsQuery, MembersAtDate
from Products.GSGroupMember.groupMembersInfo import GSGroupMembersInfo

import datetime
import calendar
import pytz
import copy

from zope.datetime import parseDatetimetz

def month_periods(interval_start, interval_end):
    start_year = interval_start.year
    end_year = interval_end.year
    start_month = interval_start.month
    end_month = interval_end.month

    periods = []

    for year in range(start_year, end_year+1):
        first_month = 1
        last_month = 12
        if year == start_year:
            first_month = start_month
        elif year == end_year:
            last_month = end_month

        for month in range(first_month, last_month+1):
            first_weekday, number_of_days = calendar.monthrange(year,month)
            periods.append((year, month, number_of_days))

    return periods

def month_periods_as_datetime(month_periods):
    periods = []
    for year, month, last_day in month_periods:
        periods.append((datetime.datetime(year, month, 1, tzinfo=pytz.utc),
                        datetime.datetime(year, month, last_day, tzinfo=pytz.utc)))
    return periods

def periods_as_dict(periods):
    pdict = {}
    for year, month, result in periods:
        if not pdict.has_key(year):
            pdict[year] = {}
        pdict[year][month] = result    
    
    return pdict

class HistoricalGroupStats(SitePage):
    stats_attributes = (
               ('new_topics', u'New Topics'),
               ('active_topics', u'Active Topics'),
               ('posts', u'Posts'),
               ('authors', u'Authors'),
               ('join_delta', u'Join Delta'),
               ('member_average', u'Average Members'),
               ('member_end_of_period', u'Members at end of Period'),
               ('percentage_members_posting', u'Members posting (%)'),
               ('average_dialogue_depth', u'Average Dialogue Depth'),
               ('min_dialogue_depth', u'Min. Dialogue Depth'),
               ('max_dialogue_depth', u'Max. Diaglogue Depth'),
               ('percentage_single_post_topics', u'Single Post Topics (%)'))
    
    def __init__(self, context, request):
        SitePage.__init__(self, context, request)
         
        self.groupInfo = createObject('groupserver.GroupInfo', self.context)
        self.mad = MembersAtDate(self.context, self.context.zsqlalchemy)
        self.gs = GroupStatsQuery(self.context.zsqlalchemy)
        self.now = datetime.datetime.now(pytz.utc)
        self.earliest_date = self.mad.earliest_member_record(self.siteInfo.id,
                                                        self.groupInfo.id)
        
        self.month_periods = month_periods_as_datetime(month_periods(self.earliest_date, self.now))

    def display_stats(self):
        return self.stats_attributes

    def months(self):
        mperiods = copy.deepcopy(self.month_periods)
        mperiods.sort(reverse=True)
        return mperiods

    def years(self):
        start_year = self.earliest_date.year
        end_year = self.now.year
        start_month = self.earliest_date.month
        end_month = self.now.month
        cal = []
        for year in range(start_year, end_year+1):
            first_month = 1
            last_month = 12
            if year == start_year:
                first_month = start_month
            elif year == end_year:
                last_month = end_month
            cal.append((year,(last_month-first_month+1)))
        cal.sort(reverse=True)
        return cal

    def join_delta(self):
        periods = []
        for interval_start, interval_end in self.month_periods:
            jl_counts = self.mad.joinleave_counts(self.siteInfo.id,
                                            self.groupInfo.id,
                                            interval_start, interval_end)
            leave = jl_counts.get('gs.group.member.leave', 0)
            join = jl_counts.get('gs.group.member.join', 0)
            periods.append((interval_start.year, interval_start.month,
                            (join-leave)))
        return periods_as_dict(periods)

    def member_average(self):
        periods = []
        for interval_start, interval_end in self.month_periods:
            result = self.mad.average_member_count(self.siteInfo.id,
                                    self.groupInfo.id,
                                    interval_start, interval_end)
            
            periods.append((interval_start.year, interval_start.month,
                            round(result, 1)))
        
        return periods_as_dict(periods)

    def member_end_of_period(self):
        periods = []
        for interval_start, interval_end in self.month_periods:
            # we use the average member count for a single day
            result = self.mad.average_member_count(self.siteInfo.id,
                                    self.groupInfo.id,
                                    interval_end, interval_end)

            periods.append((interval_start.year, interval_start.month,
                            round(result, 1)))

        return periods_as_dict(periods)

    def percentage_members_posting(self):
        periods = []
        for interval_start, interval_end in self.month_periods:
            m_count = self.mad.average_member_count(self.siteInfo.id,
                                    self.groupInfo.id,
                                    interval_start, interval_end)

            a_count = self.gs.authors(self.siteInfo.id, self.groupInfo.id,
                                           interval_start,
                                           interval_end)

            percentage = 0.0
            if a_count and m_count:
                percentage = float(a_count)/float(m_count) * 100.0

            periods.append((interval_start.year, interval_start.month,
                            round(percentage, 1)))

        return periods_as_dict(periods)

    def posts(self):
        periods = []
        for interval_start, interval_end in self.month_periods:
            result = self.gs.posts(self.siteInfo.id, self.groupInfo.id,
                                              interval_start,
                                              interval_end)
            periods.append((interval_start.year, interval_start.month, result))
        return periods_as_dict(periods)

    def active_topics(self):
        periods = []
        for interval_start, interval_end in self.month_periods:
            result = self.gs.active_topics(self.siteInfo.id, self.groupInfo.id,
                                               interval_start,
                                               interval_end)
            periods.append((interval_start.year, interval_start.month, result))
        return periods_as_dict(periods)

    def percentage_single_post_topics(self):
        periods = []
        for interval_start, interval_end in self.month_periods:
            spt_count = self.gs.single_post_topics(self.siteInfo.id,
                                                   self.groupInfo.id,
                                                   interval_start,
                                                   interval_end)
            at_count = self.gs.active_topics(self.siteInfo.id,
                                               self.groupInfo.id,
                                               interval_start,
                                               interval_end)
            percentage = 0.0
            if at_count and spt_count:
                percentage = float(spt_count)/float(at_count) * 100.0
            periods.append((interval_start.year, interval_start.month,
                            round(percentage,1)))
        return periods_as_dict(periods)

    def authors(self):
        periods = []
        for interval_start, interval_end in self.month_periods:
            result = self.gs.authors(self.siteInfo.id, self.groupInfo.id,
                                           interval_start,
                                           interval_end)
            periods.append((interval_start.year, interval_start.month, result))
        return periods_as_dict(periods)

    def new_topics(self):
        periods = []
        for interval_start, interval_end in self.month_periods:
            result = self.gs.new_topics(self.siteInfo.id, self.groupInfo.id,
                                           interval_start,
                                           interval_end)
            periods.append((interval_start.year, interval_start.month, result))
        return periods_as_dict(periods)

    def average_dialogue_depth(self):
        periods = []
        for interval_start, interval_end in self.month_periods:
            mindepth, maxdepth, avgdepth = self.gs.dialogue_depths(
                                           self.siteInfo.id,
                                           self.groupInfo.id,
                                           interval_start,
                                           interval_end)
            periods.append((interval_start.year, interval_start.month,
                           round(avgdepth, 1)))
        
        return periods_as_dict(periods)

    def min_dialogue_depth(self):
        periods = []
        for interval_start, interval_end in self.month_periods:
            mindepth, maxdepth, avgdepth = self.gs.dialogue_depths(
                                           self.siteInfo.id,
                                           self.groupInfo.id,
                                           interval_start,
                                           interval_end)
            periods.append((interval_start.year, interval_start.month, mindepth))
        return periods_as_dict(periods)

    def max_dialogue_depth(self):
        periods = []
        for interval_start, interval_end in self.month_periods:
            mindepth, maxdepth, avgdepth = self.gs.dialogue_depths(
                                           self.siteInfo.id,
                                           self.groupInfo.id,
                                           interval_start,
                                           interval_end)
            periods.append((interval_start.year, interval_start.month, maxdepth))
        return periods_as_dict(periods)

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

    def join_delta(self):
        mad = MembersAtDate(self.context, self.context.zsqlalchemy)
        jl_counts = mad.joinleave_counts(self.siteInfo.id, self.groupInfo.id,
                                    self.interval_start, self.interval_end)
        leave = jl_counts.get('gs.group.member.leave', 0)
        join = jl_counts.get('gs.group.member.join', 0)
        
        return join-leave

    def member_average(self):
        mad = MembersAtDate(self.context, self.context.zsqlalchemy)
        return mad.average_member_count(self.siteInfo.id, self.groupInfo.id,
                                    self.interval_start, self.interval_end)

    def current_member_count(self):
        membersInfo = GSGroupMembersInfo(self.groupInfo.groupObj)
        return membersInfo.fullMemberCount

    def posts(self):
        result = self.groupStatsQuery.posts(self.siteInfo.id, self.groupInfo.id,
                                          self.interval_start,
                                          self.interval_end)
        return result  

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

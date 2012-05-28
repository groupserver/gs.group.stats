# coding=utf-8
import sqlalchemy as sa
import datetime

from gs.group.member.log.queries import JoinLeaveQuery

from gs.group.member.join.audit import JOIN_GROUP as JOIN
from gs.group.member.join.audit import SUBSYSTEM as JOIN_SUBSYSTEM
from gs.group.member.leave.audit import LEAVE
from gs.group.member.leave.audit import SUBSYSTEM as LEAVE_SUBSYSTEM
from Products.GSGroupMember.groupMembersInfo import GSGroupMembersInfo
from zope.component import createObject
from Products.XWFCore.XWFUtils import dt_to_user_timezone
from Products.XWFCore.cache import simplecache

from zope.cachedescriptors.property import Lazy

import pytz

import logging
#logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)

def ck_sid_gid_sp_ep(*args):
    self, site_id, group_id, start_period, end_period = args
    ck = ':'.join((self.da.getProperty('database'), site_id, group_id,
                   start_period.date().isoformat(),end_period.date().isoformat()))
    return ck

def ck_sid_gid(*args):
    self, site_id, group_id = args
    ck = ':'.join((self.da.getProperty('database'), site_id, group_id))

    return ck

class MembersAtDate(JoinLeaveQuery):
    def __init__(self, context, da):
        self.context = context
        self.da = da
        JoinLeaveQuery.__init__(self, None, da)
        self.auditEventTable = da.createTable('audit_event')
        self.user = self.context.REQUEST.get('AUTHENTICATED_USER')

        self.now = dt_to_user_timezone(context, datetime.datetime.now(pytz.utc),
                                       self.user)

    @simplecache('gs.group.stats.MembersAtDate.joinleave_counts', ck_sid_gid_sp_ep)
    def joinleave_counts(self, site_id, group_id, start_period, end_period):
        aet = self.auditEventTable
        
        start_period = dt_to_user_timezone(self.context, start_period,
                                           self.user)
        end_period = dt_to_user_timezone(self.context, end_period,
                                         self.user)
 
        s = sa.select([
          aet.c.subsystem,
          sa.func.count(aet.c.subsystem), 
        ], group_by=aet.c.subsystem)
        joinClauses = ((aet.c.subsystem == JOIN_SUBSYSTEM) & (aet.c.event_code == JOIN))
        leaveClauses = ((aet.c.subsystem == LEAVE_SUBSYSTEM) & (aet.c.event_code == LEAVE))
        s.append_whereclause(joinClauses | leaveClauses)
        s.append_whereclause(aet.c.group_id == group_id)
        s.append_whereclause(aet.c.site_id == site_id)
        s.append_whereclause(aet.c.event_date>=start_period)
        s.append_whereclause(aet.c.event_date<=end_period)
 
        r = s.execute()
        retval = {'gs.group.member.join': 0, 'gs.group.member.leave': 0}
        for result in r:
            subsystem, count = result
            assert subsystem in ('gs.group.member.join',
                                 'gs.group.member.leave')
            
            retval[subsystem] = count

        return retval # {'gs.group.member.join': COUNT, 'gs.group.member.leave': COUNT}

    @simplecache("gs.group.stats.MembersAtDate.average_member_count", ck_sid_gid_sp_ep)
    def average_member_count(self, site_id, group_id, start_period, end_period):
        """ The average over a period is a rather misleading concept, since
            it really depends on the interval at which the membership is
            calculated. In this function it is effectively the midpoint between
            start_period and end_period.

            A rolling average taken across the days/weeks/months between
            the start of period and now would be more accurate, but far
            more intensive to calculate.

        """
        groupInfo = createObject('groupserver.GroupInfo', self.context, group_id)

        membersInfo = GSGroupMembersInfo(groupInfo.groupObj)
        current_member_count = membersInfo.fullMemberCount
        
        # first we measure the number of joins and leaves since the end_period
        end_to_now = self.joinleave_counts(site_id, group_id, end_period, self.now)
        
        # then the leaves between the start and end
        start_to_end = self.joinleave_counts(site_id, group_id, start_period, end_period)
        endperiod_member_count = (current_member_count -
                                  end_to_now['gs.group.member.join'] +
                                  end_to_now['gs.group.member.leave'])
        startperiod_member_count = (endperiod_member_count -
                                  start_to_end['gs.group.member.join'] +
                                  start_to_end['gs.group.member.leave'])

        average_member_count = (startperiod_member_count+endperiod_member_count)/2.0
        
        return average_member_count

    @simplecache('gs.group.stats.MembersAtDate.earliest_member_record', ck_sid_gid)
    def earliest_member_record(self, site_id, group_id):
        aet = self.auditEventTable
        s = sa.select([
          sa.func.min(aet.c.event_date),
        ]) 
        joinClauses = ((aet.c.subsystem == JOIN_SUBSYSTEM) & (aet.c.event_code == JOIN))
        leaveClauses = ((aet.c.subsystem == LEAVE_SUBSYSTEM) & (aet.c.event_code == LEAVE))
        s.append_whereclause(joinClauses | leaveClauses)
        s.append_whereclause(aet.c.group_id == group_id)
        s.append_whereclause(aet.c.site_id == site_id)

        r = s.execute()
        if r.rowcount:
            return r.fetchone()[0]
        return None

class GroupStatsQuery(object):
    def __init__(self, da):
        self.da = da
        self.topicTable = da.createTable('topic')
        self.postTable  = da.createTable('post')
        self.auditTable = da.createTable('audit_event')

    @simplecache('gs.group.stats.GroupStatsQuery.posts_by_web', ck_sid_gid_sp_ep)
    def posts_by_web(self, site_id, group_id, start_period, end_period):
        t = self.auditTable
        s = t.select()
        
        s.append_whereclause(t.c.site_id==site_id)
        s.append_whereclause(t.c.group_id==group_id)
        s.append_whereclause(t.c.event_date>=start_period)
        s.append_whereclause(t.c.event_date<=end_period)
        s.append_whereclause(t.c.subsystem=='groupserver.WebPost')
        
        r = s.execute()
        retval = r.rowcount
        
        return retval

    @simplecache('gs.group.stats.GroupStatsQuery.posts', ck_sid_gid_sp_ep)
    def posts(self, site_id, group_id, start_period, end_period):
        t = self.postTable 
        s = t.select()

        s.append_whereclause(t.c.site_id==site_id)
        s.append_whereclause(t.c.group_id==group_id)
        s.append_whereclause(t.c.date>=start_period)
        s.append_whereclause(t.c.date<=end_period)
        
        r = s.execute()
        
        retval = r.rowcount
        
        return retval

    @simplecache('gs.group.stats.GroupStatsQuery.active_topics', ck_sid_gid_sp_ep)
    def active_topics(self, site_id, group_id, start_period, end_period):
        p = self.postTable
        s = sa.select([p.c.topic_id], distinct=True, group_by=p.c.topic_id)
        s.append_whereclause(p.c.site_id==site_id)
        s.append_whereclause(p.c.group_id==group_id)
        s.append_whereclause(p.c.date>=start_period)
        s.append_whereclause(p.c.date<=end_period)
        
        r = s.execute()
        retval = r.rowcount

        return retval

    @simplecache('gs.group.stats.GroupStatsQuery.single_post_topics', ck_sid_gid_sp_ep)
    def single_post_topics(self, site_id, group_id, start_period, end_period):
        p = self.postTable
        t = self.topicTable
        s = sa.select([p.c.topic_id], distinct=True, group_by=p.c.topic_id)
        s.append_whereclause(p.c.topic_id==t.c.topic_id)
        s.append_whereclause(t.c.num_posts==1)
        s.append_whereclause(p.c.site_id==site_id)
        s.append_whereclause(p.c.group_id==group_id)
        s.append_whereclause(p.c.date>=start_period)
        s.append_whereclause(p.c.date<=end_period)
        
        r = s.execute()
        retval = r.rowcount
        
        return retval

    @simplecache('gs.group.stats.GroupStatsQuery.dialogue_depths', ck_sid_gid_sp_ep)
    def dialogue_depths(self, site_id, group_id, start_period, end_period):
        p = self.postTable
        s = sa.select([sa.func.count(p.c.topic_id)], group_by=p.c.topic_id)
        s.append_whereclause(p.c.site_id==site_id)
        s.append_whereclause(p.c.group_id==group_id)
        s.append_whereclause(p.c.date>=start_period)
        s.append_whereclause(p.c.date<=end_period)
        
        r = s.execute()
        count = r.rowcount
        depths = []
        if count:
            for row in r:
                depths.append(row[0])

        total = sum(depths)
        avgdepth = 0; mindepth = 0; maxdepth = 0
        if count:
            avgdepth = float(total)/float(count) 
            mindepth = min(depths)
            maxdepth = max(depths)    
 
        return mindepth, maxdepth, avgdepth

    @simplecache('gs.group.stats.GroupStatsQuery.new_topics', ck_sid_gid_sp_ep)
    def new_topics(self, site_id, group_id, start_period, end_period):
        t = self.postTable

        s = sa.text("""select min_date from
           (select min(date) as min_date from post
                                         where group_id=:group_id and
                                               site_id=:site_id
                                         group by topic_id) as min_topic
         where min_topic.min_date>=:start_period and
               min_topic.min_date<=:end_period""", engine=t.engine)
        
        r = s.execute(site_id=site_id, group_id=group_id,
                      start_period=start_period, end_period=end_period)
        retval = r.rowcount

        return retval

    @simplecache('gs.group.stats.GroupStatsQuery.authors', ck_sid_gid_sp_ep)
    def authors(self, site_id, group_id, start_period, end_period):
        t = self.postTable
        s = sa.select([t.c.user_id], distinct=True)
        s.append_whereclause(t.c.site_id==site_id)
        s.append_whereclause(t.c.group_id==group_id)
        s.append_whereclause(t.c.date>=start_period)
        s.append_whereclause(t.c.date<=end_period)
        
        r = s.execute()
        retval = r.rowcount

        return retval

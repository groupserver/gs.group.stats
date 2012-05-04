# coding=utf-8
import sqlalchemy as sa

class GroupStatsQuery(object):
    def __init__(self, da):
        self.topicTable = da.createTable('topic')
        self.postTable  = da.createTable('post')
    
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

    def active_topics(self, site_id, group_id, start_period, end_period):
        t = self.topicTable
        s = t.select()

        s.append_whereclause(t.c.site_id==site_id)
        s.append_whereclause(t.c.group_id==group_id)
        s.append_whereclause(t.c.last_post_date>=start_period)
        s.append_whereclause(t.c.last_post_date<=end_period)
        
        r = s.execute()
        retval = r.rowcount

        return retval

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

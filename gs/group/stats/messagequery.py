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
from datetime import date
import sqlalchemy as sa
from gs.database import getSession
from Products.XWFMailingListManager.queries import MessageQuery as MLMQ


class MessageQuery(MLMQ):
    def posting_stats(self, site_id, group_ids=[]):
        retval = []

        pt = self.postTable

        s = sa.select([
          sa.extract('year', pt.c.date).label('year'),
          sa.extract('month', pt.c.date).label('month'),
          pt.c.site_id,
          pt.c.group_id,
          sa.func.count(pt.c.user_id.distinct()).label('user_count'),
          sa.func.count(pt.c.post_id).label('post_count'),
        ], group_by=('year', 'month', pt.c.site_id, pt.c.group_id),
           order_by=(sa.desc('year'), sa.desc('month'),
          pt.c.site_id, pt.c.group_id))
        aswc = MLMQ.__add_std_where_clauses
        aswc(self, s, pt, site_id, group_ids)

        session = getSession()
        r = session.execute(s)

        if r:
            rows = [{
              'year': int(x['year']),
              'month': int(x['month']),
              'site_id': x['site_id'],
              'group_id': x['group_id'],
              'post_count': x['post_count'],
              'user_count': x['user_count']
            } for x in r]

        years = {}
        for row in rows:
            if row['year'] not in years:
                years[row['year']] = {}
        for row in rows:
            years[row['year']][row['month']] = {'post_count': row['post_count']}
            years[row['year']][row['month']]['user_count'] = row['user_count']
        retval = years
        return retval

    def posts_per_day(self, groupId):
        pt = self.postTable
        cols = [
            sa.func.count(pt.c.post_id).label('n_posts'),
            sa.extract('day', pt.c.date).label('day'),
            sa.extract('month', pt.c.date).label('month'),
            sa.extract('year', pt.c.date).label('year')]

        s = sa.select(cols, group_by=('day', 'month', 'year'))
        s.append_whereclause(pt.c.group_id == groupId)

        session = getSession()
        r = session.execute(s)
        retval = [{
            'n_posts': x['n_posts'],
            'date': date(int(x['year']), int(x['month']), int(x['day']))
            } for x in r]
        return retval

    def posts_per_day_on_site(self, siteId):
        pt = self.postTable
        cols = [
            sa.func.count(pt.c.post_id).label('n_posts'),
            sa.extract('day', pt.c.date).label('day'),
            sa.extract('month', pt.c.date).label('month'),
            sa.extract('year', pt.c.date).label('year')]

        s = sa.select(cols, group_by=('day', 'month', 'year'))
        s.append_whereclause(pt.c.site_id == siteId)

        session = getSession()
        r = session.execute(s)
        retval = [{
            'n_posts': x['n_posts'],
            'date': date(int(x['year']), int(x['month']), int(x['day']))
            } for x in r]
        return retval

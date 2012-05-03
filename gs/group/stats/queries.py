# coding=utf-8
import sqlalchemy as sa

class GroupStatsQuery(object):
    def __init__(self, da):
        self.auditTable = da.createTable('audit_event')
        self.paymentRequestTable = da.createTable('payment_request') 
        self.subscriptionTable = da.createTable('subscription')

    def recently_started_sites(self, limit=10):
        at = self.auditTable
        s = sa.select([at.c.site_id, at.c.event_date])
        s.append_whereclause(at.c.subsystem=='ogn.site.start')
        s.append_whereclause(at.c.event_code=='1')
        s.order_by(sa.desc(at.c.event_date))
        s.limit = limit
        r = s.execute()
        
        retval = [{'siteId': x['site_id'], 'date': x['event_date']}
                    for x in r]
        assert type(retval) == list
        return retval

    def subscription_count_at_monies(self):
        prt = self.paymentRequestTable
        st = self.subscriptionTable
        # select amount_request, count(amount_request) 
        #     from payment_request, subscription 
        #     where subscription.cancelled is null 
        #         and payment_request.cancelled is null 
        #         and payment_request.site_id = subscription.site_id 
        #     group by amount_request 
        #     order by count desc;
        cols = [prt.c.amount_request, 
                sa.func.count(prt.c.amount_request).label('count')]
        s = sa.select(cols)
        s.append_whereclause(prt.c.cancelled == None)
        s.append_whereclause(st.c.cancelled == None)
        s.append_whereclause(prt.c.site_id == st.c.site_id)
        s.group_by(prt.c.amount_request)
        s.order_by(prt.c.amount_request)
        
        r = s.execute()
        retval = [{ 'amount':   x['amount_request'], 
                    'count':    x['count'] } for x in r]
        assert type(retval) == list
        return retval

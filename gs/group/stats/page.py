from gs.content.base.page import SitePage
from zope.component import createObject
from zope.cachedescriptors.property import Lazy

class GroupStatsView(SitePage):
    def __init__(self, context, request):
        SitePage.__init__(self, context, request)

    @Lazy
    def groupInfo(self):
        retval = createObject('groupserver.GroupInfo', self.context)
        assert retval, 'Could not create the GroupInfo from %s' % self.context
        return retval

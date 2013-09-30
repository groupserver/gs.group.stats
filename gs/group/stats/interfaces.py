# coding=utf-8
from zope.schema import ASCIILine
from zope.interface import Interface
from zope.contentprovider.interfaces import IContentProvider

class IGSGroupStatsContentProvider( IContentProvider ):
    groupId = ASCIILine(title=u'Group Identifier',
        description=u'The identifier for the group',
        required=True)

    siteId = ASCIILine(title=u'Site Identifier',
        description=u'The identifier for the site',
        required=True)

    pageTemplateFileName = ASCIILine(title=u"Page Template File Name",
        description=u'The name of the ZPT file that is used to '\
        u'render the status message.',
        required=False,
        default="browser/templates/groupstatscontentprovider.pt")

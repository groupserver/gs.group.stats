# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2016 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
############################################################################
from __future__ import absolute_import, unicode_literals, print_function
from mock import (MagicMock, patch)  # , PropertyMock)
from unittest import TestCase
from gs.group.stats.contentprovider import (GroupStatsContentProvider, )


class TestGroupStatsContentProvider(TestCase):
    '''Test the ``GroupStatsContentProvider`` class'''

    @patch('gs.group.stats.contentprovider.createObject')
    def test_groupInfo_id(self, m_cO):
        'Test that we cope with a group-identifier being passed in'
        context = MagicMock()
        a = GroupStatsContentProvider(context, MagicMock(), MagicMock())
        a.groupId = 'example'
        r = a.groupInfo

        self.assertEqual(m_cO.return_value, r)
        m_cO.assert_called_once_with('groupserver.GroupInfo', context, 'example')

    @patch('gs.group.stats.contentprovider.createObject')
    def test_groupInfo_id_none(self, m_cO):
        'Test that we cope with a group-identifier being set to ``None``'
        context = MagicMock()
        a = GroupStatsContentProvider(context, MagicMock(), MagicMock())
        a.groupId = None
        r = a.groupInfo

        self.assertEqual(m_cO.return_value, r)
        m_cO.assert_called_once_with('groupserver.GroupInfo', context)

    @patch('gs.group.stats.contentprovider.createObject')
    def test_groupInfo_id_gone(self, m_cO):
        'Test that we cope with an absent group-identifier'
        context = MagicMock()
        a = GroupStatsContentProvider(context, MagicMock(), MagicMock())
        r = a.groupInfo

        self.assertEqual(m_cO.return_value, r)
        m_cO.assert_called_once_with('groupserver.GroupInfo', context)

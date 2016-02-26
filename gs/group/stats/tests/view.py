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
from mock import (MagicMock, patch, PropertyMock)
from unittest import TestCase
from gs.group.stats.view import (GSGroupStatsView, )


class TestGSGroupStatsView(TestCase):
    '''Test the ``GSGroupStatsView`` class'''

    @patch.object(GSGroupStatsView, 'stats', new_callable=PropertyMock)
    def test_years(self, m_s):
        'Test that that the post-stats are sorted by year'
        m_s.return_value = {2014: 'data', 2016: 'is', 2015: 'fun', }
        g = GSGroupStatsView(MagicMock(), MagicMock())
        r = g.years

        self.assertEqual(3, len(r))
        self.assertEqual(2016, r[0])
        self.assertEqual(2014, r[-1])

    @patch.object(GSGroupStatsView, 'stats', new_callable=PropertyMock)
    def test_get_months_none(self, m_s):
        'Test that we get an empty dict if we lack the year'
        m_s.return_value = {2014: 'data', 2016: 'is', 2015: 'fun', }
        g = GSGroupStatsView(MagicMock(), MagicMock())
        r = g.get_months(2013)

        self.assertEqual({}, r)

    @patch.object(GSGroupStatsView, 'stats', new_callable=PropertyMock)
    def test_get_months(self, m_s):
        'Test that we get an empty dict if we lack the year'
        m_s.return_value = {2014: 'data', 2016: 'is', 2015: 'fun', }
        g = GSGroupStatsView(MagicMock(), MagicMock())
        r = g.get_months(2014)

        self.assertEqual('data', r)

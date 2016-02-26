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
from datetime import date
from mock import (MagicMock, patch, PropertyMock)
from unittest import TestCase
from gs.group.stats.posting import (GroupPostingStats, )


class TestGroupPostingStats(TestCase):
    '''Test the ``GroupPostingStats`` class'''
    @staticmethod
    def stat(d, n):
        retval = {'date': d, 'n_posts': n}
        return retval

    @patch.object(GroupPostingStats, 'query', new_callable=PropertyMock)
    def test_postStats(self, m_q):
        'Test that that the post-stats are sorted by date'
        m_q().posts_per_day.return_value = [
            self.stat(date(2016, 2, 1), 5), self.stat(date(2016, 1, 1), 7),
            self.stat(date(2016, 3, 1), 2), self.stat(date(2015, 12, 1), 9)]
        g = GroupPostingStats(MagicMock())
        r = g.postStats

        self.assertEqual(4, len(r))
        self.assertEqual(9, r[0]['n_posts'])  # The 2015-12-01 entry
        self.assertEqual(2, r[-1]['n_posts'])  # The 2016-03-01 entry

    @patch.object(GroupPostingStats, 'postStats', new_callable=PropertyMock)
    def test_meanPerDay_none(self, m_pS):
        'Test the mean posts-per-day value if there is no time-difference'
        m_pS.return_value = [self.stat(date(2016, 2, 1), 5), ]
        g = GroupPostingStats(MagicMock())
        r = g.meanPerDay

        self.assertEqual(0.0, r)

    @patch.object(GroupPostingStats, 'postStats', new_callable=PropertyMock)
    def test_meanPerDay(self, m_pS):
        'Test the mean posts-per-day'
        m_pS.return_value = [
            self.stat(date(2016, 2, 26), 6), self.stat(date(2016, 2, 27), 7),
            self.stat(date(2016, 2, 28), 5), self.stat(date(2016, 2, 29), 9), ]
        g = GroupPostingStats(MagicMock())
        r = g.meanPerDay

        self.assertEqual(9, r)

    @patch.object(GroupPostingStats, 'meanPerDay', new_callable=PropertyMock)
    def test_intMeanPerDay_round_up(self, m_mPD):
        'Test the mean posts-per-day round up'
        m_mPD.return_value = 5.6
        g = GroupPostingStats(MagicMock())
        r = g.intMeanPerDay

        self.assertEqual(6, r)

    @patch.object(GroupPostingStats, 'meanPerDay', new_callable=PropertyMock)
    def test_intMeanPerDay_round_down(self, m_mPD):
        'Test the mean posts-per-day round down'
        m_mPD.return_value = 5.4
        g = GroupPostingStats(MagicMock())
        r = g.intMeanPerDay

        self.assertEqual(5, r)

    @patch.object(GroupPostingStats, 'postStats', new_callable=PropertyMock)
    def test_minPerDay(self, m_pS):
        'Test the minPerDay property'
        m_pS.return_value = [
            self.stat(date(2016, 2, 26), 6), self.stat(date(2016, 2, 27), 7),
            self.stat(date(2016, 2, 28), 5), self.stat(date(2016, 2, 29), 9), ]
        g = GroupPostingStats(MagicMock())
        r = g.minPerDay

        self.assertEqual(5, r)

    @patch.object(GroupPostingStats, 'postStats', new_callable=PropertyMock)
    def test_maxPerDay(self, m_pS):
        'Test the maxPerDay property'
        m_pS.return_value = [
            self.stat(date(2016, 2, 26), 6), self.stat(date(2016, 2, 27), 7),
            self.stat(date(2016, 2, 28), 5), self.stat(date(2016, 2, 29), 9), ]
        g = GroupPostingStats(MagicMock())
        r = g.maxPerDay

        self.assertEqual(9, r)

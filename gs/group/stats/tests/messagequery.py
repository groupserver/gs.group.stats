# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2016 Michael JasonSmith and Contributors.
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
# from mock import (MagicMock, )  # patch, ) # PropertyMock)
from unittest import TestCase
from gs.group.stats.messagequery import (MessageQuery, YearDict, )


class TestYearDict(TestCase):

    def test_ordered(self):
        'Test that the YearDict is an ordered dictionary'
        y = YearDict()
        y[2] = 'foo'
        y[1] = 'bar'
        y[3] = 'wibble'

        self.assertEqual([2, 1, 3], list(y))

    def test_present(self):
        'Assert we get out what we put in'
        y = YearDict()
        month = {'post_count': 7, 'user_count': 10, }
        y[1] = month

        self.assertEqual(month, y[1])

    def test_missing(self):
        'Assert we get the correct missing values'
        y = YearDict()
        month = {'post_count': 7, 'user_count': 10, }
        y[1] = month

        expected = {'post_count': 0, 'user_count': 0, }
        self.assertEqual(expected, y[2])

    def test_not_a_month(self):
        'Assert we handle non-months'
        y = YearDict()
        month = {'post_count': 7, 'user_count': 10, }
        y[1] = month

        with self.assertRaises(KeyError):
            y[13]


class TestMessageQuery(TestCase):
    '''Test the ``MessageQuery`` class'''
    #: The statistics for GroupServer Development in 2010, 2011, and January 2012
    rows = [
        {'year': '2012', 'month': '1', 'site_id': 'groupserver', 'group_id': 'development',
         'post_count': 7, 'user_count': 10},
        {'year': '2011', 'month': '12', 'site_id': 'groupserver', 'group_id': 'development',
         'post_count': 6, 'user_count': 17},
        {'year': '2011', 'month': '11', 'site_id': 'groupserver', 'group_id': 'development',
         'post_count': 8, 'user_count': 15},
        {'year': '2011', 'month': '10', 'site_id': 'groupserver', 'group_id': 'development',
         'post_count': 10, 'user_count': 27},
        {'year': '2011', 'month': '9', 'site_id': 'groupserver', 'group_id': 'development',
         'post_count': 7, 'user_count': 39},
        {'year': '2011', 'month': '8', 'site_id': 'groupserver', 'group_id': 'development',
         'post_count': 11, 'user_count': 47},
        {'year': '2011', 'month': '7', 'site_id': 'groupserver', 'group_id': 'development',
         'post_count': 11, 'user_count': 79},
        {'year': '2011', 'month': '6', 'site_id': 'groupserver', 'group_id': 'development',
         'post_count': 7, 'user_count': 87},
        {'year': '2011', 'month': '5', 'site_id': 'groupserver', 'group_id': 'development',
         'post_count': 7, 'user_count': 38},
        {'year': '2011', 'month': '4', 'site_id': 'groupserver', 'group_id': 'development',
         'post_count': 7, 'user_count': 29},
        {'year': '2011', 'month': '3', 'site_id': 'groupserver', 'group_id': 'development',
         'post_count': 7, 'user_count': 61},
        {'year': '2011', 'month': '2', 'site_id': 'groupserver', 'group_id': 'development',
         'post_count': 7, 'user_count': 38},
        {'year': '2011', 'month': '1', 'site_id': 'groupserver', 'group_id': 'development',
         'post_count': 5, 'user_count': 12},
        {'year': '2010', 'month': '12', 'site_id': 'groupserver', 'group_id': 'development',
         'post_count': 6, 'user_count': 26},
        {'year': '2010', 'month': '11', 'site_id': 'groupserver', 'group_id': 'development',
         'post_count': 9, 'user_count': 70},
        {'year': '2010', 'month': '10', 'site_id': 'groupserver', 'group_id': 'development',
         'post_count': 6, 'user_count': 58},
        {'year': '2010', 'month': '9', 'site_id': 'groupserver', 'group_id': 'development',
         'post_count': 9, 'user_count': 103},
        {'year': '2010', 'month': '8', 'site_id': 'groupserver', 'group_id': 'development',
         'post_count': 4, 'user_count': 27},
        {'year': '2010', 'month': '7', 'site_id': 'groupserver', 'group_id': 'development',
         'post_count': 6, 'user_count': 26},
        {'year': '2010', 'month': '6', 'site_id': 'groupserver', 'group_id': 'development',
         'post_count': 4, 'user_count': 21},
        {'year': '2010', 'month': '5', 'site_id': 'groupserver', 'group_id': 'development',
         'post_count': 4, 'user_count': 12},
        {'year': '2010', 'month': '4', 'site_id': 'groupserver', 'group_id': 'development',
         'post_count': 6, 'user_count': 42},
        {'year': '2010', 'month': '3', 'site_id': 'groupserver', 'group_id': 'development',
         'post_count': 1, 'user_count': 1},
        {'year': '2010', 'month': '2', 'site_id': 'groupserver', 'group_id': 'development',
         'post_count': 1, 'user_count': 3},
        {'year': '2010', 'month': '1', 'site_id': 'groupserver', 'group_id': 'development',
         'post_count': 1, 'user_count': 1},
    ]

    def test_marshal_posting_stats_years(self):
        'Test we get the right years back'
        r = MessageQuery.marshal_posting_stats(self.rows)

        self.assertEqual(3, len(r))  # 3 years
        self.assertEqual([2012, 2011, 2010], list(r))  # In decending order

    def test_marshal_posting_stats_months(self):
        'Test we get the right months back'
        r = MessageQuery.marshal_posting_stats(self.rows)

        self.assertEqual(12, len(r[2011]))
        self.assertEqual(list(range(12, 0, -1)), list(r[2011]))

    def test_marshal_posting_stats_values(self):
        'Ensure we get the right month values back'
        r = MessageQuery.marshal_posting_stats(self.rows)

        expected = {'post_count': 7, 'user_count': 10, }
        self.assertEqual(expected, r[2012][1])
        # The missing value
        expected = {'post_count': 0, 'user_count': 0, }
        self.assertEqual(expected, r[2012][2])

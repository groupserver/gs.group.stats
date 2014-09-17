==================
``gs.group.stats``
==================
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Usage statistics for a GroupServer group
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Author: `Michael JasonSmith`_
:Contact: Michael JasonSmith <mpj17@onlinegroups.net>
:Date: 2013-10-02
:Organization: `GroupServer.org`_
:Copyright: This document is licensed under a
  `Creative Commons Attribution-Share Alike 3.0 New Zealand License`_
  by `OnlineGroups.Net`_.

Introduction
============

This product provides a page providing the statistics for a GroupServer_
group. I consists of three components: a page_, a `content provider`_, and
a class_ that provides the statistics.

Page
====

The page ``stats.html``, in the Group context, provides a summary of the
posting statistics in a group. It shows a table, with the number of posts
made each month, and the number of distinct authors each month. 

In addition ``stats.csv`` presents the same information as the page, but in
a CSV format that is suitable for use in a spreadsheet.

Content provider
================

The ``groupserver.GroupStats`` gives a sense of how busy the group is. It
displays a ``<span>`` that contains information on

* The current number of members,
* The mean number of posts,  and.
* The maximum number of posts.

The maximum number of posts is used to give a sense of the
standard-deviation about the mean. The latter was considered a touch too
complex for a general-purpose content provider.

To use the content provider from *within* the group context call it as
follows::

      <p tal:content="structure provider:groupserver.GroupStats">
        Summary of the stats
      </p>

Unusually, the content provider can be used from *outside* the group
context, by passing ``groupId`` to the content provider::

      <p define="groupId view/groupInfo/id"
         tal:content="structure provider:groupserver.GroupStats">
        Summary of the stats
      </p>

Class
=====

The class ``gs.group.stats.GroupPostingStats`` provides some
posting-statistics for the group. The class takes a group-info as the
argument to ``__init__``, and provides the following properties.

:``digestMembers``:
   The number of members that receive the daily-digest of topics.

:``webonlyMembers``:
   The number of members that follow the group using the Web only.

:``postsExist``:
  ``True`` if any post has been made to the group.

:``minPerDay``:
  The *minimum* number of posts per day.

:``maxPerDay``:
  The *maximum* number posts per day.

:``meanPerDay``:
  The *mean* number of posts per day, as a float.

:``intMeanPerDay``:
  The *mean* number of posts per day, as an integer rounded.

:``postStats``:
   The raw posts-per-day data, as a list of dictionaries:
   
   * ``n_posts``: The number of posts
   * ``date``: The date.

Resources
=========

- Code repository: https://source.iopen.net/groupserver/gs.site.stats/
- Questions and comments to http://groupserver.org/groups/development/
- Report bugs at https://redmine.iopen.net/projects/groupserver/

.. _GroupServer.org: http://groupserver.org/
.. _Michael JasonSmith: http://groupserver.org/p/mpj17
.. _Creative Commons Attribution-Share Alike 3.0 New Zealand License:
   http://creativecommons.org/licenses/by-sa/3.0/nz/
.. _GroupServer: http://groupserver.org/
.. _OnlineGroups.net: http://onlinegroups.net/

.. [#group] See <http://source.iopen.net/groupserver/gs.group.stats/>

..  LocalWords:  html groupserver GroupStats GroupPostingStats LocalWords
..  LocalWords:  GroupStatsExtended init postsExist minPerDay maxPerDay
..  LocalWords:  meanPerDay intMeanPerDay postStats csv digestMembers
..  LocalWords:  webonlyMembers

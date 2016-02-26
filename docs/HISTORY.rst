Changelog
=========

3.2.0 (2016-02-26)
------------------

* Adding internationalisation support
* Following the changes to `gs.group.member.base`_
* Adding unit tests

.. _gs.group.member.base:
   https://github.com/groupserver/gs.group.member.base

3.1.0 (2015-06-15)
------------------

* Naming the reStructuredText files as such
* Using GitHub_ as the primary code repository
* Closing a memory leak
* Following the change to `gs.group.member.leave.base`_

.. _GitHub: https://github.com/groupserver/gs.group.stats
.. _gs.group.member.leave.base:
   https://github.com/groupserver/gs.group.member.leave.base

3.0.0 (2012-10-02)
------------------

* Adding the group-stats view and content provider to this
  product
* Exposing the ``MessageQuery``, ``GroupPostingStats``,
  ``MembersAtDate``, and ``GroupStatsQery`` classes
* Rejigging the queries
* Cleaning up the code

2.0.0 (2012-08-29)
------------------

* Providing stats about adding posts via the Web

1.2.0 (2012-07-19)
------------------

* Moving the instance-identifier to `gs.config`_

.. _gs.config: https://github.com/groupserver/gs.config

1.1.0 (2012-06-22)
------------------

* Updating SQLAlchemy

1.0.0 (2012-06-06)
------------------

Initial version. Prior to the creation of this product group
statistics was provided by ``Products.GSParticipationStats``

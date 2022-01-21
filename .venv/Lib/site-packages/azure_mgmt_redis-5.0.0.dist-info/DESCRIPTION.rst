Microsoft Azure SDK for Python
==============================

This is the Microsoft Azure Redis Cache Management Client Library.

Azure Resource Manager (ARM) is the next generation of management APIs that
replace the old Azure Service Management (ASM).

This package has been tested with Python 2.7, 3.4, 3.5 and 3.6.

For the older Azure Service Management (ASM) libraries, see
`azure-servicemanagement-legacy <https://pypi.python.org/pypi/azure-servicemanagement-legacy>`__ library.

For a more complete set of Azure libraries, see the `azure <https://pypi.python.org/pypi/azure>`__ bundle package.


Compatibility
=============

**IMPORTANT**: If you have an earlier version of the azure package
(version < 1.0), you should uninstall it before installing this package.

You can check the version using pip:

.. code:: shell

    pip freeze

If you see azure==0.11.0 (or any version below 1.0), uninstall it first:

.. code:: shell

    pip uninstall azure


Usage
=====

For code examples, see `Redis Cache Management
<https://docs.microsoft.com/python/api/overview/azure/redis>`__
on docs.microsoft.com.


Provide Feedback
================

If you encounter any bugs or have suggestions, please file an issue in the
`Issues <https://github.com/Azure/azure-sdk-for-python/issues>`__
section of the project.


.. :changelog:

Release History
===============

5.0.0 (2018-02-08)
++++++++++++++++++

**Disclaimer**

Several model (like RedisCreateParameters) have positional arguments shuffled, due to constraints
in our code generator. This is not breaking if you use keyword arguments. If you are using 
positional arguments, we strongly suggest to use keyword only arguments for Model creation, since
next version 6.0.0 will use keyword only arguments for models.

**Breaking changes**

- RedisCreateParameters parameters orders shuffled (see disclaimer)
- RedisUpdateParameters parameters orders shuffled (see disclaimer)
- Merging redis_firewall_rule operations group into firewall_rules
- Rename firewall_rules.list to firewall_rules.list_by_redis_resource

**Features**

- All operation groups have now a "models" attribute
- Add linked_server operations group

New ApiVersion 2017-10-01

4.1.1 (2017-10-25)
++++++++++++++++++

**Bugfixes**

- Fix "tags" attribute in redis update

4.1.0 (2017-04-18)
++++++++++++++++++

**Features**

- Add firewall rules operations

**Notes**

- This wheel package is now built with the azure wheel extension

4.0.0 (2017-01-13)
++++++++++++++++++

**Bugfixes**

* Fix error if patching when not exist

**Breaking change**

* `redis.update` is no longer an async operation

3.0.0 (2016-11-14)
++++++++++++++++++

**New features**

* Add "Everyday" and "Weekend" to schedule enums
* Improve technical documention

**Breaking change**

* Simplify `patch_schedules.create_or_update` parameters

2.0.0 (2016-10-20)
++++++++++++++++++

* Major bug fixes and refactoring.

1.0.0 (2016-08-09)
++++++++++++++++++

* Initial Release (API Version 2016-04-01)



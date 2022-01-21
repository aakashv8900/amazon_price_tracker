Microsoft Azure SDK for Python
==============================

This is the Microsoft Azure Commerce Client Library.

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

For code examples, see `Commerce
<https://docs.microsoft.com/python/api/overview/azure/commerce>`__
on docs.microsoft.com.


Provide Feedback
================

If you encounter any bugs or have suggestions, please file an issue in the
`Issues <https://github.com/Azure/azure-sdk-for-python/issues>`__
section of the project.


.. :changelog:

Release History
===============

1.0.1 (2018-02-21)
++++++++++++++++++

- usage_aggregation.quantity is now correctly declared as float
- All operation groups have now a "models" attribute

1.0.0 (2017-06-23)
++++++++++++++++++

* Initial stable release

This wheel package is now built with the azure wheel extension

If moved from 0.30.0rc6, expect some tiny renaming like (not exhaustive):

- reportedstart_time renamed to reported_start_time
- self.Name renamed to self.name in some classes



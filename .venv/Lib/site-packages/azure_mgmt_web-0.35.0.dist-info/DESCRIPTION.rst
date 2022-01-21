Microsoft Azure SDK for Python
==============================

This is the Microsoft Azure Web Apps Management Client Library.

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

For code examples, see `Web Apps Management
<https://docs.microsoft.com/python/azure/>`__
on docs.microsoft.com.


Provide Feedback
================

If you encounter any bugs or have suggestions, please file an issue in the
`Issues <https://github.com/Azure/azure-sdk-for-python/issues>`__
section of the project.


.. :changelog:

Release History
===============

0.35.0 (2018-02-20)
+++++++++++++++++++

**Breaking changes**

- Many models signature changed to expose correctly required parameters. Example (non exhaustive) list:

  - AppServiceCertificateOrderPatchResource now requires product_type
  - AppServicePlanPatchResource now requires app_service_plan_patch_resource_name
  - CertificatePatchResource now requires password
  - DomainPatchResource now requires contact_admin, contact_billing, contact_registrant, contact_tech, consent
  - MigrateMySqlRequest now requires connection_string, migration_type
  - PushSettings now requires is_push_enabled

- get_available_stacks now returns a pageable object

**Features**

- Add certificate_registration_provider operations group
- Add Diagnostics operations group
- Add domain registration provider operations groups
- All operations group have now a "models" attribute


0.34.1 (2017-10-24)
+++++++++++++++++++

- MSI fixes

0.34.0 (2017-10-16)
+++++++++++++++++++

- Add MSI support

0.33.0 (2017-10-04)
+++++++++++++++++++

**Features**

- Add providers.list_operations
- Add verify_hosting_environment_vnet
- Add web_apps.list_sync_function_triggers
- Add web_apps.list_processes
- Add web_apps.get_instance_process_module
- Add web_apps.delete_process
- Add web_apps.get_process_dump
- Add web_apps continous web job operations
- Add web_apps continous web job slots operations
- Add web_apps public certificate operations
- Add web_apps site_extension operations
- Add web_apps functions operations
- Add web_apps.list_function_secrets
- Add web_apps.list_deployment_log
- Add web_apps.list_deployment_log_slot
- Add web_apps ms_deploy_status operations
- Add web_apps ms_deploy_status_slot operations
- Add web_apps ms_deploy_log_slot operations
- Add web_apps instance_process_modules operations
- Add web_apps instance_process_threads operations
- Add web_apps instance_process_slot operations
- Add web_apps instance_process_modules_slot operations
- Add web_apps instance_process_threads_slot operations
- Add web_apps.list_sync_function_triggers_slot
- Add web_apps processes_slot operations
- Add web_apps site_extensions_slot operations
- Add web_apps triggered_web_jobs_slot operations
- Add web_apps web_jobs_slot operations
- Add web_apps triggered_web_jobs operations
- Add web_apps web_jobs operations
- Add web_apps.is_cloneable

**Breaking changes**

- Remove 'name' and 'type' from several models (was ignored by server as read-only parameters)
- Remove completely 'location' parameter from several models (None was the only acceptable value)
- Remove a lot of incorrect parameter into DeletedSite
- Remove deleted_web_apps.list_by_resource_group
- Change web_apps.update_application_settings method signature
- Change web_apps.update_connection_strings method signature
- Change web_apps.update_metadata method signature
- web_apps.recover now recover from a delete app to a previous snapshot
- web_apps.recover_slot now recover from a delete app to a previous snapshot

0.32.0 (2017-04-26)
+++++++++++++++++++

* Support list web runtime stacks
* Expose non resource based model type for SiteConfig, SiteAuthSettings, etc, to be used as property
* Support list linux web available regions

0.31.1 (2017-04-20)
+++++++++++++++++++

This wheel package is now built with the azure wheel extension

0.31.0 (2017-02-13)
+++++++++++++++++++

* Major refactoring and breaking changes
* New API Version

0.30.0 (2016-10-17)
+++++++++++++++++++

* Initial release



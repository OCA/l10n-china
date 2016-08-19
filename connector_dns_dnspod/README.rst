.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

====================
Connector Dns Dnspod
====================

This module aims to allows you to manage your DNSPod domain through Odoo.

Installation
============

To install this module, you need to:

 * have basic modules installed (connector_dns)

Configuration
=============

To configure this module, you need to:

 * No specific configuration needed.

Usage
=====

To use this module, you need to:
#. Create a backend which links to your dnspod.cn.
#. When you create a domain belongs to the backend,if the domain
   export to the dnspod.cn successfully,the state will change to
   done,else exception.
#. Record can be created only in the domain which state is done.

Known issues / Roadmap
======================

* This connector is only compatible with dnspod.cn and not dnspod.com which has a different API.
Add a line note

Credits
=======


Contributors
------------

* Eric Caudal <eric.caudal@elico-corp.com>
* Noah Wang <noah.wang@elico-corp.com>
* Liu Lixia <liu.lixia@elico-corp.com>
* Augustin Cisterne-Kaas

Maintainer
----------

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization
    whose mission is to support the collaborative development of Odoo features
        and promote its widespread use.

To contribute to this module, please visit https://odoo-community.org.
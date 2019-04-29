After you installed this module, you need to create DNS Backend and get DNSPod API Token first.

#. Create DNS Backend

    * Open menu Connectors / DNS Backend / Backend
    * Create a new backend
    * Get Token ID and Login Token follow step 2
    * Save backend record

    .. figure:: ../static/img/dns_backend.png
       :width: 600 px
       :alt: Create DNS Backend

#. Get DNSPod API Token

    * Login to the DNSPod `dashboard`_
    * Go to the menu `Security Settings`_
    * Find API Token section and click View button
    * Click button Create API Token
    * Input token name and click Confirm
    * Copy & paste the ID and Token into the backend

#. Create Domain and get subdomains

    * Go to Connectors / DNS Backend / DNS Domains
    * Add your domain name and select backend
    * Save & Connect
    * Click button Get Subdomains to get all records

    .. figure:: ../static/img/dns_domain.png
       :width: 600 px
       :alt: Create DNS Domain
    
#. Create DNS records

    * Go to Connectors / DNS Backend / DNSPod Records
    * Click Create
    * Fill all fields

    .. figure:: ../static/img/dns_records.png
       :width: 600 px
       :alt: DNSPod Records

.. _dashboard: https://www.dnspod.cn/console/dashboard
.. _Security Settings: https://www.dnspod.cn/console/user/security

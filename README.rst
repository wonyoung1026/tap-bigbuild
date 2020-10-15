===============================
bigbuild
===============================

.. image:: https://badge.fury.io/py/bigbuild.png
    :target: http://badge.fury.io/py/bigbuild

.. image:: https://travis-ci.org/wonyoung1026/bigbuild.png?branch=master
        :target: https://travis-ci.org/wonyoung1026/bigbuild

.. image:: https://pypip.in/d/bigbuild/badge.png
        :target: https://crate.io/packages/bigbuild?version=latest


TAP big build project tool

Dashboard
--------
refer to `link <https://kubernetes.io/docs/reference/access-authn-authz/authentication/>`_

- kubectl apply -f bigbuild/kubernetes/yaml/dashboard.yaml

- kubectl apply -f bigbuild/kubernetes/yaml/dashboard-adminuser.yaml

- kubectl -n kubernetes-dashboard describe secret $(kubectl -n kubernetes-dashboard get secret | grep admin-user | awk '{print $1}')

- kubectl proxy

- http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/


Clean dashboard
--------

- kubectl -n kubernetes-dashboard delete serviceaccount admin-user

- kubectl -n kubernetes-dashboard delete clusterrolebinding admin-user


Ingress bare metal LB
----------
refer to `link <https://kubernetes.github.io/ingress-nginx/deploy/#bare-metal>`_



Requirements
------------

- Python >= 2.6 or >= 3.3
- Kubernetes / Weave, Docker

License
-------

MIT licensed. See the bundled `LICENSE <https://github.com/wonyoung1026/tap-bigbuild/blob/master/LICENSE>`_ file for more details.

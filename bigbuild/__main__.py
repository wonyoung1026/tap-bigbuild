#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''

Usage:
  bigbuild (describe|deploy|destroy|log) app <user-id> <app-id>
  bigbuild list apps <user-id>
  bigbuild scale (up|down) <user-id> <app-id> [-n=<num>]

  bigbuild -h | --help
  bigbuild --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  -n=<num>            Increment/decrement number [default: 1].
'''

from __future__ import unicode_literals, print_function
from docopt import docopt

from . import commands 
__version__ = "0.2.0"
__author__ = "Won Jung"
__license__ = "MIT"


def main():
    '''Main entry point for the bigbuild CLI.'''
    args = docopt(__doc__, version=__version__)
    commands.process_args(args)

if __name__ == '__main__':
    main()

# cat <<EOF | kubectl apply -f -
# apiVersion: v1
# kind: Namespace
# metadata:
#   name: user--wonyoung1026
# EOF

# cat <<EOF | kubectl apply -f -
# apiVersion: apps/v1
# kind: Deployment
# metadata:
#   name: kube-django
#   namespace: user--wonyoung1026
#   labels:
#     app: kube-django
# spec:
#   replicas: 3
#   selector:
#     matchLabels:
#       app: kube-django
#   template:
#     metadata:
#       labels:
#         app: kube-django
#     spec:
#       containers:
#       - name: kube-django
#         image: wonyoung1026/kube-django
#         imagePullPolicy: Always
#         ports:
#         - containerPort: 8000
# EOF

# # get free port 

# cat <<EOF | kubectl apply -f -
# apiVersion: v1
# kind: Service
# metadata:
#   name: kube-django
#   labels:
#     run: kube-django
#   namespace: user--wonyoung1026
# spec:
#   type: NodePort
#   ports:
#   - port: 8000
#     targetPort: 8000
#     protocol: TCP
#   selector:
#     run: kube-django
# EOF
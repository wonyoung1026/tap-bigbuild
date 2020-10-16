from . import utils as k8utils

USER_NAMESPACE_PREFIX = 'user--'

def process_args(args):
    # print(args)
    # ------------------------------------
    #   bigbuild deploy app <user-id> <app-id> <image> <port> [-r=<num>]
    # ------------------------------------
    if args.get("deploy") and args.get("app"):
        return deploy_app(uid=args.get('<user-id>'), aid=args.get('<app-id>'),
            image=args.get('<image>'), port=args.get('<port>'), replicas=args.get('-r')
        )
    
    # ------------------------------------
    #   bigbuild get port <user-id> <app-id>
    # ------------------------------------
    if args.get("get") and args.get("port"):
        return get_service_port(uid=args.get('<user-id>'), aid=args.get('<app-id>'))


    # ------------------------------------
    #   bigbuild (describe|deploy|destroy|log) app <user-id> <app-id>
    # ------------------------------------
    if args.get("describe") and args.get("app"):
        return describe_app(uid=args.get('<user-id>'), aid=args.get('<app-id>'))

    if args.get("destroy") and args.get("app"):
        return destroy_app(uid=args.get('<user-id>'), aid=args.get('<app-id>'))
    
    if args.get("log") and args.get("app"):
        return log_app(uid=args.get('<user-id>'), aid=args.get('<app-id>'))

    # ------------------------------------
    # bigbuild list apps <user-id>
    # ------------------------------------
    if args.get("list"):
        return list_apps(uid=args.get('<user-id>'))

    # ------------------------------------
    # bigbuild scale <user-id> <app-id> [-r=<num>]
    # ------------------------------------
    if args.get("scale"):
        return scale_app(uid=args.get('<user-id>'), aid=args.get('<app-id>'), r=args.get('-r'))

    if args.get("test"):
        return test_app()

def test_app():
    k8utils.get_service_port('kube-dj', 'user--wonyoung1026')

def get_service_port(uid, aid):
    namespace = USER_NAMESPACE_PREFIX + uid
    r = k8utils.get_service_port(ns=namespace, name=aid)
    print(r[1] if r[0] else r)

def describe_app(uid, aid):
    namespace = USER_NAMESPACE_PREFIX + uid
    r = k8utils.get_deployment_description(ns=namespace, name=aid)
    print(r[1] if r[0] else r)


def deploy_app(uid, aid, image, port, replicas):
    # TODO: accept multiple ports and their types
    namespace = USER_NAMESPACE_PREFIX + uid
        
    print("[INFO] Setting namespace")
    r = k8utils.set_namespace(namespace)
    if not r[0]:
        print(r)
        return
        
    print("[INFO] Creating PV")
    r = k8utils.create_pv(name=aid, ns=namespace)
    if not r[0]:
        print(r)
        return


    print("[INFO] Creating PVC")
    r = k8utils.create_pvc(name=aid, ns=namespace)
    if not r[0]:
        print(r)
        return


    print("[INFO] Creating deployment")
    r = k8utils.create_deployment(
        name=aid, ns=namespace, image=image, 
        port=port, replicas=replicas
    )
    if not r[0]:
        print(r)
        return

    print("[INFO] Creating service")
    r = k8utils.create_service(name=aid, ns=namespace)
    if not r[0]:
        print(r)
        return
    
    print("[INFO] Fetching node port number")
    r = k8utils.get_service_port(ns=namespace, name=aid)
    if not r[0]:
        print(r)
        return
    
    print("Deployed on port#"+r[1])

def destroy_app(uid, aid):
    namespace=USER_NAMESPACE_PREFIX+uid
    # print("[INFO] Deleting deployment")
    r = k8utils.delete_deployment(ns=namespace, name=aid)
    if not r[0]:
        print(r)
        return

    # print("[INFO] Deleting service")
    r = k8utils.delete_service(ns=namespace, name=aid)
    if not r[0]:
        print(r)
        return

    print("Deleted")

def log_app(uid, aid):
    namespace = USER_NAMESPACE_PREFIX+uid
    r = k8utils.get_deployments(ns=namespace, name=aid)
    
    print(r[1] if r[0] else r)


def list_apps(uid):
    namespace = USER_NAMESPACE_PREFIX+uid
    r = k8utils.get_deployments(ns=namespace)
    
    print(r[1] if r[0] else r)


def scale_app(uid, aid, r):
    namespace = USER_NAMESPACE_PREFIX+uid
    r = k8utils.scale_replica(ns=namespace, name=aid, replicas=r)

    print(r[1] if r[0] else r)
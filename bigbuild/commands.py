from . import utils as k8utils

USER_NAMESPACE_PREFIX = 'user--'

def process_args(args):
    print(args)
    # ------------------------------------
    #   bigbuild deploy app <user-id> <app-id> <image> <port> [-r=<num>]
    # ------------------------------------
    if args.get("deploy") and args.get("app"):
        return deploy_app(uid=args.get('<user-id>'), aid=args.get('<app-id>'),
            image=args.get('<image>'), port=args.get('<port>'), replicas=args.get('-r')
        )

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
        return list_apps(uid=args.get('<user-id>'), aid=args.get('<app-id>'))

    # ------------------------------------
    # bigbuild scale (up|down) <user-id> <app-id> [-n=<num>]
    # ------------------------------------
    if args.get("scale"):
        return scale_app(inc=args.get("up"), uid=args.get('<user-id>'), aid=args.get('<app-id>'), n=args.get('-n'))

def describe_app(uid, aid):
    print(uid)
    print(aid)

def deploy_app(uid, aid, image, port, replicas):
    namespace = USER_NAMESPACE_PREFIX + uid
        
    print("[INFO] Setting namespace")
    r = k8utils.set_namespace(namespace)
    if not r[0]:
        return r
    
    print("[INFO] Creating deployment")
    r = k8utils.create_deployment(
        name=aid, ns=namespace, image=image, 
        port=port, replicas=replicas
    )
    if not r[0]:
        return r

    print("[INFO] Creating service")
    r = k8utils.create_service(
        name=aid, ns=namespace, port=port
    )
    if not r[0]:
        return r
    
    return True

def destroy_app(uid, aid):
    pass

def log_app(uid, aid):
    pass

def list_apps(uid):
    pass

def scale_app(inc, uid, aid, n):
    pass
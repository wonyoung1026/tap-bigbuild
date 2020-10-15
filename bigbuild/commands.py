from invoke import run

def process_args(args):
    print(args)

    if args.get("describe") and args.get("app"):
        return describe_app(uid=args.get('<user-id>'), aid=args.get('<app-id>'))
    
    if args.get("deploy") and args.get("app"):
        return deploy_app(uid=args.get('<user-id>'), aid=args.get('<app-id>'))

    if args.get("destroy") and args.get("app"):
        return destroy_app(uid=args.get('<user-id>'), aid=args.get('<app-id>'))
    
    if args.get("log") and args.get("app"):
        return log_app(uid=args.get('<user-id>'), aid=args.get('<app-id>'))

    if args.get("list") and args.get("apps"):
        return list_apps(uid=args.get('<user-id>'), aid=args.get('<app-id>'))


def describe_app(uid, aid):
    print(uid)
    print(aid)

def deploy_app(uid, aid):
    pass

def destroy_app(uid, aid):
    pass

def log_app(uid, aid):
    pass

def list_apps(uid):
    pass

def scale_app(uid, aid, n):
    pass
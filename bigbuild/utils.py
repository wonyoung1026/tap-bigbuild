from invoke import run
import json

def set_namespace(ns):
    cmd = '''
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Namespace
metadata:
  name: {ns}
EOF
    '''.format(ns=ns)
    result = run(cmd)
    
    return (
        result.ok, 
        result.stdout if result.ok else result.stderr
    )

def create_deployment(name, ns, image, port, replicas):
    cmd = '''
cat <<EOF | kubectl apply --validate=false -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {name}
  namespace: {ns}
  labels:
    app: {name}
spec:
  replicas: {replicas}
  selector:
    matchLabels:
      app: {name}
  template:
    metadata:
      labels:
        app: {name}
    spec:
      containers:
      - name: {name}
        image: {image}
        imagePullPolicy: Always
        ports:
        - containerPort: {port}
EOF
    '''.format(
        name=name, ns=ns, replicas=replicas, 
        image=image, port=port
    )

    result = run(cmd)
    
    return (result.ok, result.stdout if result.ok else result.stderr)

# def get_free_port(min_port=):

def create_service(ns, name):
    # TODO: Change NodePort --> ingress for load balancing and defining paths
    cmd = '''
kubectl expose deployment {name} --type=NodePort -n {ns}
    '''.format(name=name, ns=ns)

    result = run(cmd)
    
    return (result.ok, result.stdout if result.ok else result.stderr)


def delete_service(name, ns):
    cmd = '''
kubectl delete svc {name} -n {ns}
    '''.format(name=name, ns=ns)

    result = run(cmd)
    
    return (result.ok, result.stdout if result.ok else result.stderr)

def delete_deployment(name, ns):
    cmd = '''
kubectl delete deployment {name} -n {ns}
    '''.format(name=name, ns=ns)
    
    result = run(cmd)
    
    return (result.ok, result.stdout if result.ok else result.stderr)

def delete_namespace(ns):
    cmd = '''
kubectl delete namespace {ns}
    '''.format(name=name, ns=ns)

    result = run(cmd)
    
    return (result.ok, result.stdout if result.ok else result.stderr)


def get_service_port(name, ns):
    # TODO: change NodePort to ingress
    # TODO 2: multiple ports
    cmd = '''
kubectl get services {name} -n {ns} -o jsonpath='{{.spec.ports[0].nodePort}}{{"\\n"}}'

    '''.format(name=name, ns=ns)

    result = run(cmd)
    
    if not result.ok:
        return (result.ok, result.stderr)
    # print(result.stdout)
    # j = json.loads(result.stdout)

    # port = j.get("spec").get("ports")[0].get("nodePort")

    return (True if port else False, port)

def get_deployments(ns):
    cmd = '''
kubectl get deployments -n {ns} -o json

    '''.format(ns=ns)

    result = run(cmd)

    return (result.ok, result.stdout if result.ok else result.stderr)
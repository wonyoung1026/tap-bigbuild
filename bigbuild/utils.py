from invoke import run
import socket

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


def delete_service():
    pass

def delete_deployment():
    pass

def delete_namespace():
    pass
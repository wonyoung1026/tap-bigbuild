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
    result = run(cmd, hide=True, warn=True)
    
    return (
        result.ok, 
        result.stdout if result.ok else result.stderr
    )

def create_pvc(name, ns):
    cmd='''
cat <<EOF | kubectl apply --validate=false -f -
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: nfs-pvc-{name}
  namespace: {ns}
spec:
  storageClassName: nfs
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 100Mi

    '''.format(name=name, ns=ns)

    result = run(cmd, hide=True, warn=True)
    
    return (
        result.ok, 
        result.stdout if result.ok else result.stderr
    )


def create_pv(name, ns):
    cmd = '''
cat <<EOF | kubectl apply --validate=false -f -
apiVersion: v1
kind: PersistentVolume
metadata:
  name: nfs-pv-{name}
  namespace: {ns}
spec:
  capacity:
    storage: 100Mi
  volumeMode: Filesystem
  accessModes:
    - ReadWriteMany
  persistentVolumeReclaimPolicy: Recycle
  storageClassName: nfs
  mountOptions:
    - hard
    - nfsvers=4.1
  nfs:
    path: /bigbuild/nfsshare
    server: nfs-server

    '''.format(name=name, ns=ns)

    result = run(cmd, hide=True, warn=True)
    
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
        volumeMounts:
        - name: bigbuild-nfs-storage      
          mountPath: "/tmp"
      volumes:
      - name: bigbuild-nfs-storage
        persistentVolumeClaim:
            claimName: nfs-pvc-{name}
EOF
    '''.format(
        name=name, ns=ns, replicas=replicas, 
        image=image, port=port
    )

    result = run(cmd, hide=True, warn=True)
    
    return (result.ok, result.stdout if result.ok else result.stderr)

# def get_free_port(min_port=):

def create_service(ns, name):
    # TODO: Change NodePort --> ingress for load balancing and defining paths
    cmd = '''
kubectl expose deployment {name} --type=NodePort -n {ns}
    '''.format(name=name, ns=ns)

    result = run(cmd, hide=True, warn=True)
    
    return (result.ok, result.stdout if result.ok else result.stderr)


def delete_service(name, ns):
    cmd = '''
kubectl delete svc {name} -n {ns}
    '''.format(name=name, ns=ns)

    result = run(cmd, hide=True, warn=True)
    
    return (result.ok, result.stdout if result.ok else result.stderr)

def delete_deployment(name, ns):
    cmd = '''
kubectl delete deployment {name} -n {ns}
    '''.format(name=name, ns=ns)
    
    result = run(cmd, hide=True, warn=True)
    
    return (result.ok, result.stdout if result.ok else result.stderr)

def delete_namespace(ns):
    cmd = '''
kubectl delete namespace {ns}
    '''.format(name=name, ns=ns)

    result = run(cmd, hide=True, warn=True)
    
    return (result.ok, result.stdout if result.ok else result.stderr)


def get_service_port(name, ns):
    # TODO: change NodePort to ingress
    # TODO 2: multiple ports
    cmd = '''
kubectl get services {name} -n {ns} -o jsonpath='{{.spec.ports[0].nodePort}}{{"\\n"}}'

    '''.format(name=name, ns=ns)

    result = run(cmd, hide=True, warn=True)
    
    if not result.ok:
        return (result.ok, result.stderr)
    port = result.stdout

    return (True if port else False, port)

def get_deployments(ns):
    cmd = '''
kubectl get deployments -n {ns} -o jsonpath='[name, creationTimestamp, replicas(active/total)]{{range .items[*]}}[{{.metadata.name}},{{.metadata.creationTimestamp}}, {{.status.readyReplicas}}/{{.status.availableReplicas}}] {{end}}'

    '''.format(ns=ns)

    result = run(cmd, hide=True, warn=True)

    return (result.ok, result.stdout if result.ok else result.stderr)


def scale_replica(ns, name, replicas):
    cmd = '''
kubectl scale --replicas={replicas} deployment {name} -n {ns}
    '''.format(ns=ns, name=name, replicas=replicas)

    result = run(cmd, hide=True, warn=True)

    return (result.ok, result.stdout if result.ok else result.stderr)

def get_deployment_logs(name, ns):
    cmd = '''
kubectl logs deployment/{name} -n {ns} --timestamps=true
    '''.format(ns=ns, name=name)


    result = run(cmd, hide=True, warn=True)

    return (result.ok, result.stdout if result.ok else result.stderr)

def get_deployment_description(name, ns):
    cmd = '''
kubectl describe deployment/{name} -n {ns}
    '''.format(ns=ns, name=name)

    result = run(cmd, hide=True, warn=True)

    return (result.ok, result.stdout if result.ok else result.stderr)

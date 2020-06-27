import os
import time

class Helm(object):
    def install_helm_chart(self, name: str):
        os.system("helm install --namespace test " + name + " ./ppw-chart --set fullnameOverride=" + name)
        time.sleep(10)

    def get_node_port(self, name: str):
        command = "kubectl get --namespace test -o jsonpath={.spec.ports[0].nodePort} services " + name
        stream = os.popen(command)
        nodePort = stream.read()
        return nodePort

    def get_node_ip(self):
        command = 'kubectl get nodes --namespace test -o jsonpath={.items[0].status.addresses[1].address}'
        stream = os.popen(command)
        nodeIP = stream.read()
        return nodeIP

    def delete_helm_chart(self, name: str):
        os.system("helm delete --namespace test " + name)

import os
import time

class Setup(object):
    def install_helm_chart(self, name: str):
        os.system("helm install --namespace test " + name + " ./ppw-chart --set fullnameOverride=" + name)
        os.system("kubectl get --namespace test services")

    def get_node_port(self, name: str):
        command = "kubectl get --namespace test -o jsonpath={.spec.ports[0].nodePort} services " + name
        stream = os.popen(command)
        nodePort = stream.read()
        print(nodePort)
        return nodePort

    def get_node_ip(self):
        command = 'kubectl get nodes --namespace test -o jsonpath={.items[0].status.addresses[1].address}'
        stream = os.popen(command)
        nodeIP = stream.read()
        print(nodeIP)
        return nodeIP

    def delete_helm_chart(self, name: str):
        os.system("helm delete --namespace test " + name)

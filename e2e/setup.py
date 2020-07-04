import os

class Setup(object):
    def __init__(self, name):
        self.chart_name = name

    def get_node_port(self):
        command = "kubectl get --namespace test -o jsonpath={.spec.ports[0].nodePort} services " + self.chart_name
        stream = os.popen(command)
        nodePort = stream.read()
        return nodePort

    def get_node_ip(self):
        command = "kubectl get nodes --namespace test -o jsonpath={.items[0].status.addresses[0].address}"
        stream = os.popen(command)
        nodeIP = stream.read()
        return nodeIP

    def install_helm_chart(self):
        os.system("helm install --namespace test " + self.chart_name + " ./ppw-chart --set fullnameOverride=" + self.chart_name + " --wait")

    def delete_helm_chart(self):
        os.system("helm delete --namespace test " + self.chart_name)
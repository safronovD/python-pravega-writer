import os
import sys

from e2e.setup_helm import HelmSetup

if __name__ == "__main__":
    obj = HelmSetup(sys.argv[1])
    obj.install_helm_chart()
    
    nodeIP = obj.get_node_ip()
    nodePort = obj.get_node_port()

    os.system('bzt ./stress-test/stress-test.yml -o scenarios.performance.default-address=http://{}:{} -report'.format(nodeIP, nodePort))

    obj.delete_helm_chart()
import os
import sys

from e2e.setup_helm import Setup

if __name__ == "__main__":
    obj = Setup(sys.argv[1])
    obj.install_helm_chart()
    nodeIP = obj.get_node_ip()
    nodePort = obj.get_node_port()

    os.system('locust -f ./stress-test/request.py --csv=reports/result --host=http://{}:{} --headless -u 1000 -r 100 --run-time 40s'.format(nodeIP, nodePort))

    obj.delete_helm_chart()
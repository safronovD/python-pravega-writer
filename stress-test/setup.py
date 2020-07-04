import os
from e2e.setup import Setup

if __name__ == "__main__":
    chartName = sys.argv[1]
    obj = Setup(chartName)

    #obj.install_helm_chart()

    nodeIP = obj.get_node_ip()
    #nodePort = obj.get_node_port()
    os.system("echo ${nodeIP}")

    #os.system("locust -f ./stress-test/request.py --csv=reports/result --host=http://${nodeIP}:${nodePort} --headless -u 1000 -r 100 --run-time 40s")

    #obj.delete_helm_chart()

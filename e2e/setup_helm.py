import os
import re
import sys
from src.common.log.logger import init_logger

# TODO проверить ответ через регулярки?
# TODO добавит логи в случае фейла


class Setup:
    def __init__(self, tag):
        self.tag = tag
        self.chart_name = ''.join(['et-', tag])
        self.logger = init_logger('dev')

    def get_node_port(self):
        self.logger.info('Attempt to get node port')

        json_path = '{.spec.ports[0].nodePort}'
        command = "kubectl get --namespace test -o jsonpath={} services {}".format(json_path, self.chart_name)
        answer = os.popen(command).read()
        # answer = '2222'
        if re.search(r'Error from server \(NotFound\): services \"(.*)\" not found', answer):
            self.logger.error('Service {} not found'.format(self.chart_name))
            self.delete_helm_chart()
        elif re.search(r'\d+', answer):
            self.logger.warning('Node port {} is received'.format(answer))
            return answer

    def get_node_ip(self):
        self.logger.info('Attempt to get node port')

        json_path = '{.items[0].status.addresses[0].address}'
        command = "kubectl get nodes --namespace test -o jsonpath={}".format(json_path)
        answer = os.popen(command).read()
        # answer = '92.168.70.216'
        if re.search(r'\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}', answer):
            self.logger.warning('Node ip {} is received'.format(answer))
            return answer

    def install_helm_chart(self):
        self.logger.info('Attempt to install helm chart')
        registry = '192.168.70.210:5000'
        secret = 'regcred'
        server_image = 'ppw-server:{}'.format(self.tag)
        connector_image = 'ppw-connector:{}'.format(self.tag)
        ml_controller_image = 'ppw-ml-controller:{}'.format(self.tag)
        command = "helm install --namespace test {0} ./ppw-chart --set fullnameOverride={0}" \
                  " --set common.image_repository={1} " \
                  "--set common.image_pullSecretName={2} " \
                  "--set server.image_name={3} " \
                  "--set jobs.connector_image={4} " \
                  "--set jobs.ml_controller_image={5}".format(self.chart_name, registry, secret, server_image,
                                                              connector_image, ml_controller_image)
        answer = os.popen(command).read()
        #
        # answer = r'Error: rendered manifests contain a resource that already exists. Unable to continue with ' \
        #                  r'install: Service "test-chart" in namespace "test" exists and cannot be imported into the ' \
        #                  r'current release: invalid ownership metadata; annotation validation error: key ' \
        #                  r'"meta.helm.sh/release-name" must equal "test1": current value is "test-chart" '

        if re.search('Error: cannot re-use a name that is still in use', answer):
            self.logger.error('Chart {} already exists'.format(self.chart_name))
            self.delete_helm_chart()
            self.install_helm_chart()

        elif re.search('Error: rendered manifests contain a resource that already exists', answer):

            match = re.findall(r'install: (.*) "(.*)" in namespace "(.*)" exists', answer)
            resource = match[0][0]
            resource_name = match[0][1]
            namespace = match[0][2]

            self.logger.error('Chart is not installed: Resource {} "{}" in namespace "{} already exists'.format(resource.lower(),
                                                                                                                resource_name,
                                                                                                                namespace))
            self.logger.info('Attempt to delete {} {}'.format(resource, resource_name))

            command = 'kubectl delete {} {} --namespace {}'.format(resource, resource_name, namespace)
            answer = os.popen(command).read()
        #     answer = 'service "test-chart" deleted'

            if re.search('{} {} deleted'.format(resource.lower(), resource_name), answer):
                self.logger.warning('{} {} deleted'.format(resource, resource_name))
                self.install_helm_chart()
            else:
                self.logger.error('{} {} is not deleted'.format(resource, resource_name))
            # print(command)

        elif answer.startswith('NAME:'):
            self.logger.warning('Chart {} is installed'.format(self.chart_name))

    def delete_helm_chart(self):
        self.logger.info('Attempt to delete helm chart')
        command = "helm delete --namespace test {}".format(self.chart_name)
        answer = os.popen(command).read()
        # answer = 'Error: uninstall: Release not loaded: test: release: not found'

        if re.search(r'Error: uninstall: Release not loaded: (.*): release: not found', answer):
            self.logger.error('Chart {} doesn\'t exist'.format(self.chart_name))
        else:
            self.logger.warning('Chart {} is deleted'.format(self.chart_name))


if __name__ == "__main__":
    obj = Setup(sys.argv[1])
    obj.install_helm_chart()
    obj.get_node_ip()
    obj.get_node_port()
    obj.delete_helm_chart()

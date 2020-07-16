from log.logger import init_logger
import os
import re
import time


class PodSetup:
    def __init__(self):
        self.logger = init_logger('ci')
        self.logger.info('\n')
        self.logger.info('Object initialization is started')

        tag = os.environ["GIT_COMMIT"]
        repo = '192.168.70.210:5000'

        self.pod_name = 'ppw-server-{}'.format(tag)
        self.image_name = '{}/ppw-server:{}'.format(repo, tag)

        self.logger.info('Object initialization is completed')

    def run_pod(self):
        command = 'kubectl run {} --image={} --port=666 --hostport=666 --wait=true --namespace=test-container'.format(self.pod_name, self.image_name)

        self.logger.info('Attempt to create pod {}'.format(self.pod_name))
        self.logger.info('Execute command {}'.format(command))

        answer = os.popen(command).read()
        if answer:
            self.logger.info('Answer from cluster received')
            self.logger.debug(answer)
            self.logger.info('Parsing results')
            if re.search(r'\w*/{} created'.format(self.pod_name), answer):
                self.logger.info('Pod {} is created'.format(self.pod_name))
            else:
                self.logger.error('Something went wrong. Pod {} is not created'.format(self.pod_name))
                self.logger.error(answer)

    def delete_pod(self):
        command = 'kubectl delete pod {}'.format(self.pod_name)

        self.logger.info('Attempt to delete pod {}'.format(self.pod_name))
        self.logger.info('Execute command {}'.format(command))

        answer = os.popen(command).read()
        if answer:
            self.logger.info('Answer from cluster received')
            self.logger.debug(answer)
            self.logger.info('Parsing results')
            if re.search(r'pod "{}" deleted'.format(self.pod_name), answer):
                self.logger.info('Pod {} is deleted'.format(self.pod_name))
            else:
                self.logger.error('Something went wrong. Pod {} is not deleted'.format(self.pod_name))
                self.logger.error(answer)
        else:
            self.logger.error('Answer from cluster not received')
            self.logger.error('Check that command {} is correct'.format(command))

    def get_pod_ip(self):
        command = 'kubectl describe pod {}'.format(self.pod_name)

        self.logger.info('Attempt to get pod {} info'.format(self.pod_name))
        self.logger.info('Execute command {}'.format(command))
        self.logger.info('Waiting pod {}'.format(self.pod_name))

        if self.check_readyness('pod', self.pod_name):
            answer = os.popen(command).read()

            self.logger.info('Answer from cluster received')
            self.logger.debug(answer)
            self.logger.info('Parsing results')
            match = re.findall(r'IP:\s+(\d{2,3}.\d{2,3}.\d{2,3}.\d{2,3})', answer)
            if match:
                self.logger.info('Ip address found: {}'.format(match[0]))
                return match[0]
            else:
                self.logger.error('Ip address not found')
                self.logger.error(answer)

    def check_readyness(self, resource_type, resource_name):
        def get_status(resource_type, answer):
            if resource_type == 'pod':
                match = re.findall(r'Status:\s+(\w+)', answer)
                if len(match) > 1:
                    match = match[0][0]
                else:
                    match = match[0]
                if match == 'Running':
                    return True

            elif resource_type == 'deployment':
                match = re.findall(r'(\d+)\s+ available', answer)
                if match[0] >= 1:
                    return True

            elif resource_type == 'service':
                pass
                # if re.findall(r'Name\s+{}'.format, answer)
            return False

        command = 'kubectl describe {} {}'.format(resource_type, resource_name)

        for _ in range(20):
            self.logger.info('Checking status № {}'.format(_ + 1))
            if get_status(resource_type, os.popen(command).read()):
                self.logger.info('{} {} is ready'.format(resource_type, resource_name))
                return True
            self.logger.warning('{} {} is not ready'.format(resource_type, resource_name))
            time.sleep(5)
        return False

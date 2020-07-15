from log.logger import init_logger
import os
import re
import time


class PodSetup:
    def __init__(self):
        self.logger = init_logger('dev')
        self.logger.info()
        self.logger.info('Object initialization is started')

        tag = os.environ["GIT_COMMIT"]
        repo = '192.168.70.210:5000'

        self.pod_name = 'ppw-server-{}'.format(tag)
        self.image_name = '{}/ppw-server:{}'.format(repo, tag)

        self.logger.info('Object initialization is completed')

    def run_pod(self):
        command = 'kubectl run {} --image={} --port=666 --hostport=666 --wait=true'.format(self.pod_name, self.image_name)

        self.logger.info('Attempt to create pod {}'.format(self.pod_name))
        self.logger.info(command)

        answer = os.popen(command).read()
        if answer:
            self.logger.info('Answer from cluster received')
            self.logger.info(answer)
            if re.search(r'\w*/{} created'.format(self.pod_name), answer):
                self.logger.warning('Pod {} is created')
            else:
                self.logger.error('Something went wrong. Pod {} is not created'.format(pod_name))

    def delete_pod(self):
        command = 'kubectl delete pod {}'.format(self.pod_name)

        self.logger.info('Attempt to delete pod {}'.format(self.pod_name))
        self.logger.info(command)

        answer = os.popen(command).read()
        if answer:
            self.logger.info('Answer from cluster received')
            self.logger.info(answer)
            if re.search(r'pod "{} deleted'.format(self.pod_name), answer):
                self.logger.warning('Pod {} is deleted')
            else:
                self.logger.error('Something went wrong. Pod {} is not deleted'.format(self.pod_name))

    def get_pod_ip(self):
        command = 'kubectl describe pod {}'.format(self.pod_name)

        self.logger.info('Attempt to get pod info {}'.format(self.pod_name))
        self.logger.info(command)
        self.logger.info('Waiting pod {}'.format(self.pod_name))
        if self.wait_readyness('pod', self.pod_name):
            answer = os.popen(command).read()

            self.logger.info(answer)
            match = re.findall(r'IP:\s+(\d{2,3}.\d{2,3}.\d{2,3}.\d{2,3})', answer)
            if match:
                self.logger.warning('Ip address found: {}'.format(match[0]))
                return match[0]

    def wait_readyness(self, resource_type, resource_name):
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
                self.logger.warning('{} {} is ready'.format(resource_type, resource_name))
                return True
            self.logger.info('{} {} is not ready'.format(resource_type, resource_name))
            time.sleep(5)
        return False

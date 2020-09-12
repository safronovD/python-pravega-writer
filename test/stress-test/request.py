from locust import HttpUser, TaskSet, task, between


def index(self):
    self.client.get("/v1")


class UserTasks(TaskSet):
    tasks = [index]


class ServerUser(HttpUser):
    wait_time = between(0.1, 0.5)
    tasks = [UserTasks]

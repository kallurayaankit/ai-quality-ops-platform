from locust import HttpUser, task, between

class AIUser(HttpUser):
    wait_time = between(0.5, 1)

    @task
    def ask_agent(self):
        self.client.post("/agent", json={"query": "Hello"})
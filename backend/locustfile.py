from locust import HttpUser, task, between


class MyUser(HttpUser):
    wait_time = between(1, 3)  # Time between requests in seconds

    @task
    def get_all_posts(self):
        self.client.get("/api")

    @task
    def get_all_tags(self):
        self.client.get("/api/get-all-tags")

    @task
    def get_all_locations(self):
        self.client.get("/api/get-all-locations")

    @task
    def get_all_clubs(self):
        self.client.get("/api/get-all-clubs")

    @task
    def autosuggest(self):
        self.client.get("/api/autosuggest?query=test")

    @task
    def search(self):
        self.client.get("/api/search?query=test")

    @task
    def get_event(self):
        event_id = 1
        self.client.get(f"/api/{event_id}")

    @task
    def get_event_image(self):
        event_id = 1
        self.client.get(f"/api/{event_id}/image")

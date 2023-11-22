import random

import requests
from faker import Faker

from SocialMediaGeneratorBot.client import API_Client
from SocialMediaGeneratorBot.settings import Settings


class StarNaviClient:
    def __init__(self):
        # Create instances of classes to connect to the API and handle configuration settings
        self.config = Settings()
        self.fake = Faker()
        self.api_client = API_Client(base_url=self.config.base_url)
        self.users = []

    def create_users(self):
        request_endpoint = "auth/register"
        for index in range(self.config.number_of_users):
            user_data = {
                "username": self.fake.name(),
                "email": self.fake.email(),
                "password": self.fake.password(),
            }
            self.users.append(user_data)

            try:
                # Send a POST request to create a new user
                response = self.api_client.post(
                    endpoint=request_endpoint, payload=user_data
                )
                response.raise_for_status()  # Check the response status
                print(
                    f"User {index + 1} created successfully. Response status code: {response.status_code}"
                )
            except requests.exceptions.RequestException as e:
                print(f"Failed to create user {index + 1}. Error: {e}")

    def create_posts(self):
        request_endpoint = "post"
        for user in self.users:
            for index in range(random.randint(1, self.config.max_post_per_user + 1)):
                post_data = {"title": self.fake.sentence(), "content": self.fake.text()}

                try:
                    # Send a POST request to create a new post
                    response = self.api_client.post(
                        endpoint=request_endpoint, payload=post_data, user=user
                    )
                    response.raise_for_status()  # Check the response status
                    print(
                        f"Post {index + 1} for user: {user['username']} created successfully. Response status code: {response.status_code}"
                    )
                except requests.exceptions.RequestException as e:
                    print(f"Failed to create post. Error: {e}")

    def like_posts(self):
        total_posts = 0
        response = self.api_client.get(endpoint="post", user=self.users[0])
        if response.status_code == 200:
            json_data = response.json()
            total_posts = json_data.get("total")

        for user in self.users:
            for index in range(self.config.max_likes_per_user):
                random_post = random.randint(1, total_posts + 1)
                request_endpoint = f"post/{random_post}/like"

                try:
                    # Send a POST request to like a post
                    response = self.api_client.post(
                        endpoint=request_endpoint, payload={}, user=user
                    )
                    response.raise_for_status()  # Check the response status
                    print(
                        f"Post id:{random_post} liked successfully by {user['username']} . Response status code: {response.status_code}"
                    )
                except requests.exceptions.RequestException as e:
                    print(f"Failed to like post. Error: {e}")

    def run(self):
        # Execute the actions to create users, posts, and like posts
        self.create_users()
        self.create_posts()
        self.like_posts()


if __name__ == "__main__":
    app = StarNaviClient()
    app.run()

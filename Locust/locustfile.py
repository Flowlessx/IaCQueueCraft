from locust import FastHttpUser, task, between

class MyUser(FastHttpUser):
    wait_time = between(1, 3)  # Random wait time between requests

    @task
    def login(self):
        data = {
            "student_name": "example_user",
            "student_password": "example_password"
        }
        response = self.client.post("/login", json=data)
        
        # Check if the request was successful
        if response:
            # Print the response status code
            print("Response status code:", response.status_code)
            
            # Print the response content as text
            print("Response content:", response.text)
            
            # If the response is JSON, you can print it in a more readable format
            # Uncomment the following lines if your response is JSON
            # try:
            #     json_response = response.json()
            #     print("Response JSON:", json_response)
            # except ValueError:
            #     print("Response is not JSON")

        else:
            # Print an error message if the request was not successful
            print("Request failed with status code:", response.status_code)

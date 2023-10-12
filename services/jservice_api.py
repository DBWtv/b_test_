import requests


class JServiceApi:
    URL = "https://jservice.io/api/random?count="

    def get_questions(self, count: int):
        response = requests.get(self.URL + str(count))
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(
                f'Error {response.status_code} while getting questions from {self.URL}')

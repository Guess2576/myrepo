import string
import requests
import json
import io

url = "https://michaelgathara.com/api/python-challenge"

response = requests.get(url)

challenges = response.json()

for challenge in challenges:
    problem = challenge["problem"]
    problem = problem.replace("?", "")
    print("Problem:", problem, "Answer:", eval(problem))
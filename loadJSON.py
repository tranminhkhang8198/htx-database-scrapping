import json
from pprint import pprint

with open("data.txt") as f:
    data = json.load(f)

pprint(data)

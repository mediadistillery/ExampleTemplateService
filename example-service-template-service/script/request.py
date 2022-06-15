import requests

def sumation_request(elements):
    _elements = elements
    url = "http://localhost:5000/api/1/example/sum"

    response = requests.post(url,
                             json=_elements,
                             headers={'accept': 'application/json'})
    return response


def version_request():

    url = "http://localhost:5000/api/1/example/version"

    response = requests.get(url,
                             headers={'accept': 'application/json'})
    return response

result = sumation_request([10,10,10, 9.78,3])
print(result.content)
print(version_request().content)

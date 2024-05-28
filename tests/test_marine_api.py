import requests

def test_api_returns_200():
    url = "https://marine-api.open-meteo.com/v1/marine"
    response = requests.get(url)
    assert response.status_code == 200

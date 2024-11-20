import requests
##
url = "http://127.0.0.1:8001/api/v1/movies/2"
data = {
    "name": "Bladerunner",
    "plot": "Deckard (Harrison Ford) is forced by the police Boss (M. Emmet Walsh) to continue his old job as Replicant Hunter. His assignment: eliminate four escaped Replicants from the colonies who have returned to Earth. ",
    "genres": ["Sci-Fi", "Thriller"],
    "cast_id": [10]
}



response = requests.delete(url)

print(response.content)
print(f"Status Code: {response.status_code}")
print(f"Response JSON: {response.json()}")

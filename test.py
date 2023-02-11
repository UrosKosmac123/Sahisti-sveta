import requests
from bs4 import BeautifulSoup

# Set the URL of the website containing the chess games
url = 'https://www.chess.net/games'

# Send a request to the website and retrieve the HTML content
response = requests.get(url)
html = response.content

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Find the element(s) containing the results of the chess games
results = soup.find_all(class_='game-result')

# Iterate through the results and print the results of the games
for result in results:
    print(result.text)
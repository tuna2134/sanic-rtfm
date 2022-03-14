import requests
from bs4 import BeautifulSoup
import json

r = requests.get("https://sanic.readthedocs.io/en/stable/sanic/api_reference.html")

soup = BeautifulSoup(r.content, "html.parser")
content = soup.find(id="api-reference")
soup = BeautifulSoup(str(content), "html.parser")
data = {
    "class": {}
}

for menu in (soup.find_all(class_="reference internal")):
    if menu.text.startswith("sanic."):
        continue
    r = requests.get("https://sanic.readthedocs.io/en/stable/sanic/" + menu.get("href"))
    soup = BeautifulSoup(r.content, "html.parser")
    for c in (soup.find_all(class_="py class")):
        em = c.find("em")
        if em is None:
            continue
        result = em.find("span", class_="pre")
        if result is None:
            continue
        elif result.text == "class":
            class_name = c.find("span", class_="sig-name descname").text
            data["class"][class_name] = []
            for i in c.find_all("dl", class_="py method"):
                data["class"][class_name].append(i.find("span", "sig-name descname").text)

with open("data.json", "w") as f:
    json.dump(data, f, indent=4)
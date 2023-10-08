import json
import requests

from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urlparse

html_parser = BeautifulSoup(
    # use any *.usmission.gov or *.usembassy.gov website
    requests.get("https://nato.usmission.gov/").text, "html.parser"
)

current_dump = {"domains": list(), "updatedOn": datetime.now().strftime("%d/%m/%Y %H:%M:%S")}

# use "country/area" dropdown
for ul in html_parser.find_all("ul", {"id": "nav__country-nav"}):
    for li in ul.find_all("li"):
        for a in li.find_all("a"):
            name = a.string.strip()
            website = urlparse(a.get("href"))

            current_dump["domains"].append(
                {
                    "name": name,
                    "website": f"{website.scheme}://{website.netloc}", # remove path
                }
            )

with open("current.json", "w", encoding="utf-8") as file:
    file.write(json.dumps(current_dump, indent=2))

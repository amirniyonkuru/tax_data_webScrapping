import os
import requests
import json
from bs4 import BeautifulSoup

# Enter the form and years range to search
fetch_res = input("Enter what to search for: ")
min_yr = int(input("Enter min year: "))
max_yr = int(input("Enter max year: "))

# First search the web url for the match
url = f"https://apps.irs.gov/app/picklist/list/priorFormPublication.html?value={fetch_res}&criteria=formNumber&submitSearch=Find"


req = requests.get(url).text
elem = []


def result():
    soup = BeautifulSoup(req, "html.parser")
    result_row = soup.find_all(class_="even")

    # Loop through all table rows that match the class name
    for result_r in result_row:
        number = result_r.find("td", class_="LeftCellSpacer").a.text
        link = result_r.find("td", class_="LeftCellSpacer").a["href"]
        title = (result_r.find("td", class_="MiddleCellSpacer").text).strip()
        year = (result_r.find("td", class_="EndCellSpacer").text).strip()

        # Get data that match exactly the search key word
        if number.lower() == fetch_res.lower():

            elem.append(
                {
                    "link": link,
                    "form_number": number,
                    "form_title": title,
                    "form_year": year,
                }
            )
    return elem


def year_result(elem_list):
    a_res = elem_list()

    # Search the form that matches the range given
    b = [item for item in a_res if int(item["form_year"]) in range(min_yr, max_yr + 1)]

    for link in b:
        download_url = link["link"]

        # Download the file
        r = requests.get(download_url, allow_redirects=True)

        with open(
            os.path.join(f'./files/{link["form_number"]}-{link["form_year"]}.pdf'), "wb"
        ) as f:
            f.write(r.content)


year_result(result)
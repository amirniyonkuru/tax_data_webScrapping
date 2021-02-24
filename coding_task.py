import requests
import json
from bs4 import BeautifulSoup

# Enter the form to search
fetch_res = input("Enter what to search for: ")

# First search the web url for the match
url = f"https://apps.irs.gov/app/picklist/list/priorFormPublication.html?value={fetch_res}&criteria=formNumber&submitSearch=Find"


req = requests.get(url).text
elem_year = []


def result():
    soup = BeautifulSoup(req, "html.parser")
    result_row = soup.find_all(class_="even")
    data = {}
    if result_row:
        # Loop through all table rows that match the class name
        for result_r in result_row:
            number = result_r.find("td", class_="LeftCellSpacer").a.text
            title = (result_r.find("td", class_="MiddleCellSpacer").text).strip()
            year = (result_r.find("td", class_="EndCellSpacer").text).strip()

            # Get data that match exactly the search key word
            if number.lower() == fetch_res.lower():

                elem_year.append(year)
                data["form_number"] = number
                data["form_title"] = title
                data["min_year"] = sorted(elem_year)[0]
                data["max_year"] = sorted(elem_year)[-1]
        data = json.dumps(data, indent=4)
        print(data)
    else:
        print(f"No result was found for {fetch_res} ")


result()
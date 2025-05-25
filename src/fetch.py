from bs4 import BeautifulSoup
from datetime import datetime
import requests
import csv
import re


SIX_MONTH_URL = "https://secure.runescape.com/m=itemdb_oldschool/top100?list=0&scale=3"

def fetch_items():
    response = requests.get(SIX_MONTH_URL).content
    soup = BeautifulSoup(response, "html.parser").find_all(class_="table-item-link")
    for id, child in enumerate(soup):
        item_name = strip_filename(child.find("span").get_text())
        item_link = child["href"]
        
        fetch_data(id+1, item_name, item_link)
        print(item_name)

        # print(f"Item no: {id+1}, Item name: {strip_filename(child.find("span").get_text())}")

def fetch_data(id, item_name, item_link):
    url = item_link
    response = requests.get(url).content
    soup = BeautifulSoup(response, "html.parser").find_all("script")

    js_code = ""
    for script in soup:
        if script.string:
            js_code += script.string + "\n"

    pattern_price = re.compile(r"average180\.push\(\[new Date\('(\d{4}/\d{2}/\d{2})'\),\s*([\d.]+),\s*([\d.]+)\]\);")
    pattern_quantity = re.compile(r"trade180\.push\(\[new Date\('(\d{4}/\d{2}/\d{2})'\),\s*([\d.]+)\]\);")

    price_data = []
    for match in pattern_price.finditer(js_code):
        date_str, price1, price2 = match.groups()
        price_data.append({
            "date": date_str,
            "price": float(price1),
            "price_inactive": float(price2)
        })

    quantity_data = []
    for match in pattern_quantity.finditer(js_code):
        date_str, quantity = match.groups()
        quantity_data.append({
            "date": date_str,
            "quantity": int(float(quantity))  # convert to int safely even if float string
        })

    combined_data = []
    for p_data in price_data:
        for q_data in quantity_data:
            if p_data["date"] == q_data["date"]:
                combined_data.append({
                    "date": p_data["date"],
                    "price": p_data["price"],
                    "quantity": q_data["quantity"]
                })
                write_data(id, item_name, combined_data)
                break

def write_data(id, item_name, combined_data):

    with open(f"/home/burak/Desktop/virtualecon-analysis/data/{id}_{item_name}.csv", mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["date", "price", "quantity"])
        #print("inside")
        writer.writeheader()  # write column headers
        for row in combined_data:
            #print(row)
            writer.writerow(row)

def strip_filename(name):
    if name.endswith("..."):
        name = name[:-3]

    name = re.sub(r'[\\/:"*?<>|]+', '', name)
    name = name.replace(' ', '_')

    return name

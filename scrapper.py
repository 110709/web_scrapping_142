import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd

# Define constants
START_URL = "https://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars"
HEADERS = ["Name", "Distance", "Magnitude", "Spectral Class"]
star_data = []

# Step 3: Fetch HTML Page
response = requests.get(START_URL)
if response.status_code == 200:
    page_content = response.content
else:
    print("Error fetching the page.")
    exit()

# Step 4: Parse HTML and Extract Data
soup = BeautifulSoup(page_content, "html.parser")

# Find the table with class "wikitable"
target_table = soup.find("table", class_="wikitable")

if target_table is None:
    print("Target table not found.")
    exit()

# Get rows from the target table
rows = target_table.find_all("tr")

# Step 5: Create empty lists for star attributes
star_names = []
star_distances = []
star_magnitudes = []
star_spectral_classes = []

# Step 6 and 7: Loop through row_list to extract star data
for row in rows[1:]:  # Skip the header row
    columns = row.find_all("td")
    if len(columns) >= 4:  # Ensure there are enough columns
        star_names.append(columns[0].get_text().strip())
        star_distances.append(columns[1].get_text().strip())
        star_magnitudes.append(columns[2].get_text().strip())
        star_spectral_classes.append(columns[3].get_text().strip())

# Step 8: Create a DataFrame using pandas
data = {
    "Name": star_names,
    "Distance": star_distances,
    "Magnitude": star_magnitudes,
    "Spectral Class": star_spectral_classes
}

df = pd.DataFrame(data)

# Step 9: Create a CSV file
csv_filename = "brightest_stars.csv"
df.to_csv(csv_filename, index=False)

print("Data has been scraped and saved to", csv_filename)

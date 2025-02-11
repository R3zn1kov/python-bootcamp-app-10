import requests
import selectorlib
from send_email import send_email
import os
import time
import sqlite3

# "INSERT INTO events VALUES ('Eagles', 'Tiger City', '2023.10.15')"
# .commit
URL = "https://programmer100.pythonanywhere.com/tours/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


class Event:
    def scrape(self, URL):
        """"Scrape the page source from URL"""
        response = requests.get(URL, HEADERS)
        source = response.text
        return source

    # display-timer

    def extract(self, source):
        extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
        value = extractor.extract(source)["tours"]
        return value


class Database:

    def __init__(self, database_path):
        self.connection = sqlite3.connect(database_path)

    def store(self, extracted):
        row = extracted.split(",")
        row = [item.strip() for item in row]
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO events VALUES(?,?,?)", row)
        self.connection.commit()

    def read(self, extracted):
        row = extracted.split(",")
        if len(row) != 3:
            print(f"Unexpected format: {extracted}")
            return None
        row = [item.strip() for item in row]
        band, city, date = row
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM events WHERE band=? AND city=? AND date=?", (band, city, date))
        rows = (cursor.fetchall())
        print(rows)
        return rows


if __name__ == "__main__":
    while True:
        event = Event()
        scraped = event.scrape(URL)
        extracted = event.extract(scraped)
        print(extracted)

        if extracted != "No Upcoming Tours":
            database = Database(database_path="data.db")
            row = database.read(extracted)
            if row is None:
                print("Skipping this iteration due to unexpected format.")
                continue
            if not row:
                database.store(extracted)
                send_email(message="Yo, niente concerti")
        time.sleep(2)

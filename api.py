import os
from cachetools import TTLCache
from bs4 import BeautifulSoup
from fastapi.middleware.cors import CORSMiddleware
import time
import re
import requests
import subprocess
import json
from fastapi import FastAPI, Path, HTTPException


app = FastAPI()


origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def validate_semester(semester: str):
    if not re.match(r'^\d{5}$', semester):
        raise HTTPException(
            status_code=500, detail=f"Semester code should have 5 digits")
    return int(semester)


cache = TTLCache(maxsize=1000, ttl=300)


def get_timetable_data(campus: str, semester: int):
    file_name = f"timetable_data_{semester}_{campus}.json"
    timetable_data = cache.get(file_name)

    if timetable_data is not None:
        # Return cached data
        return timetable_data

    # Check if file exists, update timetable until it is available
    while not os.path.exists(file_name):
        result = subprocess.run(["python3", "scraper.py", "--semester", str(
            semester), "--campus", campus], capture_output=True, text=True)

        if result.returncode != 0:
            raise HTTPException(
                status_code=500, detail=f"Error occurred while updating timetable: {result.stderr}")

        time.sleep(10)

    # Load timetable data from file
    with open(file_name, "r") as file:
        timetable_data = json.load(file)

    # Cache the timetable data for 5 minutes
    cache[file_name] = timetable_data

    return timetable_data


@app.get("/timetable_data/{campus}/{semester}")
async def read_timetable_data(campus: str, semester: str):
    semester = validate_semester(semester)
    timetable_data = get_timetable_data(campus, semester)

    return timetable_data

cache = TTLCache(maxsize=1, ttl=3600)


@app.get("/latest_semester_codes")
async def get_latest_semester_codes():
    # Check if semester codes are already cached
    if "latest_semester_codes" in cache:
        return cache["latest_semester_codes"]

    # If not, scrape the website to get the latest semester codes
    url = "http://etimetable.unisel.edu.my"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all anchor tags with the semester code
    sa_codes = []
    bj_codes = []
    f_codes = []

    sa_table = soup.find_all('table')[0]
    bj_table = soup.find_all('table')[1]
    f_table = soup.find_all('table')[2]

    sa_links = sa_table.find_all('a')
    bj_links = bj_table.find_all('a')
    f_links = f_table.find_all('a')

    for link in sa_links:
        sa_codes.append(link.text.split()[-1])

    for link in bj_links:
        bj_codes.append(link.text.split()[-1])

    for link in f_links:
        f_codes.append(link.text.split()[-1])

    sa_codes[0] = sa_codes[0].replace('(', '').replace(')', '')
    bj_codes[0] = bj_codes[0].replace('(', '').replace(')', '')
    f_codes[0] = f_codes[0].replace('(', '').replace(')', '')

    latest_semester_codes = {
        "SA": sa_codes,
        "BJ": bj_codes,
        "F": f_codes
    }

    # Cache the semester codes for future requests
    cache["latest_semester_codes"] = latest_semester_codes

    return latest_semester_codes

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

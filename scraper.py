
import sys
import re
import json
import requests
from bs4 import BeautifulSoup

if len(sys.argv) < 3:
    print("Usage: script.py --semester <semester_number>")
    sys.exit(1)

if sys.argv[1] == "--semester" and sys.argv[2].isnumeric():
    semester = int(sys.argv[2])
else:
    print("Please enter a correct semester")
    sys.exit(1)

def fetch_data(campus, semester):
    subjectPage = requests.get(f"http://etimetable.unisel.edu.my/{campus}{semester}/{campus}{semester}_subjects_days_vertical.html")
    teachersPage = requests.get(f"http://etimetable.unisel.edu.my/{campus}{semester}/{campus}{semester}_teachers_days_vertical.html")

    subjectSoup = BeautifulSoup(subjectPage.content, 'html.parser')
    teachersSoup = BeautifulSoup(teachersPage.content, 'html.parser')

    subjects = subjectSoup.find_all('li')
    lecturers = teachersSoup.find_all('li')
    availSub = subjectSoup.select("table > tbody > tr")
    
    def process_names(items):
        names = []
        for item in items:
            item = item.text.strip('\n').strip()
            if 'Subject' in item:
                item = item.replace('Subject', '').strip()
            names.append({"subject": item})
        return names

    lecturers_data = process_names(lecturers)
    subjects_data = process_names(subjects)
    
    def get_day_from_index(index, campus):    
        if (campus == "SA"):
            days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
            return days[index % 7]
        else:
            days = ["monday", "tuesday", "wednesday", "thursday", "friday"]
            return days[index % 5]

    subjects_time_data = {}
    idx = 0
    
    for time in availSub:
        time = time.text.strip('\n').strip()
        time = re.split('\n', time)
      
        if any("Timetable generated with FET" in t for t in time):
            continue
        
       
        time.pop(0)
        
       
     
        
        day = get_day_from_index(idx, campus)

        if (campus == "SA"):
            subject_id = idx // 7
        else: 
            subject_id = idx // 5

        if subject_id not in subjects_time_data:
            subjects_time_data[subject_id] = {}

        subjects_time_data[subject_id][day] = time
        idx += 1

    return {
        "lecturers": lecturers_data,
        "subjects": subjects_data,
        "subjectsTime": subjects_time_data
    }

campus_data = {}

for campus in ["SA", "BJ"]:
    campus_data[campus] = fetch_data(campus, semester)

with open(f"timetable_data_{semester}.json", "w") as outfile:
    json.dump(campus_data, outfile, indent=2)

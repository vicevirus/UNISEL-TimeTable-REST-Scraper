from fastapi import FastAPI, Path, HTTPException
import json
import subprocess
import re
from fastapi.middleware.cors import CORSMiddleware

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
        raise HTTPException(status_code=500, detail=f"Semester code should have 5 digits")
    return int(semester)

@app.get("/timetable_data/{semester}")
async def get_timetable_data(semester: str):
    semester = validate_semester(semester)
    file_name = f"timetable_data_{semester}.json"

    try:
        with open(file_name, "r") as file:
            timetable_data = json.load(file)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")

    return timetable_data

@app.get("/update_timetable/{semester}")
async def update_timetable(semester: str):
    semester = validate_semester(semester)
    result = subprocess.run(["python3", "scraper.py", "--semester", str(semester)], capture_output=True, text=True)

    if result.returncode != 0:
        raise HTTPException(status_code=500, detail=f"Error occurred while updating timetable: {result.stderr}")
    
    return {"message": "Timetable updated successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

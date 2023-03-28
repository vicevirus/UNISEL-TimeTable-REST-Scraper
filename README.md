# UNISEL-TimeTable-FastAPI-Scraper


This API provides timetable data for different campuses and semesters. The data is scraped from the [Universiti Selangor (UNISEL) e-timetable website](http://etimetable.unisel.edu.my) using a web scraper.

## Requirements

This API requires the following packages to be installed:

- `cachetools`
- `bs4`
- `fastapi`
- `requests`
- `uvicorn`

These can be installed by running the following command:
```
pip install cachetools bs4 fastapi requests uvicorn
```

## Usage

To start the API server, run the following command:
```
python api.py
```
By default, the server will listen on `http://localhost:8000`. You can change the host and port by passing the `--host` and `--port` arguments to the `uvicorn.run` method in `app.py`.

### Endpoints

#### `GET /timetable_data/{campus}/{semester}`

Returns the timetable data for the specified campus and semester.

##### Parameters

- `campus` (string, required): The campus code (`SA`, `BJ`, or `F`).
- `semester` (string, required): The semester code (5 digits, e.g. `20182`).

##### Response

Returns a JSON object with the timetable data.

#### `GET /latest_semester_codes`

Returns the latest semester codes for each campus.

##### Response

Returns a JSON object with the latest semester codes for each campus (`SA`, `BJ`, and `F`).
Returns a JSON object with the latest semester codes for each campus (`SA`, `BJ`, and `F`).

# UNISEL Timetable API

This is an API that provides timetable data for students of Universiti Selangor (UNISEL). The API uses FastAPI framework and Redis for caching. The API also scrapes the university's website to get the latest semester codes and timetable data.

## Endpoints

### `GET /`

This endpoint returns a welcome message and a link to the Github page of the project.

### `GET /timetable_data/{campus}/{semester}`

This endpoint takes two parameters:

- `campus`: The campus code. It can be `SA` for Shah Alam, `BJ` for Bestari Jaya, or `F` for Flexi mode.
- `semester`: The semester code. It should be a 5-digit integer.

The endpoint returns the timetable data for the specified campus and semester. If the data is not available in the Redis cache, the API scrapes the university's website and updates the Redis cache with the latest data.

### `GET /latest_semester_codes`

This endpoint returns the latest semester codes for each campus. The data is scraped from the university's website.

## Dependencies

The API uses the following Python libraries:

- `os`
- `re`
- `subprocess`
- `ujson`
- `time`
- `requests`
- `BeautifulSoup`
- `fastapi`
- `redis`
- `uvicorn`

## Running the API

To run the API, use the following command:
```
python3 api.py
```

The API runs on `https://localhost:8000`.

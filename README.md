# History Timeline

A personal web app for recording and exploring historical events. Built with Python and Flask, containerized with Docker, and deployed via a CI/CD pipeline using GitHub Actions and Docker Hub.

![CI](https://github.com/JLChoran/timeline/actions/workflows/ci.yml/badge.svg)

---

## Features

- Add historical events with a date, title, category, and description
- View all events sorted chronologically on a timeline
- Filter events by category (War, Science, Politics, Art, etc.)
- Delete events
- Mobile-friendly — usable from a phone browser

## Tech Stack

| Layer | Technology |
|---|---|
| Web framework | Python / Flask |
| Data storage | JSON file |
| Containerization | Docker |
| CI/CD | GitHub Actions |
| Container registry | Docker Hub |

## Running Locally

**Prerequisites:** Python 3.12+

```bash
# Clone the repo
git clone https://github.com/JLChoran/timeline.git
cd timeline

# Install dependencies
pip install -r requirements.txt

# Start the app
python run.py
```

Open [http://localhost:5000](http://localhost:5000) in your browser.

## Running with Docker

```bash
# Build the image
docker build -t timeline .

# Run the container
docker run -p 5000:5000 timeline
```

Open [http://localhost:5000](http://localhost:5000) in your browser.

## Running Tests

```bash
pip install pytest
pytest tests/ -v
```

## CI/CD Pipeline

Every push to `main` or `dev` triggers the pipeline:

```
Push to GitHub
     │
     ▼
┌─────────────────┐
│  Lint & Test    │  flake8 (lint) + pytest (12 tests)
└────────┬────────┘
         │ passes
         ▼
┌─────────────────┐
│ Build & Push    │  docker build → push to Docker Hub
│ (main only)     │  tagged with commit SHA + :latest
└─────────────────┘
```

Secrets required (set in GitHub repo → Settings → Secrets):

| Secret | Description |
|---|---|
| `DOCKER_USERNAME` | Docker Hub username |
| `DOCKER_PASSWORD` | Docker Hub access token |

## Project Structure

```
timeline/
├── app/
│   ├── __init__.py        # Flask app factory
│   ├── data.py            # JSON read/write layer
│   ├── routes.py          # URL routes
│   ├── templates/         # HTML templates
│   └── static/            # CSS
├── tests/
│   ├── test_data.py       # Data layer tests
│   └── test_routes.py     # Route tests
├── .github/workflows/
│   └── ci.yml             # GitHub Actions pipeline
├── Dockerfile
├── requirements.txt
└── run.py                 # App entry point
```

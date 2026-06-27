# Flask Docker CI/CD Project

A simple Flask web application containerized with Docker and deployed automatically via a GitHub Actions CI/CD pipeline.

---

## Project Structure

```
proyecto_4/
├── app.py                        # Flask application
├── test_app.py                   # Unit tests (pytest)
├── requirements.txt              # Python dependencies
├── Dockerfile                    # Container image definition
├── .dockerignore                 # Files excluded from the Docker build context
├── .github/
│   └── workflows/
│       └── ci.yml                # GitHub Actions CI/CD pipeline
└── README.md                     # Project documentation
```

---

## Application

The Flask application exposes a single route:

| Route | Method | Response                                          |
|-------|--------|---------------------------------------------------|
| `/`   | GET    | `Hello, World! Welcome to the Flask application.` |

---

## Requirements

- Python 3.12+
- Docker
- A Docker Hub account
- A GitHub repository with Actions enabled

---

## Running Locally

### Without Docker

```bash
pip install -r requirements.txt
python app.py
```

Access the application at `http://localhost:5000`.

### With Docker

```bash
docker build -t flask-app .
docker run -p 5000:5000 flask-app
```

Access the application at `http://localhost:5000`.

---

## Running Tests

```bash
pip install -r requirements.txt
pytest test_app.py -v
```

The test suite verifies:

- The root route returns HTTP 200.
- The response body contains the greeting message.
- The response content type is `text/html; charset=utf-8`.

---

## Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

- **Base image**: `python:3.12-slim` — official, minimal Python image.
- **WORKDIR**: sets `/app` as the working directory inside the container.
- **Dependencies**: installed from `requirements.txt` before copying source code to take advantage of Docker layer caching.
- **EXPOSE 5000**: documents the port Flask listens on.
- **CMD**: starts the Flask development server.

---

## CI/CD Pipeline (GitHub Actions)

The pipeline defined in `.github/workflows/ci.yml` runs on every push or pull request to `main` and has two sequential jobs:

### Job 1 — `test`

1. Checks out the repository.
2. Sets up Python 3.12.
3. Installs dependencies from `requirements.txt`.
4. Runs `pytest test_app.py -v`.

The next job is blocked until all tests pass.

### Job 2 — `build-and-push`

1. Checks out the repository.
2. Logs in to Docker Hub using repository secrets.
3. Builds the Docker image with Buildx (with GitHub Actions layer cache).
4. Pushes two tags to Docker Hub:
   - `<username>/flask-app:latest`
   - `<username>/flask-app:<git-sha>`

---

## Configuring Docker Hub Secrets in GitHub

1. Go to your GitHub repository → **Settings** → **Secrets and variables** → **Actions**.
2. Click **New repository secret** and add the following two secrets:

   | Secret name          | Value                                       |
   |----------------------|---------------------------------------------|
   | `DOCKERHUB_USERNAME` | Your Docker Hub username                    |
   | `DOCKERHUB_TOKEN`    | A Docker Hub access token (not your password) |

3. To generate a Docker Hub access token: Docker Hub → **Account Settings** → **Personal access tokens** → **Generate new token**.

---

## Verifying the Deployed Image

Once the pipeline completes successfully, pull and run the published image:

```bash
docker pull <your-dockerhub-username>/flask-app:latest
docker run -p 5000:5000 <your-dockerhub-username>/flask-app:latest
```

Then open `http://localhost:5000` — you should see:

```
Hello, World! Welcome to the Flask application.
```

---

## Dependencies

| Package | Version | Purpose              |
|---------|---------|----------------------|
| Flask   | 3.1.1   | Web framework        |
| pytest  | 8.3.5   | Unit testing         |

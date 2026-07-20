FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Docker sees requirements.txt and only re-installs if it changed to make builds faster. The rest of the code is copied after this step to avoid unnecessary re-installation of dependencies.
COPY . .

# starts the Gunicorn server, listens on port 5000 and accepts connections from outside the container
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip --default-timeout=100 install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

# Define the environment variable for Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

# Start the Flask application
CMD ["flask", "run"]
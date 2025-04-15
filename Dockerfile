FROM python:3.11-slim

WORKDIR /app

# COPY requirements.txt .

# Install numpy separately to ensure compatibility
RUN pip install numpy==1.23.5

# Install pandas and other dependencies
RUN pip install pandas==1.5.3 scikit-learn==1.2.2 Flask==2.3.2 joblib==1.3.0


# RUN pip --default-timeout=100 install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

# Define the environment variable for Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

# Start the Flask application
CMD ["flask", "run"]
# Get official python image
FROM python:3.9-slim-buster

# Define work directory
WORKDIR /app

# Copy file with dependencies and setup it
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest files
COPY . .

# Open port 5000
EXPOSE 5000

# Run web-app
CMD [ "python", "app.py" ]

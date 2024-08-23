# Use the official Python image
FROM python:3.11

# Install poppler-utils
RUN apt-get update && apt-get install -y poppler-utils

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files
COPY . .

# Expose the port
EXPOSE 8000

# Set default commands based on the role
ENTRYPOINT []
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

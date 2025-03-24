# Use the official Python image from the Docker Hub
FROM python:3.11

# Set the working directory
WORKDIR /MDS_Tehnicki_zadatak

# its important to install these prior to the django init because django does not have them
RUN pip install pydantic requests

# Copy the requirements file to the container
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Install PostgreSQL driver and other necessary tools
RUN apt-get update && apt-get install -y \
    libpq-dev gcc \
    && apt-get clean

# Copy the entire project to the container
COPY . .

# Run migrations and collect static files
# RUN python manage.py collectstatic --noinput

# Expose the port that the app runs on
EXPOSE 8000

# Command to run the Django server
# CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "MDS_Tehnicki_zadatak.wsgi:application"]
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "MDS_Tehnicki_zadatak.wsgi:application"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

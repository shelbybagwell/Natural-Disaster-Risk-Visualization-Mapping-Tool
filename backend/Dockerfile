# Use official Python image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Install Updates
RUN apt-get update

# Copy project files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
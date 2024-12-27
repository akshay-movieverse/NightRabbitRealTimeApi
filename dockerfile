# Use the official Python image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Flask will run on
EXPOSE 5000

# Command to run the app
CMD ["gunicorn", "-w", "4", "-b", "192.168.1.50:5000", "app:app"]

# Use the official image based on Python 3.13.
FROM python:3.13-slim

# Set the working directory
WORKDIR /app

# Install the necessary system packages (for PostgreSQL connection)
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# Copy and upload dependencies.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Run FastApi
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
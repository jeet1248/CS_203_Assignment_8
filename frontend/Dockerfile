# Use a lightweight Python base image.
FROM python:3.9-slim

WORKDIR /app

# Copy and install dependencies.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code.
COPY main.py .

# Expose port 9567 so that it can be mapped to the host.
EXPOSE 9567

# Run the FastAPI app using Uvicorn.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9567"]
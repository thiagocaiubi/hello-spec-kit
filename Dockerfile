# Use an official Python base image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install uv for dependency management
RUN pip install uv

# Copy only pyproject.toml first for better caching
COPY pyproject.toml .

# Install dependencies from pyproject.toml
RUN uv pip install --system -e .

# Copy the rest of the application
COPY . .

# Expose FastAPI default port
EXPOSE 8000

# Command to run FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

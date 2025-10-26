FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy API code
COPY api/ ./api/

# Expose port (Hugging Face uses 7860)
EXPOSE 7860

# Run the API
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "7860"]


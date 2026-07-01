# Step 1: Build stage with lightweight Python image
FROM python:3.11-slim as builder
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Step 2: Final minimal execution image
FROM python:3.11-slim
WORKDIR /app

# Copy virtual environment from builder stage
COPY --from=builder /opt/venv /opt/venv

# Copy your Streamlit app and startup dataset explicitly
COPY app.py .
COPY startup_clean.csv .

ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1
ENV STREAMLIT_HOME=/app 

# Fix Permissions for appuser
RUN useradd -u 8888 appuser && \
    chown -R appuser:appuser /app && \
    chown -R appuser:appuser /opt/venv

USER appuser

EXPOSE 8501

# Using absolute path to avoid "executable file not found" error
CMD ["/opt/venv/bin/streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
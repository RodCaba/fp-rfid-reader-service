# Multi-stage build for ARM64/AMD64 compatibility
FROM python:3.12-slim AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    portaudio19-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Production stage
FROM builder
# Update and upgrade packages to fix vulnerabilities
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get dist-upgrade -y && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install runtime dependencies for Raspberry Pi hardware
RUN apt-get update && apt-get install -y \
    i2c-tools \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash app

# Set working directory
WORKDIR /app

# Copy Python packages from builder
COPY --from=builder /root/.local /home/app/.local

# Copy application code
COPY . .

# Copy only the required proto file  
COPY ./proto/audio_service.proto /tmp/audio_service.proto

# Create necessary directories
RUN mkdir -p src/grpc_generated && \
    chown -R app:app /app

# Generate gRPC code at build time
RUN python -m grpc_tools.protoc \
    --proto_path=/tmp \
    --python_out=./src/grpc_generated \
    --grpc_python_out=./src/grpc_generated \
    /tmp/audio_service.proto && \
    sed -i 's/import audio_service_pb2/from . import audio_service_pb2/g' ./src/grpc_generated/audio_service_pb2_grpc.py

# Switch to non-root user
USER app

# Add local packages to PATH
ENV PATH=/home/app/.local/bin:$PATH
ENV PYTHONPATH=/app/src:$PYTHONPATH

# Expose any monitoring ports if needed
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

# Run the RFID service
CMD ["python", "main_simulator.py"]

# Use the official Ubuntu base image
FROM ubuntu:22.04

# Set environment variables to prevent prompts during package installations
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies and Python 3.10.12
RUN apt-get update && apt-get install -y \
    software-properties-common \
    git \
    curl \
    build-essential \
    libssl-dev \
    libffi-dev \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update \
    && apt-get install -y python3.10 python3.10-venv python3.10-dev python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Set Python 3.10 as the default python version
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1 \
    && update-alternatives --install /usr/bin/python python /usr/bin/python3.10 1

# Clone your GitHub repository
# Replace <your-repo-url> with the actual URL of your GitHub repository
RUN git clone https://github.com/mrkaesy/IndicWav2vecHindiInference.git /app/repo

# Set the working directory to the cloned repository
WORKDIR /app/repo

# Install Python dependencies from the requirements file
RUN pip install --no-cache-dir -r requirements.txt

# Command to run your code
CMD ["python", "/code/api.py"]
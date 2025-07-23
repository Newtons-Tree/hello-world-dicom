# Other base image versions available at https://hub.docker.com/r/pytorch/pytorch
FROM pytorch/pytorch:2.7.1-cuda11.8-cudnn9-runtime

# Define the in-container working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the script to the container working directory
COPY main.py .

# Ensure /data exists with correct permissions
RUN mkdir -p /data/in /data/out
RUN chown -R 999:999 /data

# Switch to a non-privileged user:group
USER 999:999

# Command to execute
# For local testing, these paths are mapped
# onto the local filesystem during the run command.
CMD ["python", "main.py", "/data/in", "/data/out"]
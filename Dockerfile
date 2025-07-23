# Other base image versions available at https://hub.docker.com/r/pytorch/pytorch
FROM pytorch/pytorch:2.7.1-cuda11.8-cudnn9-runtime

# Define the in-container working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the script to the container working directory
COPY main.py .

# Ensure /tmp exists with correct permissions
RUN mkdir -p /tmp && chmod 1777 /tmp

# Command to execute
# Containers run without root privileges, so we use
# the /tmp path within the container to prevent issues
# with permissions. For local testing, these paths are
# mapped onto the local filesystem during the run command.
CMD ["python", "main.py", "/tmp/in", "/tmp/out"]
# Use the official Jenkins LTS image as the base
FROM jenkins/jenkins:lts

# Switch to root user to install system dependencies
USER root

# Install prerequisites
RUN apt-get update -y && \
    apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    software-properties-common

# Install Docker CLI (Allows Jenkins to run 'docker build')
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add - && \
    echo "deb [arch=amd64] https://download.docker.com/linux/debian bullseye stable" > /etc/apt/sources.list.d/docker.list && \
    apt-get update -y && \
    apt-get install -y docker-ce docker-ce-cli containerd.io

# Install AWS CLI (Required for ECR/ECS interaction)
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install && \
    rm awscliv2.zip

# Create 'docker' group and add 'jenkins' user to it
# This ensures Jenkins can run docker commands without sudo
RUN groupadd -f docker && \
    usermod -aG docker jenkins

# Clean up to keep image small
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Switch back to Jenkins user for security
USER jenkins
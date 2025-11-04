# Use the official Jenkins LTS image as base
FROM jenkins/jenkins:lts

USER root

# Install Docker inside Jenkins container
RUN apt-get update -y && \
    apt-get install -y ca-certificates curl gnupg lsb-release && \
    mkdir -p /etc/apt/keyrings && \
    curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg && \
    echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list && \
    apt-get update -y && \
    apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin && \
    usermod -aG docker jenkins && \
    apt-get clean

USER jenkins

EXPOSE 8080
EXPOSE 50000

ENTRYPOINT ["/usr/bin/tini", "--", "/usr/local/bin/jenkins.sh"]

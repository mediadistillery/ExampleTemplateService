FROM python:3.8-slim AS builder
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    build-essential
ARG USERNAME=example-service-template-service
ARG VERSION
RUN test -n "${VERSION}" || (echo "VERSION not set" && false)
RUN useradd -u 1001 -m -s /bin/bash ${USERNAME}
USER ${USERNAME}
COPY requirements.txt /
RUN pip install setuptools wheel --no-cache-dir \
 && pip install -r requirements.txt --user \
 && pip install . --user

FROM python:3.8-slim
ARG USERNAME=example-service-template-service
RUN useradd -u 1001 -m -s /bin/bash ${USERNAME}
USER ${USERNAME}
ENV PATH="/home/${USERNAME}/.local/bin:${PATH}"
COPY --from=builder --chown=1001 /home/${USERNAME}/.local /home/${USERNAME}/.local
COPY default_config.yml /etc/${USERNAME}/config.yml
ENV REMOTE_CONFIG_URL=/etc/${USERNAME}/config.yml
EXPOSE 5000 8080
CMD ["run-cli"]

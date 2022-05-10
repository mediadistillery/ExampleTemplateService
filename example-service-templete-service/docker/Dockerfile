FROM python:3.8.10-slim AS builder

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake
ARG USERNAME=md-dl-face-clustering-service
ARG VERSION
RUN test -n "${VERSION}" || (echo "VERSION not set" && false)
RUN useradd -u 1001 -m -s /bin/bash ${USERNAME}
USER ${USERNAME}
ENV PATH="/home/${USERNAME}/.local/bin:${PATH}"

COPY requirements.txt /
RUN pip install setuptools wheel --no-cache-dir
RUN pip install \
    --extra-index-url=http://nexus/repository/md-pypi/simple \
    --trusted-host=nexus \
    -r requirements.txt --user

FROM python:3.8.10-slim
ARG DEBIAN_FRONTEND=noninteractive
ARG USERNAME=md-dl-face-clustering-service
ARG VERSION
RUN test -n "${VERSION}" || (echo "VERSION not set" && false)
RUN useradd -u 1001 -m -s /bin/bash ${USERNAME}
USER ${USERNAME}
ENV PATH="/home/${USERNAME}/.local/bin:${PATH}"
COPY --from=builder --chown=1001 /home/${USERNAME}/.local /home/${USERNAME}/.local

RUN pip install \
    --extra-index-url=http://nexus/repository/md-pypi/simple \
    --trusted-host=nexus \
    ${USERNAME}==${VERSION} --user

ENV REMOTE_CONFIG_URL=http://md-spring-cloud-config/${USERNAME}/master
EXPOSE 5000 8080 8000
CMD ["face_clustering_service_web_start"]

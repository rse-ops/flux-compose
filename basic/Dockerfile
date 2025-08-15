ARG flux_sched_version=jammy
FROM fluxrm/flux-sched:${flux_sched_version} AS builder
ARG replicas=3
ENV workers=${replicas}
USER root

RUN apt-get update
RUN DEBIAN_FRONTEND="noninteractive" apt-get -y install \
    autotools-dev \
    autoconf \
    automake \
    cmake \
    git \
    python3 \
    openssh-server \
    openssh-client \
    libdb-dev \
    apt-utils \
    dnsutils \
    iputils-ping \
    python3-pip \
    software-properties-common

# These are the STATE_DIR, system, and resources directories
ENV STATE_DIR=/var/lib/flux
RUN mkdir -p ${STATE_DIR} /etc/flux/system /etc/flux/system/cron.d /etc/flux/config /run/flux && \
    mkdir -p /etc/flux/system/cron.d && \
    mkdir -p /mnt/curve && \
    flux keygen /mnt/curve/curve.cert && \
    # Important: "basic" is the directory name here
    flux R encode --hosts="node-[1-${workers}]" > /etc/flux/system/R && \
    chown -R fluxuser:fluxuser /run/flux ${STATE_DIR} /mnt/curve/curve.cert ${workdir}

WORKDIR /home/fluxuser
RUN pip3 install --upgrade pip && \
    pip3 install pika --upgrade && \
    chown -R fluxuser:fluxuser /home/fluxuser && \
    chown -R fluxuser:fluxuser /run/flux

USER fluxuser
WORKDIR /home/fluxuser/
COPY ./scripts/entrypoint.sh ./scripts/job.py ./
ENTRYPOINT /bin/bash /home/fluxuser/entrypoint.sh

ARG BUILD_FROM
FROM $BUILD_FROM
ARG BUILD_VERSION

ENV LANG C.UTF-8

COPY requirements.txt rootfs /

RUN apk add --update \
    --no-cache \
    --virtual build-dependencies \
    python3 \
    py3-pip \
    apache2-utils \
    && python3 -m pip install --no-cache-dir --upgrade -r /requirements.txt

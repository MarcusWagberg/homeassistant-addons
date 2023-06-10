ARG BUILD_FROM
FROM $BUILD_FROM
ARG BUILD_VERSION

ENV LANG C.UTF-8
ENV TEST_OPTIONS=0

COPY requirements.txt options.test.json rootfs /

RUN apk add --update \
    --no-cache \
    --virtual build-dependencies \
    python3 \
    py3-pip \
    && python3 -m pip install --no-cache-dir --upgrade -r /requirements.txt
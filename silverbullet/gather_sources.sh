#!/bin/bash

UNAME_ARCH=$(uname -m)
DOCKER_ARCH=""

if [ "$UNAME_ARCH" == "x86_64" ]; then
    DOCKER_ARCH="amd64"
elif [ "$UNAME_ARCH" == "aarch64" ]; then
    DOCKER_ARCH="aarch64"
else
    echo "unknown arch"
    exit 1
fi

mkdir /sources
cd /sources

while IFS="" read -r p || [ -n "$p" ]; do
    if [ ! -z "$p" ]; then
        url=${p% @ *}
        arch=${p#* @ }

        if [ "$arch" == "all" ] || [ "$arch" == "$DOCKER_ARCH" ]; then
            printf 'downloading %s\n' "$url"
            curl -L -O "$url"
        fi
    fi
done < /sources.txt

find . -name "*.zip" -exec bash -c "unzip {} && rm {}" \;
find . -name "*.tar.gz" -exec bash -c "tar -xzvf {} && rm {}" \;
find . -name "*.tar.bz2" -exec bash -c "tar -xjvf {} && rm {}" \;
find . -name "*.tar" -exec bash -c "tar -xvf {} && rm {}" \;

rm /sources.txt

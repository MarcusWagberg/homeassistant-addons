#!/usr/bin/env python3

from sys import argv
from time import sleep
from os import environ
from docker import DockerClient

import common
import build

def print_usage():
    print(f"Usage: {argv[0]} [addon]")
    print()
    print("Addons:")
    for addon in common.addons:
        print(f"    {addon}")
    print()
    exit(1)

def main():
    root = common.get_root_path()

    if len(argv)-1 != 1:
        print_usage()

    if argv[1] not in common.addons:
        print(f"No addon named: {argv[1]}")
        exit(1)

    addon = argv[1]

    if not build.build(addon, f"{root}/{addon}", False):
        print(">>> Build Unsuccessful <<<")
        exit(1)

    image = f"local/hass-{addon}-{common.get_arch()}"

    print(f">>> Running {addon} ({image}) <<<")

    socat = common.start_socat()
    sleep(2)

    docker_client = DockerClient(base_url=f'unix:/{environ["HOME"]}/.docker.sock')
    container = docker_client.containers.run(
        image,
        detach=True,
        remove=True,
        stdout=True,
        stderr=True,
        environment=[
            "TEST_OPTIONS=1"
        ]
    )
    output = container.attach(stdout=True, stream=True, logs=True)


    try:
        for line in output:
            print(line.decode(), end="")
        socat.kill()
    except KeyboardInterrupt:
        container.remove(force=True)
        socat.kill()
        exit(1)

if __name__ == "__main__":
    main()

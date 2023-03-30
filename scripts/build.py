#!/bin/sh
"exec" "`dirname $0`/../.venv/bin/python" "$0" "$@"

from sys import argv
from docker import from_env

import common

def print_usage():
    print(f"Usage: {argv[0]} [addon]")
    print()
    print("Addons:")
    for addon in common.addons:
        print(f"    {addon}")
    print()
    exit(1)

def build(addon_name: str, addon_path, all_arch: bool) -> bool:
    print(f">>> Building {addon_name} <<<")
    arch_arg = " --all" if all_arch else f" --{common.get_arch()}"

    docker_client = from_env()
    container = docker_client.containers.run(
        f"homeassistant/{common.get_arch()}-builder",
        f"-t /data --test -i hass-{addon_name}-{{arch}} -d local {arch_arg}",
        name="builder",
        volumes=[
            f"{addon_path}:/data",
            "/var/run/docker.sock:/var/run/docker.sock:ro"
        ],
        tty=True,
        privileged=True,
        detach=True,
        remove=True,
        stdout=True,
        stderr=True,
    )
    output = container.attach(stdout=True, stream=True, logs=True)

    for line in output:
        print(line.decode(), end="")

    exit = container.wait()
    if exit["StatusCode"] == 0:
        return True
    else:
        return False

def main():
    root = common.get_root_path(argv[0])
    
    if len(argv)-1 != 1:
        print_usage()

    if argv[1] not in common.addons:
        print(f"No addon named: {argv[1]}")
        exit(1)

    addon = argv[1]

    if build(addon, f"{root}/{addon}", True):
        print(">>> Build Successful <<<")
    else:
        print(">>> Build Unsuccessful <<<")

if __name__ == "__main__":
    main()

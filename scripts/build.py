#!/usr/bin/env python3

from sys import argv
from os import environ
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

    socat = common.start_socat()

    docker_client = from_env()
    container = docker_client.containers.run(
        f"homeassistant/{common.get_arch()}-builder",
        f"-t /data --test -i hass-{addon_name}-{{arch}} -d local {arch_arg}",
        name="builder",
        volumes=[
            f"{addon_path}:/data",
            f'{environ["HOME"]}/.docker.sock:/var/run/docker.sock:ro'
        ],
        tty=True,
        privileged=True,
        detach=True,
        remove=True,
        stdout=True,
        stderr=True,
    )
    output = container.attach(stdout=True, stream=True, logs=True)

    fail = True

    for line in output:
        decoded_line = line.decode()
        print(decoded_line, end="")
        if "Finish build for" in decoded_line:
            fail = False

    exit = container.wait()
    socat.kill()
    if fail:
        return False
    else:
        return True

def main():
    root = common.get_root_path()
    
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

#!/usr/bin/env python3

from sys import argv
from git import Repo
from os import environ
from docker import from_env
from yaml import load, dump, SafeLoader, SafeDumper

import common

def print_usage():
    print(f"Usage: {argv[0]} [addon] [version]")
    print()
    print("Addons:")
    for addon in common.addons:
        print(f"    {addon}")
    print()
    exit(1)

def main():
    root = common.get_root_path()
    repo = Repo(root)

    if len(argv)-1 != 2:
        print_usage()

    if argv[1] not in common.addons:
        print(f"No addon named: {argv[1]}")
        exit(1)

    addon = argv[1]

    if not common.validate_version(argv[2]):
        print(f"Invalied version: {argv[2]}")
        exit(1)

    version = argv[2]

    branch = f"{addon}-{version}"

    if repo.active_branch.name != branch:
        print(f"Must publish from branch: '{branch}'")
        exit(1)

    print(f">>> Publishing {addon} ({version}) <<<")

    with open(f"{root}/{addon}/config.yaml", 'r+') as f:
        data = load(f, Loader=SafeLoader)
        data["version"] = version
        f.seek(0)
        dump(data, f, Dumper=SafeDumper, sort_keys=False, default_flow_style=False)
        f.truncate()

    docker_client = from_env()
    container = docker_client.containers.run(
        f"homeassistant/{common.get_arch()}-builder",
        f'-t /data --docker-hub-check --all --addon --docker-hub "ghcr.io/marcuswagberg" -i "hass-{addon}-{{arch}}"',
        name="builder",
        volumes=[
            f"{root}/{addon}:/data",
            f'{environ["HOME"]}/.docker:/root/.docker',
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

    container_exit = container.wait()
    if container_exit["StatusCode"] != 0:
        print(">>> Publishing Unsuccessful <<<")
        exit(1)
    
    repo.git.add(f"{addon}/config.yaml")
    repo.git.commit("-m", f"Publish {addon} {version}")
    
    active_branch = repo.active_branch.name
    repo.heads.main.checkout()
    repo.git.merge(active_branch)

    repo.remotes.origin.push(refspec='main:main')

if __name__ == "__main__":
    main()

#!/usr/bin/env python3

from sys import argv
from json import loads
from os.path import exists
from requirements import parse
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import common

def check_requirements_txt(requirements_path: str):
    num_outdated = 0
    requirements = {}

    with open(requirements_path, "r", encoding="utf-8") as fd:
        for requirement in parse(fd):
            if not requirement.line.startswith("https://"):
                if len(requirement.specs) != 1 or requirement.specs[0][0] != "==":
                    print(f"Invalid requirement '{requirement.name} {requirement.specs}' in {requirements_path}")
                    exit(1)

                requirements[requirement.name] = {
                    "wanted": requirement.specs[0][1],
                    "latest": ""
                }

    for requirement in requirements:
        req = Request(f"https://pypi.org/pypi/{requirement}/json")
        try:
            with urlopen(req, timeout=1) as response:
                contents = response.read()
                data = loads(contents)
                requirements[requirement]["latest"] = data["info"]["version"]
        except (HTTPError, TimeoutError, URLError):
            print("Failed to connect to https://pypi.org/")
            exit(1)

    for requirement in requirements:
        if requirements[requirement]["wanted"] != requirements[requirement]["latest"]:
            num_outdated += 1

    if num_outdated > 0:
        print(f"|{'':-<80}|")
        print(f"|{requirements_path:<80}|")
        print(f"|{'':-<80}|")
        print(f"| {'Name':<42} | {'Wanted':^15} | {'latest':^15} |")
        print(f"|{'':-<80}|")
        for requirement in requirements:
            if requirements[requirement]["wanted"] != requirements[requirement]["latest"]:
                print(f"| {requirement:<42} | {requirements[requirement]['wanted']:^15} | {requirements[requirement]['latest']:^15} |")
        print(f"|{'':-<80}|")
        print()
        print()

def main():
    root = common.get_root_path()

    for addon in common.addons:
        requirements_path = f"{root}/{addon}/requirements.txt"
        if exists(requirements_path):
            check_requirements_txt(requirements_path)

if __name__ == "__main__":
    main()

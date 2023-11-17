from re import match
from platform import machine
from os import getcwd
from os.path import abspath, isfile

addons = ["intermedium", "radicale"]

def validate_version(ver: str) -> bool:
    return bool(match(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(r[1-9]\d*)?$", ver))

def get_root_path() -> str:
    cwd = getcwd()
    if f"{cwd}/repository.yaml":
        return cwd
    else:
        raise Exception("error: cwd is not root of addon repository")

def get_arch() -> str:
    arch = machine()
    if "arm" == arch:
        return "armhf"
    elif "armv7l" == arch:
        return "armv7"
    elif "x86_64" == arch:
        return "amd64"
    elif "aarch64" == arch:
        return "aarch64"
    elif "i386" == arch:
        return "i386"


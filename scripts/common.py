from re import match
from platform import machine
from os.path import abspath, dirname

addons = ["intermedium"]

def validate_version(ver: str) -> bool:
    return bool(match(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(r[1-9]\d*)?$", ver))

def get_root_path(arg0: str) -> str:
    return dirname(abspath(dirname(arg0)))

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


from re import match
from platform import machine
from os.path import abspath, isfile
from subprocess import Popen, DEVNULL
from os import getcwd, environ, remove

addons = ["intermedium", "radicale", "silverbullet"]

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

def start_socat() -> Popen:
    user_sock = f'{environ["HOME"]}/.docker.sock'
    try:
        remove(user_sock)
    except OSError:
        pass

    return Popen(["socat", "-d", "-d", f"UNIX-LISTEN:{user_sock},fork", "UNIX-CONNECT:/var/run/docker.sock"], stdout = DEVNULL, stdin = DEVNULL, stderr = DEVNULL)

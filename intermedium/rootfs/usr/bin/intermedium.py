#!/usr/bin/env python3
from os import getenv
from sys import argv
from json import loads
from requests import post
from os.path import exists
from mailparser import parse_from_string
from aiosmtpd.controller import Controller
from asyncio import AbstractEventLoop, new_event_loop, set_event_loop

TEST_CONFIG = """
{
    "users": [
        {
            "email": "intermedium@hass.local",
            "notify_service": "notify"
        }
    ]
}
"""

SUPERVISOR_TOKEN = ""
CONFIG = {}
HEADERS = {}

class IntermediumHandler:
    async def handle_RCPT(self, server, session, envelope, address, rcpt_options):
        envelope.rcpt_tos.append(address)
        return "250 OK"
    
    async def handle_DATA(self, server, session, envelope):
        for user in CONFIG["users"]:
            if envelope.rcpt_tos[0] == user["email"]:
                content = envelope.content.decode("utf8", errors="replace")
                mail = parse_from_string(content)
                data = {"title": mail.subject, "message": mail.body}

                response = post(f"http://supervisor/core/api/services/notify/{user['notify_service']}", headers=HEADERS, json=data)
                if response.ok:
                    return "250 Message accepted for delivery"
                else:
                    return "451 Requested action aborted: local error in processing"
                
        return "550 Recipient address rejected: User unknown"


async def amain(loop: AbstractEventLoop):
    cont = Controller(IntermediumHandler(), hostname="", port=8025)
    cont.start()   

if __name__ == "__main__":
    SUPERVISOR_TOKEN = getenv("SUPERVISOR_TOKEN")
    HEADERS = {"Authorization": f"Bearer {SUPERVISOR_TOKEN}"}
    if exists(argv[1]):
        with open(argv[1], "r") as f:
            CONFIG = loads(f.read())
    else:
        CONFIG = loads(TEST_CONFIG)

    loop = new_event_loop()
    set_event_loop(loop)
    loop.create_task(amain(loop=loop))

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
#! /usr/bin/env python3

# gammu_config.py
# Noah Sandman <noah@modulytic.com>
# Created 15 October 2020

# generates all config files for Gammu

import json
import os
from typing import List


# gammu single device config
#   modem_device: name of modem mountpoint
#   series: number config being generated (for gammu1, gammu2, etc.)
def __device_config(modem_device: str, series=0) -> str:
    # it's never gammu0, just gammu
    config_name: str = "gammu"
    if series != 0:
        config_name += str(series)

    return """[{config_name}]
port = {modem_device}
device = {modem_device}
connection = at
logformat = textall

""".format(config_name=config_name, modem_device=modem_device)


# https://stackoverflow.com/a/33685234/1420247
def __disk_exists(path):
    return os.path.exists(path)


def __get_dongle(num: int) -> str:
    return "/dev/mobile{}".format(num)


# list of mountpoints of all dongles, /dev/mobileX, sequentially
# if we fine one that doesn't exist, stop the loop and assume there are no more
def get_dongles() -> List[str]:
    dongles: List[str] = []

    i: int = 0
    while True:
        dongle = __get_dongle(i)
        if not __disk_exists(dongle):
            break

        dongles.append(dongle)

        i += 1

    return dongles


# Generate text of /etc/gammurc file
def gammurc(dongles: List[str]) -> str:
    file: str = ""

    for i, v in enumerate(dongles):
        file += __device_config(v, i)

    return file


# Generate text of gammu-smsdrc for each dongle
def gammusmsdrc(dongles: List[str]) -> List[str]:
    daemons: List[str] = []
    daemon_settings = """[smsd]
logfile = /var/log/gammu.log
debuglevel = 0
RunOnReceive = /app/on_receive

{smsdrc_user_text}

PhoneId = {id}"""

    for i, dongle in enumerate(dongles):
        smsdrc_user_file = None
        try:
            smsdrc_user_file = open("/app/smsdrc{}-user".format(i), "r")
        except IOError:     # If config file not defined for this daemon, use generic
            smsdrc_user_file = open("/app/smsdrc-user", "r")
        finally:
            smsdrc_user_text = smsdrc_user_file.read()
            daemon_settings = daemon_settings.format(
                smsdrc_user_text = smsdrc_user_text.format(**os.environ),
                id=i
            )

            pin = os.environ.get("PIN{}".format(i))
            if pin is not None:
                daemon_settings += "\nPIN = {}".format(pin)

            daemons.append(
                "{device_conf}\n{daemon_settings}\n".format(
                    device_conf=__device_config(dongle),
                    daemon_settings=daemon_settings
                )
            )

    return daemons


if __name__ == "__main__":
    dongles: List[str] = get_dongles()

    # Create gammu config file
    gammurc_file = open("/etc/gammurc", "w")
    gammurc_file.write(gammurc(dongles))
    gammurc_file.close()

    # Create multiple config files so we can have 1:1 daemon:modem ratio
    smsdrcs = gammusmsdrc(dongles)
    for i, smsdrc in enumerate(smsdrcs):
        smsdrc_file = open("/app/smsdrcs/smsdrc{}".format(i), "w")
        smsdrc_file.write(smsdrc)
        smsdrc_file.close()

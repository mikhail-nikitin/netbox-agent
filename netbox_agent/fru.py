import logging
import sys
import subprocess

from netbox_agent.misc import is_tool

FIELD_CHASSIS_TYPE = 'Chassis Type'
FIELD_CHASSIS_PART_NUMBER = 'Chassis Part Number'
FIELD_CHASSIS_SERIAL = 'Chassis Serial'
FIELD_BOARD_MFG = 'Board Mfg'
FIELD_BOARD_PRODUCT = 'Board Product'
FIELD_BOARD_SERIAL = 'Board Serial'
FIELD_PRODUCT_MANUFACTURER = 'Product Manufacturer'
FIELD_PRODUCT_PART_NUMBER = 'Product Part Number'
FIELD_PRODUCT_SERIAL = 'Product Serial'


def parse(output=None):
    if output:
        buffer = output
    else:
        buffer = _execute_cmd()
    if isinstance(buffer, bytes):
        buffer = buffer.decode("utf-8")
    _data = _parse(buffer)

def _execute_cmd():
    if not is_tool("ipmitool"):
        logging.error(
            "ipmi does not seem to be present on your system. Add it your path or "
            "check the compatibility of this project with your distro."
        )
        sys.exit(1)
    return subprocess.check_output(
        [
            "ipmitool",
            "fru",
            "print",
        ],
        stderr=subprocess.PIPE,
    )

def _parse(output):
    data = {}
    for line in output.splitlines():
        line = line.strip()
        if not line:
            continue
        key, value = line.split(':', maxsplit=1)
        key, value = key.strip(), value.strip()
        if not key:
            continue
        data[key] = value
    return data

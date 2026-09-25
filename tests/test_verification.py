from verification import (
    handler_entry,
    handler_success,
    handler_failure
)

from decoder import decode_space_packet, decode_pus_secondary_header
from validator import validate_space_packet, validate_pus_header


def test_handler_entry():
    report = handler_entry(17, 1)

    assert report["service"] == 1
    assert report["subtype"] == 3

    packet = report["packet"]

    decoded = decode_space_packet(packet)

    assert decoded["apid"] == 17

    validate_space_packet(packet, decoded)

    pus_header = decode_pus_secondary_header(decoded["data"])

    assert pus_header["pus_version"] == 0x20
    assert pus_header["service"] == 1
    assert pus_header["subtype"] == 3


def test_handler_success():
    report = handler_success(17, 1)

    assert report["service"] == 1
    assert report["subtype"] == 7

    packet = report["packet"]

    decoded = decode_space_packet(packet)

    assert decoded["apid"] == 17

    validate_space_packet(packet, decoded)

    pus_header = decode_pus_secondary_header(decoded["data"])

    assert pus_header["pus_version"] == 0x20
    assert pus_header["service"] == 1
    assert pus_header["subtype"] == 7


def test_handler_failure():
    report = handler_failure(
        17,
        1,
        "COMMAND_FAILED"
    )

    assert report["service"] == 1
    assert report["subtype"] == 8
    assert report["failure_code"] == "COMMAND_FAILED"

    packet = report["packet"]

    decoded = decode_space_packet(packet)

    assert decoded["apid"] == 17

    validate_space_packet(packet, decoded)

    pus_header = decode_pus_secondary_header(decoded["data"])

    assert pus_header["pus_version"] == 0x20
    assert pus_header["service"] == 1
    assert pus_header["subtype"] == 8
    
def test_handler_failure_packet_contains_failure_code():
    report = handler_failure(
        99,
        99,
        "UNSUPPORTED_COMMAND"
    )

    assert report["service"] == 1
    assert report["subtype"] == 8
    assert report["failure_code"] == "UNSUPPORTED_COMMAND"

    packet = report["packet"]

    decoded = decode_space_packet(packet)

    validate_space_packet(packet, decoded)

    pus_header = decode_pus_secondary_header(decoded["data"])

    assert pus_header["pus_version"] == 0x20
    assert pus_header["service"] == 1
    assert pus_header["subtype"] == 8
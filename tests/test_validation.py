from packet_builder import build_space_packet

from decoder import (
    decode_space_packet,
    decode_pus_secondary_header
)

from validator import (
    validate_space_packet,
    validate_pus_header,
    ValidationError
)


def test_valid_packet():

    packet = build_space_packet(
        apid=17,
        service=17,
        subtype=1,
        user_data=b"PING"
    )

    decoded = decode_space_packet(packet)

    validate_space_packet(packet, decoded)

    assert decoded["apid"] == 17


def test_valid_pus_header():

    pus_header = {
        "pus_version": 0x20,
        "service": 17,
        "subtype": 1
    }

    validate_pus_header(pus_header)


def test_invalid_pus_version():

    pus_header = {
        "pus_version": 0x10,
        "service": 17,
        "subtype": 1
    }

    try:
        validate_pus_header(pus_header)
        assert False
    except ValidationError:
        assert True


def test_invalid_service():

    pus_header = {
        "pus_version": 0x20,
        "service": 0,
        "subtype": 1
    }

    try:
        validate_pus_header(pus_header)
        assert False
    except ValidationError:
        assert True

def test_invalid_crc():
    packet = build_space_packet(
        apid=17,
        service=17,
        subtype=1,
        user_data=b"PING"
    )

    # Corrupt the last CRC byte
    bad_packet = bytearray(packet)
    bad_packet[-1] ^= 0xFF
    bad_packet = bytes(bad_packet)

    decoded = decode_space_packet(bad_packet)

    try:
        validate_space_packet(bad_packet, decoded)
        assert False
    except ValidationError:
        assert True        
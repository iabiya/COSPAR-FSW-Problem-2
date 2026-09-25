# Validation functions for Telecommand packets


from config import (
    SPACE_PACKET_VERSION,
    TELECOMMAND_TYPE,
    PUS_VERSION,
    VALID_CREDENTIALS
)

from crc import verify_crc


class ValidationError(Exception):
    pass


def validate_credentials(credentials: bytes):
    """
    Check whether the TC Transfer Frame credentials are valid.
    """

    if credentials != VALID_CREDENTIALS:
        raise ValidationError("Invalid PUS-C credentials")


def validate_space_packet(packet: bytes, decoded: dict):
    """
    Validate the Space Packet primary header and CRC.
    """

    # Check Space Packet version
    if decoded["version"] != SPACE_PACKET_VERSION:
        raise ValidationError(
            "Invalid Space Packet version"
        )

    # Check packet type
    if decoded["type"] != TELECOMMAND_TYPE:
        raise ValidationError(
            "Invalid packet type"
        )

    # Check packet length
    expected_length = 6 + decoded["data_length"] + 1 + 2

    if len(packet) != expected_length:
        raise ValidationError(
            "Invalid data length"
        )

    # Check CRC
    if not verify_crc(packet):
        raise ValidationError(
            "CRC validation failed"
        )


def validate_pus_header(pus_header: dict):
    """
    Validate the PUS-C secondary header.
    """

    # PUS version must be 0x20
    if pus_header["pus_version"] != PUS_VERSION:
        raise ValidationError(
            "Invalid PUS version"
        )

    # Service cannot be zero
    if pus_header["service"] == 0:
        raise ValidationError(
            "Service cannot be zero"
        )

    # Subtype cannot be zero
    if pus_header["subtype"] == 0:
        raise ValidationError(
            "Subtype cannot be zero"
        )
# Decoder for CCSDS-like Space Packets


class DecodeError(Exception):
    pass


def decode_space_packet(packet: bytes) -> dict:
    """
    Decode the primary header of a Space Packet.
    """

    # Primary header requires at least 6 bytes
    if len(packet) < 6:
        raise DecodeError("Packet is shorter than 6 bytes")

    # -----------------------------------------
    # First 16-bit field
    # -----------------------------------------

    first_two = int.from_bytes(packet[0:2], "big")

    version = (first_two >> 13) & 0b111

    packet_type = (first_two >> 12) & 0b1

    secondary_header_flag = (first_two >> 11) & 0b1

    apid = first_two & 0x07FF

    # -----------------------------------------
    # Second 16-bit field
    # -----------------------------------------

    second_two = int.from_bytes(packet[2:4], "big")

    sequence_flags = (second_two >> 14) & 0b11

    sequence_count = second_two & 0x3FFF

    # -----------------------------------------
    # Data Length
    # -----------------------------------------

    data_length = int.from_bytes(packet[4:6], "big")

    # CCSDS Packet Data Length represents:
    # number of bytes after the primary header - 1

    packet_data_length = data_length + 1

    expected_total_length = 6 + packet_data_length

    if len(packet) < expected_total_length:
        raise DecodeError("Incomplete Space Packet")

    # -----------------------------------------
    # Extract packet data
    # -----------------------------------------

    packet_data = packet[6:expected_total_length]

    return {
        "version": version,
        "type": packet_type,
        "secondary_header": secondary_header_flag,
        "apid": apid,
        "sequence_flags": sequence_flags,
        "sequence_count": sequence_count,
        "data_length": data_length,
        "data": packet_data,
    }


def decode_pus_secondary_header(packet_data: bytes) -> dict:
    """
    Decode the PUS-C secondary header.

    Development format:
        Byte 0 = PUS version
        Byte 1 = Service
        Byte 2 = Subtype
    """

    if len(packet_data) < 3:
        raise DecodeError("PUS secondary header too short")

    pus_version = packet_data[0]

    service = packet_data[1]

    subtype = packet_data[2]

    user_data = packet_data[3:]

    return {
        "pus_version": pus_version,
        "service": service,
        "subtype": subtype,
        "user_data": user_data,
    }
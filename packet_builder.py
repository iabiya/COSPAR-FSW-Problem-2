# Test Space Packet builder


from crc import append_crc


def build_space_packet(
    apid,
    service,
    subtype,
    user_data=b"",
    sequence_count=0
):
    """
    Build a development Space Packet.

    APID       = Application Process Identifier
    Service    = PUS-C service
    Subtype    = PUS-C subtype
    user_data  = command-specific data
    """

    # -----------------------------------------
    # PUS-C secondary header
    # -----------------------------------------

    pus_header = bytes([
        0x20,
        service,
        subtype
    ])

    payload = pus_header + user_data

    # -----------------------------------------
    # Primary header
    # -----------------------------------------

    version = 0
    packet_type = 1
    secondary_header = 1

    first_two = (
        (version << 13)
        | (packet_type << 12)
        | (secondary_header << 11)
        | apid
    )

    sequence_flags = 3

    second_two = (
        (sequence_flags << 14)
        | sequence_count
    )

    # -----------------------------------------
    # Calculate data length
    # -----------------------------------------

    data_length = len(payload) - 1

    # -----------------------------------------
    # Create primary header
    # -----------------------------------------

    primary_header = (
        first_two.to_bytes(2, "big")
        + second_two.to_bytes(2, "big")
        + data_length.to_bytes(2, "big")
    )

    # -----------------------------------------
    # Add payload and CRC
    # -----------------------------------------

    packet_without_crc = primary_header + payload

    packet_with_crc = append_crc(packet_without_crc)

    return packet_with_crc
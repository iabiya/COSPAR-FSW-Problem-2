# CRC-16-CCITT functions


def crc16_ccitt(data: bytes) -> int:
    """
    Calculate CRC-16-CCITT for the given data.
    """

    crc = 0xFFFF

    for byte in data:
        crc ^= byte << 8

        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ 0x1021
            else:
                crc <<= 1

            crc &= 0xFFFF

    return crc


def append_crc(data: bytes) -> bytes:
    """
    Calculate CRC and append it to the data.
    """

    crc = crc16_ccitt(data)

    return data + crc.to_bytes(2, byteorder="big")


def verify_crc(data_with_crc: bytes) -> bool:
    """
    Check whether the CRC attached to the data is correct.
    """

    if len(data_with_crc) < 2:
        return False

    data = data_with_crc[:-2]

    received_crc = int.from_bytes(
        data_with_crc[-2:],
        byteorder="big"
    )

    calculated_crc = crc16_ccitt(data)

    return received_crc == calculated_crc
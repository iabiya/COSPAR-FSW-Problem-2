from crc import append_crc, verify_crc


def test_valid_crc():
    data = b"HELLO"

    packet = append_crc(data)

    assert verify_crc(packet) is True


def test_invalid_crc():
    data = b"HELLO"

    packet = bytearray(append_crc(data))

    # Change one byte to simulate corrupted data
    packet[0] ^= 0xFF

    assert verify_crc(bytes(packet)) is False
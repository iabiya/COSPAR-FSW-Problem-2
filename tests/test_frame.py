from frame import (
    build_frame,
    extract_space_packet,
    FrameError
)

from packet_builder import build_space_packet

from config import START_SEQUENCE

def test_valid_frame():

    packet = build_space_packet(
        apid=17,
        service=17,
        subtype=1,
        user_data=b"PING"
    )

    frame = build_frame(packet)

    extracted_packet = extract_space_packet(frame)

    assert extracted_packet == packet


def test_invalid_start_sequence():

    packet = build_space_packet(
        apid=17,
        service=17,
        subtype=1,
        user_data=b"PING"
    )

    frame = build_frame(packet)

    # Change the first byte
    bad_frame = bytearray(frame)
    bad_frame[0] ^= 0xFF

    try:
        extract_space_packet(bytes(bad_frame))
        assert False
    except FrameError:
        assert True


def test_invalid_tail_sequence():

    packet = build_space_packet(
        apid=17,
        service=17,
        subtype=1,
        user_data=b"PING"
    )

    frame = build_frame(packet)

    # Change the last byte
    bad_frame = bytearray(frame)
    bad_frame[-1] ^= 0xFF

    try:
        extract_space_packet(bytes(bad_frame))
        assert False
    except FrameError:
        assert True


def test_invalid_credentials():

    packet = build_space_packet(
        apid=17,
        service=17,
        subtype=1,
        user_data=b"PING"
    )

    bad_credentials = b"BAD!"

    frame = build_frame(
        packet,
        credentials=bad_credentials
    )

    try:
        extract_space_packet(frame)
        assert False
    except FrameError:
        assert True
        
def test_noisy_stream_frame_detection():
    packet = build_space_packet(
        apid=17,
        service=17,
        subtype=1,
        user_data=b"PING"
    )

    frame = build_frame(packet)

    noisy_stream = (
        b"\xAA\xBB\xCC"
        + frame
        + b"\xDD\xEE\xFF"
    )

    from frame import extract_frame_from_stream

    extracted_frame = extract_frame_from_stream(noisy_stream)

    assert extracted_frame == frame
    
def test_noisy_stream_without_start_sequence():
    packet = build_space_packet(
        apid=17,
        service=17,
        subtype=1,
        user_data=b"PING"
    )

    frame = build_frame(packet)

    noisy_stream = b"\xAA\xBB\xCC" + frame[len(START_SEQUENCE):]

    from frame import extract_frame_from_stream

    try:
        extract_frame_from_stream(noisy_stream)
        assert False
    except FrameError:
        assert True
        
def test_multiple_frames_in_noisy_stream():
    from frame import extract_all_frames_from_stream

    packet1 = build_space_packet(
        apid=17,
        service=17,
        subtype=1,
        user_data=b"PING"
    )

    packet2 = build_space_packet(
        apid=3,
        service=3,
        subtype=1,
        user_data=b"HK"
    )

    frame1 = build_frame(packet1)
    frame2 = build_frame(packet2)

    noisy_stream = (
        b"\xAA\xBB"
        + frame1
        + b"\xCC\xDD"
        + frame2
        + b"\xEE\xFF"
    )

    frames = extract_all_frames_from_stream(noisy_stream)

    assert len(frames) == 2
    assert frames[0] == frame1
    assert frames[1] == frame2
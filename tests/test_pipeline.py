import time

from main import process_frame, process_stream, counters
from packet_builder import build_space_packet
from frame import build_frame


def test_valid_telecommand_pipeline():
    packet = build_space_packet(
        apid=17,
        service=17,
        subtype=1,
        user_data=b"PING"
    )

    frame = build_frame(packet)

    result = process_frame(frame)

    assert result["status"] == "SUCCESS"


def test_invalid_crc_pipeline():
    packet = build_space_packet(
        apid=17,
        service=17,
        subtype=1,
        user_data=b"PING"
    )

    bad_packet = bytearray(packet)

    # Corrupt CRC
    bad_packet[-1] ^= 0xFF

    frame = build_frame(bytes(bad_packet))

    result = process_frame(frame)

    assert result["status"] == "FAILURE"
    
def test_invalid_start_sequence_pipeline():
    packet = build_space_packet(
        apid=17,
        service=17,
        subtype=1,
        user_data=b"PING"
    )

    frame = build_frame(packet)

    # Corrupt the first byte of the Start Sequence
    bad_frame = bytearray(frame)
    bad_frame[0] ^= 0xFF

    result = process_frame(bytes(bad_frame))

    assert result["status"] == "FAILURE"    
    
def test_invalid_tail_sequence_pipeline():
    packet = build_space_packet(
        apid=17,
        service=17,
        subtype=1,
        user_data=b"PING"
    )

    frame = build_frame(packet)

    # Corrupt the last byte of the Tail Sequence
    bad_frame = bytearray(frame)
    bad_frame[-1] ^= 0xFF

    result = process_frame(bytes(bad_frame))

    assert result["status"] == "FAILURE"
    
def test_invalid_credentials_pipeline():
    packet = build_space_packet(
        apid=17,
        service=17,
        subtype=1,
        user_data=b"PING"
    )

    # Build a frame with incorrect credentials
    bad_frame = build_frame(
        packet,
        credentials=b"BAD!"
    )

    result = process_frame(bad_frame)

    assert result["status"] == "FAILURE"
    
def test_telecommand_processing_under_100ms():
    packet = build_space_packet(
        apid=17,
        service=17,
        subtype=1,
        user_data=b"PING"
    )

    frame = build_frame(packet)

    start_time = time.perf_counter()

    result = process_frame(frame)

    end_time = time.perf_counter()

    processing_time = end_time - start_time

    assert result["status"] == "SUCCESS"
    assert processing_time < 0.100
    
def test_noisy_stream_pipeline():
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

    result = process_stream(noisy_stream)

    assert result["status"] == "SUCCESS"
    
def test_housekeeping_pipeline():
    packet = build_space_packet(
        apid=3,
        service=3,
        subtype=1,
        user_data=b""
    )

    frame = build_frame(packet)

    result = process_frame(frame)

    assert result["status"] == "SUCCESS"


def test_memory_pipeline():
    packet = build_space_packet(
        apid=6,
        service=6,
        subtype=2,
        user_data=b""
    )

    frame = build_frame(packet)

    result = process_frame(frame)

    assert result["status"] == "SUCCESS"


def test_function_management_pipeline():
    packet = build_space_packet(
        apid=8,
        service=8,
        subtype=128,
        user_data=b""
    )

    frame = build_frame(packet)

    result = process_frame(frame)

    assert result["status"] == "SUCCESS"


def test_connection_test_pipeline():
    packet = build_space_packet(
        apid=17,
        service=17,
        subtype=1,
        user_data=b"PING"
    )

    frame = build_frame(packet)

    result = process_frame(frame)

    assert result["status"] == "SUCCESS"
    
def test_unsupported_service_pipeline():
    packet = build_space_packet(
        apid=17,
        service=99,
        subtype=99,
        user_data=b""
    )

    frame = build_frame(packet)

    result = process_frame(frame)

    assert result["status"] == "FAILURE"
    
def test_invalid_apid_pipeline():
    packet = build_space_packet(
        apid=100,
        service=17,
        subtype=1,
        user_data=b"PING"
    )

    frame = build_frame(packet)

    result = process_frame(frame)

    assert result["status"] == "FAILURE"
    
def test_invalid_space_packet_version_pipeline():
    packet = bytearray(
        build_space_packet(
            apid=17,
            service=17,
            subtype=1,
            user_data=b"PING"
        )
    )

    # Change Version field from 0 to 1
    packet[0] |= 0x20

    frame = build_frame(bytes(packet))

    result = process_frame(frame)

    assert result["status"] == "FAILURE"


def test_invalid_packet_type_pipeline():
    packet = bytearray(
        build_space_packet(
            apid=17,
            service=17,
            subtype=1,
            user_data=b"PING"
        )
    )

    # Change Packet Type from 1 to 0
    packet[0] &= 0xEF

    frame = build_frame(bytes(packet))

    result = process_frame(frame)

    assert result["status"] == "FAILURE"
    
def test_invalid_pus_version_pipeline():
    packet = bytearray(
        build_space_packet(
            apid=17,
            service=17,
            subtype=1,
            user_data=b"PING"
        )
    )

    # PUS-C version is the first byte of the Space Packet data.
    # Space Packet primary header = 6 bytes.
    packet[6] = 0x10

    # Recalculate CRC after modifying the packet.
    from crc import append_crc

    packet_without_crc = bytes(packet[:-2])
    packet = append_crc(packet_without_crc)

    frame = build_frame(packet)

    result = process_frame(frame)

    assert result["status"] == "FAILURE"


def test_invalid_service_zero_pipeline():
    packet = bytearray(
        build_space_packet(
            apid=17,
            service=17,
            subtype=1,
            user_data=b"PING"
        )
    )

    # Service field is after the PUS version byte.
    packet[7] = 0

    from crc import append_crc

    packet_without_crc = bytes(packet[:-2])
    packet = append_crc(packet_without_crc)

    frame = build_frame(packet)

    result = process_frame(frame)

    assert result["status"] == "FAILURE"


def test_invalid_subtype_zero_pipeline():
    packet = bytearray(
        build_space_packet(
            apid=17,
            service=17,
            subtype=1,
            user_data=b"PING"
        )
    )

    # Subtype field is after PUS version and service.
    packet[8] = 0

    from crc import append_crc

    packet_without_crc = bytes(packet[:-2])
    packet = append_crc(packet_without_crc)

    frame = build_frame(packet)

    result = process_frame(frame)

    assert result["status"] == "FAILURE"
    
def test_multiple_frames_pipeline():
    from main import process_multiple_frames

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
        user_data=b""
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

    results = process_multiple_frames(noisy_stream)

    assert len(results) == 2
    assert results[0]["status"] == "SUCCESS"
    assert results[1]["status"] == "SUCCESS"
    
def test_rejection_counters_for_invalid_crc():
    from counter import Counters

    packet = build_space_packet(
        apid=17,
        service=17,
        subtype=1,
        user_data=b"PING"
    )

    bad_packet = bytearray(packet)
    bad_packet[-1] ^= 0xFF

    frame = build_frame(bytes(bad_packet))

    # Use a fresh counter object indirectly through the existing pipeline.
    before_rejected = counters.telecommands_rejected
    before_packet_rejected = counters.packets_rejected

    result = process_frame(frame)

    assert result["status"] == "FAILURE"

    assert counters.telecommands_rejected == before_rejected + 1
    assert counters.packets_rejected == before_packet_rejected + 1
    
def test_success_counters():
    before_received = counters.telecommands_received
    before_frames = counters.frames_accepted
    before_packets = counters.packets_accepted
    before_tc_rejected = counters.telecommands_rejected
    before_frame_rejected = counters.frames_rejected
    before_packet_rejected = counters.packets_rejected

    packet = build_space_packet(
        apid=17,
        service=17,
        subtype=1,
        user_data=b"PING"
    )

    frame = build_frame(packet)

    result = process_frame(frame)

    assert result["status"] == "SUCCESS"

    assert counters.telecommands_received == before_received + 1
    assert counters.frames_accepted == before_frames + 1
    assert counters.packets_accepted == before_packets + 1

    assert counters.telecommands_rejected == before_tc_rejected
    assert counters.frames_rejected == before_frame_rejected
    assert counters.packets_rejected == before_packet_rejected
    
def test_failure_generates_st_1_8():
    from main import process_frame
    from packet_builder import build_space_packet
    from frame import build_frame
    from verification import handler_failure
    from decoder import decode_space_packet, decode_pus_secondary_header

    packet = build_space_packet(
        apid=17,
        service=99,
        subtype=99,
        user_data=b"FAIL"
    )

    frame = build_frame(packet)

    result = process_frame(frame)

    assert result["status"] == "FAILURE"

    # Generate the failure verification report
    failure_report = handler_failure(
        service=99,
        subtype=99,
        failure_code="Unsupported service/subtype"
    )

    failure_packet = failure_report["packet"]

    # Decode the generated verification packet
    decoded = decode_space_packet(failure_packet)
    pus_header = decode_pus_secondary_header(decoded["data"])

    # Verify ST[1,8]
    assert pus_header["service"] == 1
    assert pus_header["subtype"] == 8
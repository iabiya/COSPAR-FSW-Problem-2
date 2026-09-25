# TC Transfer Frame handling
#
# NOTE:
# The exact Start Sequence, Tail Sequence and
# credential encoding are not specified in the
# supplied problem statement.
# These values come from our development configuration
# in config.py and must be matched to the organizer's
# simulator/interface when those details are provided.


from config import (
    START_SEQUENCE,
    TAIL_SEQUENCE,
    VALID_CREDENTIALS
)


class FrameError(Exception):
    pass


def build_frame(
    space_packet: bytes,
    credentials: bytes = VALID_CREDENTIALS
):
    """
    Build a development TC Transfer Frame.
    """

    return (
        START_SEQUENCE
        + credentials
        + space_packet
        + TAIL_SEQUENCE
    )


def extract_space_packet(frame: bytes):
    """
    Check the frame and extract the Space Packet.
    """

    # Check Start Sequence
    if not frame.startswith(START_SEQUENCE):
        raise FrameError(
            "Start sequence not detected"
        )

    # Check Tail Sequence
    if not frame.endswith(TAIL_SEQUENCE):
        raise FrameError(
            "Tail sequence not detected"
        )

    # -----------------------------------------
    # Extract credentials
    # -----------------------------------------

    credential_start = len(START_SEQUENCE)

    credential_end = (
        credential_start
        + len(VALID_CREDENTIALS)
    )

    credentials = frame[
        credential_start:credential_end
    ]

    # Check credentials
    if credentials != VALID_CREDENTIALS:
        raise FrameError(
            "Invalid frame credentials"
        )

    # -----------------------------------------
    # Extract Space Packet
    # -----------------------------------------

    packet_start = credential_end

    packet_end = (
        len(frame)
        - len(TAIL_SEQUENCE)
    )

    if packet_end <= packet_start:
        raise FrameError(
            "No Space Packet found in frame"
        )

    return frame[
        packet_start:packet_end
    ]
    
def extract_frame_from_stream(stream: bytes):
    """
    Find a valid telecommand frame inside a noisy byte stream.
    """

    start_index = stream.find(START_SEQUENCE)

    if start_index == -1:
        raise FrameError("Start sequence not found in stream")

    tail_start = start_index + len(START_SEQUENCE)

    tail_index = stream.find(TAIL_SEQUENCE, tail_start)

    if tail_index == -1:
        raise FrameError("Tail sequence not found in stream")

    frame_end = tail_index + len(TAIL_SEQUENCE)

    frame = stream[start_index:frame_end]

    return frame
def extract_all_frames_from_stream(stream: bytes):
    """
    Extract all complete telecommand frames from a noisy byte stream.
    """

    frames = []
    search_position = 0

    while True:
        start_index = stream.find(START_SEQUENCE, search_position)

        if start_index == -1:
            break

        tail_start = start_index + len(START_SEQUENCE)

        tail_index = stream.find(TAIL_SEQUENCE, tail_start)

        if tail_index == -1:
            break

        frame_end = tail_index + len(TAIL_SEQUENCE)

        frame = stream[start_index:frame_end]

        frames.append(frame)

        search_position = frame_end

    if not frames:
        raise FrameError("No complete frames found in stream")

    return frames
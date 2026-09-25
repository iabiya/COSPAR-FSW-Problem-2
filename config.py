# Configuration settings for COSPAR FSW Problem 2


# --------------------------------------------------
# Space Packet settings
# --------------------------------------------------

SPACE_PACKET_VERSION = 0

TELECOMMAND_TYPE = 1

PUS_VERSION = 0x20


# --------------------------------------------------
# Development frame settings
# --------------------------------------------------

# These are temporary development values.
# The actual simulator/frame format must be matched
# to the organizer's provided interface when available.

START_SEQUENCE = bytes.fromhex("1ACFFC1D")

TAIL_SEQUENCE = bytes.fromhex("DEADBEEF")

VALID_CREDENTIALS = b"TCOK"


# --------------------------------------------------
# APID Routing Table
# --------------------------------------------------

# APID = Application Process Identifier
# The problem statement requires a configurable
# routing table with at least 32 entries.

ROUTING_TABLE = {
    1: "APP_1",
    2: "APP_2",
    3: "APP_3",
    4: "APP_4",
    5: "APP_5",
    6: "APP_6",
    7: "APP_7",
    8: "APP_8",
    9: "APP_9",
    10: "APP_10",
    11: "APP_11",
    12: "APP_12",
    13: "APP_13",
    14: "APP_14",
    15: "APP_15",
    16: "APP_16",
    17: "APP_17",
    18: "APP_18",
    19: "APP_19",
    20: "APP_20",
    21: "APP_21",
    22: "APP_22",
    23: "APP_23",
    24: "APP_24",
    25: "APP_25",
    26: "APP_26",
    27: "APP_27",
    28: "APP_28",
    29: "APP_29",
    30: "APP_30",
    31: "APP_31",
    32: "APP_32",
}
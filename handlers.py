# Telecommand service handlers


def housekeeping(service, subtype, data, counters):

    print("Housekeeping command executed")

    if subtype == 1:
        return {
            "status": "SUCCESS",
            "message": "Housekeeping report",
            "counters": counters.get_status()
        }

    if subtype == 2:
        return {
            "status": "SUCCESS",
            "message": "Housekeeping command accepted"
        }

    return {
        "status": "FAILURE",
        "message": "Unsupported housekeeping subtype"
    }


def memory_handler(service, subtype, data, counters):

    print("Memory command received")

    if subtype in (2, 5):
        return {
            "status": "SUCCESS",
            "message": "Memory command executed"
        }

    return {
        "status": "FAILURE",
        "message": "Unsupported memory subtype"
    }


def function_management(service, subtype, data, counters):

    print("Function Management command received")

    if subtype == 128:
        return {
            "status": "SUCCESS",
            "message": "Function Management command executed"
        }

    return {
        "status": "FAILURE",
        "message": "Unsupported Function Management subtype"
    }


def connection_test(service, subtype, data, counters):
    print("Connection Test command received")

    if subtype == 1:
        from packet_builder import build_space_packet

        response_packet = build_space_packet(
            apid=17,
            service=17,
            subtype=2,
            user_data=b"PONG"
        )

        return {
            "status": "SUCCESS",
            "message": "Connection Test successful",
            "response_service": 17,
            "response_subtype": 2,
            "response_packet": response_packet
        }

    return {
        "status": "FAILURE",
        "message": "Unsupported Connection Test subtype"
    }


# -----------------------------------------
# Service/Subtype dispatch table
# -----------------------------------------

SERVICE_TABLE = {

    (3, 1): housekeeping,
    (3, 2): housekeeping,

    (6, 2): memory_handler,
    (6, 5): memory_handler,

    (8, 128): function_management,

    (17, 1): connection_test,
}
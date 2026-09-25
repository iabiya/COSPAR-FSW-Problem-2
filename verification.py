from packet_builder import build_space_packet


def generate_verification(
    service,
    subtype,
    stage,
    failure_code=None
):
    user_data = (
        bytes([
            service,
            subtype,
            stage
        ])
    )

    if failure_code is not None:
        failure_bytes = str(failure_code).encode("utf-8")
        user_data += failure_bytes

    packet = build_space_packet(
        apid=17,
        service=1,
        subtype=stage,
        user_data=user_data
    )

    report = {
        "service": 1,
        "subtype": stage,
        "acknowledged_service": service,
        "acknowledged_subtype": subtype,
        "packet": packet
    }

    if failure_code is not None:
        report["failure_code"] = failure_code

    return report


def handler_entry(service, subtype):
    return generate_verification(
        service,
        subtype,
        3
    )


def handler_success(service, subtype):
    return generate_verification(
        service,
        subtype,
        7
    )


def handler_failure(service, subtype, failure_code):
    return generate_verification(
        service,
        subtype,
        8,
        failure_code
    )
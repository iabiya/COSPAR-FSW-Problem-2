from router import route_apid, dispatch, RoutingError
from counter import Counters


def test_valid_apid():

    result = route_apid(17)

    assert result == "APP_17"


def test_another_valid_apid():

    result = route_apid(3)

    assert result == "APP_3"


def test_invalid_apid():

    try:

        route_apid(100)

        assert False

    except RoutingError:

        assert True

def test_unsupported_service_subtype():
    counters = Counters()

    try:
        dispatch(
            service=99,
            subtype=99,
            data=b"",
            counters=counters
        )
        assert False
    except RoutingError:
        assert True     
        
def test_connection_test_response():
    from handlers import connection_test
    from decoder import decode_space_packet, decode_pus_secondary_header
    from validator import validate_space_packet, validate_pus_header

    counters = Counters()

    result = connection_test(
        service=17,
        subtype=1,
        data=b"",
        counters=counters
    )

    assert result["status"] == "SUCCESS"
    assert result["response_service"] == 17
    assert result["response_subtype"] == 2

    packet = result["response_packet"]

    decoded = decode_space_packet(packet)

    assert decoded["apid"] == 17

    validate_space_packet(packet, decoded)

    pus_header = decode_pus_secondary_header(decoded["data"])

    assert pus_header["pus_version"] == 0x20
    assert pus_header["service"] == 17
    assert pus_header["subtype"] == 2   
    
def test_housekeeping_report():
    from handlers import housekeeping

    counters = Counters()

    counters.tc_received()
    counters.frame_accepted()
    counters.packet_accepted()

    result = housekeeping(
        service=3,
        subtype=1,
        data=b"",
        counters=counters
    )

    assert result["status"] == "SUCCESS"
    assert result["message"] == "Housekeeping report"

    report_counters = result["counters"]

    assert report_counters["telecommands_received"] == 1
    assert report_counters["frames_accepted"] == 1
    assert report_counters["packets_accepted"] == 1  
    
def test_housekeeping_dispatch():
    counters = Counters()

    result = dispatch(
        service=3,
        subtype=1,
        data=b"",
        counters=counters
    )

    assert result["status"] == "SUCCESS"
    assert result["message"] == "Housekeeping report"


def test_memory_dispatch():
    counters = Counters()

    result = dispatch(
        service=6,
        subtype=2,
        data=b"",
        counters=counters
    )

    assert result["status"] == "SUCCESS"


def test_function_management_dispatch():
    counters = Counters()

    result = dispatch(
        service=8,
        subtype=128,
        data=b"",
        counters=counters
    )

    assert result["status"] == "SUCCESS"


def test_connection_test_dispatch():
    counters = Counters()

    result = dispatch(
        service=17,
        subtype=1,
        data=b"",
        counters=counters
    )

    assert result["status"] == "SUCCESS"
    assert result["response_service"] == 17
    assert result["response_subtype"] == 2
    assert "response_packet" in result
    
def test_housekeeping_subtype_2_dispatch():
    counters = Counters()

    result = dispatch(
        service=3,
        subtype=2,
        data=b"",
        counters=counters
    )

    assert result["status"] == "SUCCESS"
    assert result["message"] == "Housekeeping command accepted"


def test_memory_subtype_5_dispatch():
    counters = Counters()

    result = dispatch(
        service=6,
        subtype=5,
        data=b"",
        counters=counters
    )

    assert result["status"] == "SUCCESS"
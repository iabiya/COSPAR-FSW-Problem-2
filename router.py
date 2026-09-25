# APID routing and service dispatch


from config import ROUTING_TABLE

from handlers import SERVICE_TABLE


class RoutingError(Exception):
    pass


def route_apid(apid):
    """
    Find the application associated with an APID.
    """

    if apid not in ROUTING_TABLE:
        raise RoutingError(
            f"No application registered for APID {apid}"
        )

    return ROUTING_TABLE[apid]


def dispatch(service, subtype, data, counters):
    """
    Find and execute the correct service/subtype handler.
    """

    key = (service, subtype)

    if key not in SERVICE_TABLE:
        raise RoutingError(
            f"No handler for Service={service}, "
            f"Subtype={subtype}"
        )

    handler = SERVICE_TABLE[key]

    return handler(
        service,
        subtype,
        data,
        counters
    )
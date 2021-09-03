from easytracer.tracer import Span
from easytracer.tracer import Tracer


class HttpHeaders:
    TRACE_ID = "x-tracer-traceid"
    SPAN_ID = "x-tracer-spanid"
    SERVICE_NAME = "x-tracer-servicename"


def inject(span, carrier: dict):
    carrier[HttpHeaders.TRACE_ID] = span.trace_id
    carrier[HttpHeaders.SPAN_ID] = span.span_id
    carrier[HttpHeaders.SERVICE_NAME] = span.service_name


def extract(headers: dict) -> Span:
    # TODO: check if headers exist

    return Span(
        service_name=headers.get(HttpHeaders.SERVICE_NAME),
        name="parsed",
        trace_id=headers.get(HttpHeaders.TRACE_ID),
        span_id=headers.get(HttpHeaders.SPAN_ID)
    )

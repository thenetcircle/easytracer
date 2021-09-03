from easytracer.tracer import Span
from easytracer.tracer import Tracer


def inject(span, carrier: dict):
    carrier["x-tracer-traceid"] = span.trace_id
    carrier["x-tracer-spanid"] = span.span_id
    carrier["x-tracer-servicename"] = span.service_name


def parent_span_from_headers(headers: dict) -> Span:
    # TODO: check if headers exist

    return Span(
        service_name=headers.get("x-tracer-servicename"),
        name="parsed",
        trace_id=headers.get("x-tracer-traceid"),
        span_id=headers.get("x-tracer-spanid")
    )

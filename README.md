# EasyTracer

Simple distributed tracing for Python.

## Using the library

Install the dependency:

```bash
pip install easytracer
```

Initialize the tracer:

```python
from easytracer import Config

config = Config(
    config={
        'sampler': {
            'type': 'const',
            'param': 1,
            'mock': False
        },
        'logging': True,
    },
    service_name="myservice"
)

tracer = config.init_tracer()
```

By setting `mock` to `True`, the tracer will log as usual but won't try to send traces to the agent; useful in testing.

Usage:

```python
data = {
    "some": "event", 
    "id": "a50d3c0c-280d-11ec-9019-782bcb05db41"  # optional, but is searchable from the UI
}

# when this context is over (handle_event has finished), this span will "close" and report 
# the total time spent waiting for processing including any possible remote service 
with tracer.start_span("handle-event", event_id=data["id"]) as span:
    span.log_kv(data)  # optionally attach the event data on the root span
    
    # pass the span for any child-tracing of this event
    handle_event(data, span)
```

To continue tracing for this span in another service, inject trace headers on the request:

```python
import easytracer
import requests

headers = dict()
easytracer.inject(
    span=span,  # the "root" span instance created above
    carrier=headers
)

response = requests.request(
    method=method, url=url, json=data, headers=headers
)
```

In a remote service receiving this request, we can extract the span context and continue reporting "child" spans:

```python
from easytracer import Config
import easytracer

config = Config(
    config={
        'sampler': {
            'type': 'const',
            'param': 1,
        },
        'logging': True
    },
    service_name="child-service-1"
)

tracer = config.initialize_tracer()

# request listener
def post(request):
    # re-created the span from the trace headers
    parent_span = easytracer.extract(request.headers)

    # indicate that this span is a child of the parent span we received
    with tracer.start_span(name="process request", child_of=parent_span) as span:
        # further child spans can be created in a similar way if needed
        process_request(request, span=span)
```

## Running the Agent

The agent should run on the same machine as the service using the easytracer. The agent can either bind to a local 
socket UNIX file, or an INET UDP ip/port. 

The only runtime requirements for the agent is the `requests` library.

Here is an example of listening on _all_ interfaces, port 9999, with debug logging on:

```bash
python backend/agent.py -v -b :9999 -e http://127.0.0.1:6790/v1/collect
```

Use `-h` for more information:

```
usage: agent.py [-h] -b BIND -e ENDPOINT [-v]

easytracer agent

optional arguments:
  -h, --help            show this help message and exit
  -b BIND, --bind BIND  Either ip:port or /path/to/easytracer.sock. Example: :9999 or localhost:1234
  -e ENDPOINT, --endpoint ENDPOINT
                        Collector endpoint URL. Example: http://127.0.0.1:6790/v1/collect
  -v, --verbose         Enable debug logging
```

## Running the Collector

TODO

## Release a new library version

```bash
cd easytracer/
vim setup.py  # edit version number
python setup.py sdist
twine upload dist/easytracer-x.x.x.tar.gz
```

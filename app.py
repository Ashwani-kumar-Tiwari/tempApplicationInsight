from flask import Flask
app = Flask(__name__)
import logging

from opencensus.ext.azure.log_exporter import AzureLogHandler
from opencensus.ext.azure.trace_exporter import AzureExporter
from opencensus.trace import config_integration
from opencensus.trace.samplers import ProbabilitySampler
from opencensus.trace.tracer import Tracer

@app.route("/")
def home():
    config_integration.trace_integrations(['logging'])

    logger = logging.getLogger(__name__)

    handler = AzureLogHandler(connection_string='InstrumentationKey=c08ced98-b263-4db1-8f7d-65c326a40712')
    handler.setFormatter(logging.Formatter('%(traceId)s %(spanId)s %(message)s'))
    logger.addHandler(handler)

    tracer = Tracer(
        exporter=AzureExporter(connection_string='InstrumentationKey=c08ced98-b263-4db1-8f7d-65c326a40712'),
        sampler=ProbabilitySampler(1.0)
    )

    logger.warning('Before the span')
    with tracer.span(name='test'):
        logger.warning('In the span')
    logger.warning('After the span')
    
    return "Hello, this is a sample Python Web App running on Flask Framework!!!"


if __name__ == "__main__":
    app.run()
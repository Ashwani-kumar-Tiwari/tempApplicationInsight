# from flask import Flask
# app = Flask(__name__)
# import logging

# from opencensus.ext.azure.log_exporter import AzureLogHandler
# from opencensus.ext.azure.trace_exporter import AzureExporter
# from opencensus.trace import config_integration
# from opencensus.trace.samplers import ProbabilitySampler
# from opencensus.trace.tracer import Tracer

# @app.route("/")
# def home():
#     config_integration.trace_integrations(['logging'])

#     logger = logging.getLogger(__name__)

#     handler = AzureLogHandler(connection_string='InstrumentationKey=c08ced98-b263-4db1-8f7d-65c326a40712;IngestionEndpoint=https://centralus-2.in.applicationinsights.azure.com/;LiveEndpoint=https://centralus.livediagnostics.monitor.azure.com/')
#     handler.setFormatter(logging.Formatter('%(traceId)s %(spanId)s %(message)s'))
#     logger.addHandler(handler)

#     tracer = Tracer(
#         exporter=AzureExporter(connection_string='InstrumentationKey=c08ced98-b263-4db1-8f7d-65c326a40712;IngestionEndpoint=https://centralus-2.in.applicationinsights.azure.com/;LiveEndpoint=https://centralus.livediagnostics.monitor.azure.com/'),
#         sampler=ProbabilitySampler(1.0)
#     )

#     logger.warning('Before the span')
#     with tracer.span(name='test'):
#         logger.warning('In the span')
#     logger.warning('After the span')

#     return "Hello, this is a sample Python Web App running on Flask Framework!!!"


# if __name__ == "__main__":
#     app.run()

#=================================================================================================================================
import os
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter

exporter = AzureMonitorTraceExporter(connection_string="InstrumentationKey=c08ced98-b263-4db1-8f7d-65c326a40712;IngestionEndpoint=https://centralus-2.in.applicationinsights.azure.com/;LiveEndpoint=https://centralus.livediagnostics.monitor.azure.com/")

trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)
span_processor = BatchSpanProcessor(exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

with tracer.start_as_current_span("hello"):
    print("Hello, World!")
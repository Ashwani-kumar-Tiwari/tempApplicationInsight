import logging

from opencensus.ext.azure.log_exporter import AzureLogHandler

logger = logging.getLogger(__name__)
logger.addHandler(AzureLogHandler(connection_string='InstrumentationKey=c08ced98-b263-4db1-8f7d-65c326a40712'))
logger.warning('Hello, World!')
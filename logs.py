from flask import Flask
app = Flask(__name__)

from datetime import datetime
from opencensus.ext.azure import metrics_exporter
from opencensus.stats import aggregation as aggregation_module
from opencensus.stats import measure as measure_module
from opencensus.stats import stats as stats_module
from opencensus.stats import view as view_module
from opencensus.tags import tag_map as tag_map_module

stats = stats_module.stats
view_manager = stats.view_manager
stats_recorder = stats.stats_recorder

prompt_measure = measure_module.MeasureInt("prompts",
                                           "number of prompts",
                                           "prompts")
prompt_view = view_module.View("prompt view",
                               "number of prompts",
                               [],
                               prompt_measure,
                               aggregation_module.CountAggregation())
view_manager.register_view(prompt_view)
mmap = stats_recorder.new_measurement_map()
tmap = tag_map_module.TagMap()

# TODO: replace the all-zero GUID with your instrumentation key.
exporter = metrics_exporter.new_metrics_exporter(
    connection_string='InstrumentationKey=c08ced98-b263-4db1-8f7d-65c326a40712')
# You can also instantiate the exporter directly if you have the environment variable
# `APPLICATIONINSIGHTS_CONNECTION_STRING` configured
# exporter = metrics_exporter.new_metrics_exporter()

view_manager.register_exporter(exporter)

def prompt():
    mmap.measure_int_put(prompt_measure, 1)
    mmap.record(tmap)
    metrics = list(mmap.measure_to_view_map.get_metrics(datetime.utcnow()))
    print(metrics[0].time_series[0].points[0])

def main():
    while True:
        prompt()

if __name__ == "__main__":
    main()
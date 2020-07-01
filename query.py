from google.cloud import monitoring_v3
from google.cloud.monitoring_v3 import enums, query
from google.protobuf.timestamp_pb2 import Timestamp
import datetime
import os
import json

def get_ts_json(d=1,h=0,m=0):
    """Saves the cloud monitoring time series data, from the present time 
    until days=d,hours=h,minutes=m from the present. The data is retrieved 
    as a dataframe and saved to a file."""

    client = monitoring_v3.MetricServiceClient()
    project = os.environ["project"]
    metric = "compute.googleapis.com/instance/cpu/usage_time"
    query_result = query.Query(client,project,metric,days=d,hours=h,minutes=m)
    dataframe = query_result.as_dataframe()
    dataframe_json = dataframe.to_json(date_format="iso")

    file_write("data_query.json", dataframe_json)

def file_write(file_name,data):
    """Writes data to the file file_name."""
    f = open(file_name, "w")
    f.write(data)
    f.close()

def current_time():
    """Creates a timestamp for the current time."""
    timestamp = Timestamp()
    timestamp.GetCurrentTime()
    return timestamp

def format_time(y, m, d):
    """From the given year=y, month=m, day=d creates a timestamp."""
    timestamp = Timestamp()
    date = datetime.datetime(y, m, d)
    timestamp.FromDatetime(date)
    return timestamp

def get_ts_iterable(y=2020, m=6, d=30):
    """Saves the cloud monitoring time series data from the present until the 
    date year=y,month=m,day=d. The data is retireved as an iterable and saved 
    to a file."""
    client = monitoring_v3.MetricServiceClient()
    project_name = client.project_path(os.environ["project"])

    ts_filter = 'metric.type="compute.googleapis.com/instance/cpu/usage_time"'
    start_time = format_time(y,m,d)
    end_time = current_time()
    interval = {"start_time": start_time, "end_time": end_time}
    
    view = enums.ListTimeSeriesRequest.TimeSeriesView.FULL
    time_series_result = list(client.list_time_series(project_name, ts_filter, 
                            interval, view))
    
    file_write("data_list.txt", str(time_series_result))
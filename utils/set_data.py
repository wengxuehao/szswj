# __author__ : htzs
# __time__   : 19-5-6 上午9:03


import json

from apps.warnlist.models import StreamId


def read_data(stream_id):
    stream_id = StreamId.objects.get(stream_id=stream_id)
    map_id = stream_id.resource_id
    name = map_id[-2:]
    file_name = '/root/adminy/json_data/IPC{0}.json'.format(name)
    with open(file_name, 'r') as load_file:
        load_file = json.load(load_file)
        return load_file['config']

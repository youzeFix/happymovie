import datetime

def datetime_to_json(obj:datetime):
    return obj.strftime('%Y-%m-%d %H:%M:%S')
    # return int(obj.timestamp())




import sys
import requests
import pandas as pd

class DataPull(object):
    """data object used to request data from api"""
    def __init__(self, show=None, sumlevel=None, required=None, where=None, limit=None, order=None, sort=None, attr=None):
        attrs = locals().iteritems()
        param = []
        for key, val in attrs:
            if key != 'self' and val:
                if key != 'required':
                    param.append(key + '=' + val)
                else:
                    param.append(key + '=' + ','.join(val))
        self.csv_string = 'http://api.datausa.io/api/csv/?' + '&'.join(param)
        # print self.csv_string
        self.json_string = 'http://api.datausa.io/api/?' + '&'.join(param)
        # print self.json_string


        # self.show = show
        # self.required = ','.join(required)
        # self.sumlevel = sumlevel
        # self.csv_string = 'http://api.datausa.io/api/csv/?show={0}&required={1}&sumlevel={2}'.format(self.show, self.required, self.sumlevel)
        # self.json_string = 'http://api.datausa.io/api/?show={0}&required={1}&sumlevel={2}'.format(self.show, self.required, self.sumlevel)
        # print self.csv_string

    def to_pandas(self):
        csv_r = requests.get(self.csv_string)
        if sys.version_info[0] < 3:
            from StringIO import StringIO
        else:
            from io import StringIO
        data = StringIO(csv_r.text)
        return pd.read_csv(data)

    def to_csv(self, filepath):
        csv_r = requests.get(self.csv_string)
        with open(filepath, 'w+') as f:
            f.write(csv_r.text)

    def to_apijson(self, filepath):
        json_r = requests.get(self.json_string)
        with open(filepath, 'w+') as f:
            f.write(json_r.text)


if __name__ == '__main__':
    dp = DataPull(show='geo', required=['year', 'geo', 'income'], sumlevel='state')
    df = dp.to_pandas()
    dp.to_csv('test.csv')
    dp.to_apijson('test.json')
    print df.dtypes


# 'http://api.datausa.io/api/csv/?show=geo&required=year,geo,income&sumlevel=state')

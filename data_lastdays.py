from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint
import requests
from urllib.request import urlopen
import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

apikey='eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJtaWdnYXJjaWE5MEBnbWFpbC5jb20iLCJqdGkiOiIwZWE4ZjI2YS02MGNiLTQzMDktOTE0OC0wMTU1ZDY3YTExYjgiLCJpc3MiOiJBRU1FVCIsImlhdCI6MTU4NTg3MDkwOSwidXNlcklkIjoiMGVhOGYyNmEtNjBjYi00MzA5LTkxNDgtMDE1NWQ2N2ExMWI4Iiwicm9sZSI6IiJ9.44EAKSmbmHyPLJIoLCLXeFbpV-CtOt-KZajfvvDNN44'
t = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

fecha_ini_str = '2022-01-01T00:00:00UTC'
# fecha_fin_str = '2022-02-07T00:00:00UTC'
fecha_fin_str = t[6:10]+'-'+t[0:2]+'-'+t[3:5]+'T00:00:00UTC'

# idema = '3195'
# idema = '3194U'
idema = '2422'


# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['api_key'] = apikey

api_instance = swagger_client.ValoresClimatologicosApi(swagger_client.ApiClient(configuration))

try:
    api_response = api_instance.climatologas_diarias_(fecha_ini_str, fecha_fin_str, idema)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ValoresClimatologicosApi->climatologas_diarias_: %s\n" % e)

r = requests.get(api_response.to_dict()['datos'])
data = json.dumps(r.json())
r.close()

df = pd.read_json(data)
df.fecha = pd.to_datetime(df['fecha'], format='%Y-%m-%d')

# df = df.apply(pd.to_numeric, errors='ignore')
# df['column name'] = df['column name'].str.replace('old character','new character')
# df.tmax = df.tmax.str.replace(",",".").apply(pd.to_numeric)
# df.tmin = df.tmin.str.replace(",",".").apply(pd.to_numeric)
# df.tmed = df.tmed.str.replace(",",".").apply(pd.to_numeric)
# df.presMax = df.presMax.str.replace(",",".").apply(pd.to_numeric)
# df.presMin = df.presMin.str.replace(",",".").apply(pd.to_numeric)

for col in df.columns.to_list():
    if type(df[col][0]) == str: 
        df[col] = df[col].str.replace(",",".").apply(pd.to_numeric, errors='ignore')

print(df.head(20))
# df.info()

plt.rcParams['figure.dpi'] = 100
plt.rcParams['figure.figsize'] = (10.0, 5.0)
df.plot.line(x='fecha',y=['tmax','tmin','tmed'],grid=True, ylabel='Temperature',xlabel='', subplots=False)
plt.show()
df.plot.line(x='fecha',y=['presMax','presMin'],grid=True, ylabel='Pressure',xlabel='', subplots=False)
plt.show()


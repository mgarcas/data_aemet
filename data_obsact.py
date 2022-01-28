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

fecha_ini_str = '2022-01-01T00:00:00UTC' # str | Fecha Inicial (AAAA-MM-DDTHH:MM:SSUTC)
fecha_fin_str = t[6:10]+'-'+t[0:2]+'-'+t[3:5]+'T00:00:00UTC' # str | Fecha Final (AAAA-MM-DDTHH:MM:SSUTC)
# idema = '3195' # Madrid Retiro
# idema = '3194U' # Madrid Ciudad Univesitaria
idema = '3191E' # Colmenar Viejo
print('fecha_fin_str: ', fecha_fin_str)

# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['api_key'] = apikey

# :::::::::: OBSERVACIÓN ACTUAL ::::::::::::::::::    

# create an instance of the API class
api_instance_obsact = swagger_client.ObservacionConvencionalApi(swagger_client.ApiClient(configuration))
fecha_ini_valclim = '2022-01-17T00:00:00UTC' # str | Fecha Inicial (AAAA-MM-DDTHH:MM:SSUTC)
fecha_fin_valclim = '2022-01-17T00:00:00UTC' # str | Fecha Final (AAAA-MM-DDTHH:MM:SSUTC)
idema_obsact = idema #'3194U' # str | Indicativo climatológico de la EMA. Puede introducir varios indicativos separados por comas (,)
date_obsact = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")[0:5].replace('/','')

try:
    # Datos de observación. Tiempo actual.
    api_response_obsact = api_instance_obsact.datos_de_observacin__tiempo_actual_1(idema_obsact)
    pprint(api_response_obsact)
except ApiException as e:
    print("Exception when calling ObservacionConvencionalApi->datos_de_observacin__tiempo_actual_1: %s\n" % e)
    
r_obsact = requests.get(api_response_obsact.to_dict()['datos'])
df_data_obsact = pd.read_json(json.dumps(r_obsact.json()))
meta_obsact = (requests.get(api_response_obsact.to_dict()['metadatos'])).json()

with open('./data_obsact_{}.csv'.format(date_obsact),'w', encoding='utf-8') as f:
    f.write(r_obsact.text)
    f.close()

print(df_data_obsact)
# pprint(meta)

# data_radiation = r.text[31:]
# pprint(data_radiation)
# type(data_radiation)
# pprint(data_radiation[0:20])
# r.close()
# type(data_radiation)

df_data_obsact.fint = pd.to_datetime(df_data_obsact['fint'],format='%Y-%m-%d')
# df['fecha'], format='%Y-%m-%d'

day = df_data_obsact.fint[0].day #.split('-')[2][0:2]
print(day)

df_data_obsact.plot(x='fint', y=['ta', 'tpr', 'pres'], kind='line', grid=True,
                    title='Day {}'.format(day), xlabel='Hour', secondary_y='pres')

plt.show()
print(df_data_obsact)
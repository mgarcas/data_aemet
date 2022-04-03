import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint
import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime


# ::::::::::::::::::: Read data from cvs and plot ::::::::::::::::::

def plot_radiation(m_d):
    '''
    returns a graphic of solar radiation UV [J/m2] at Madrid Ciudad Universitaria \n
    m_d -> month and day, like mmdd
    '''
    df_radiation = pd.DataFrame()
    try:
        df_radiation = pd.read_csv('./data_radiation_{}.csv'.format(m_d),sep=';',header=2)
    except FileNotFoundError:
        raise FileNotFoundError
    
    ind_madrid = df_radiation[df_radiation['Estación']=='Madrid, Ciudad Universitaria'].index.to_list()[0]

    columns = df_radiation.columns.to_list()
    index_tipo = columns.index('Tipo.3')
    index_suma = columns.index('SUMA.3')+1


    sums_radiation=df_radiation[['Estación','Indicativo','Tipo','SUMA','Tipo.1','SUMA.1','Tipo.2','SUMA.2','Tipo.3','SUMA.3','Tipo.4','SUMA.4']]
    print(sums_radiation)
    madrid_radiation=df_radiation[df_radiation['Estación']=='Madrid, Ciudad Universitaria']


    old_index_UVB = madrid_radiation.transpose()[index_tipo:index_suma].index.to_list()
    new_index_UVB = list()
    new_index_UVB.append(old_index_UVB[0])
    for i in range(1,len(old_index_UVB)-1):
        new_index_UVB.append(str(int(old_index_UVB[i].split('.')[0],10)))
    new_index_UVB.append(old_index_UVB[-1])

    mad_rad_UVB = madrid_radiation.transpose()[index_tipo:index_suma]

    mad_rad_UVB.index = new_index_UVB
    mad_rad_UVB = mad_rad_UVB.iloc[1:,:]
    mad_rad_UVB.reset_index(inplace=True)

    mad_rad_UVB.rename(columns={'index':'hour',15:'UVB'},inplace=True)

    mad_rad_UVB.drop(mad_rad_UVB.tail(1).index,inplace=True)
    mad_rad_UVB.plot(x='hour',y='UVB',kind='line',ylabel='UVB (J/m2)',title=day, grid=True)

    print('\n')
    print('Day: ', day)
    print('Data plotted: ', 'Radiación Ultravioleta Eritemática')
    print(mad_rad_UVB)
    plt.savefig('./plot_radiation{}.png'.format(m_d))
    plt.show()

# _=_=_=_=_=_=_= END OF FUNCTIONS =_=_=_=_=_=_=_



apikey='eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJtaWdnYXJjaWE5MEBnbWFpbC5jb20iLCJqdGkiOiIwZWE4ZjI2YS02MGNiLTQzMDktOTE0OC0wMTU1ZDY3YTExYjgiLCJpc3MiOiJBRU1FVCIsImlhdCI6MTU4NTg3MDkwOSwidXNlcklkIjoiMGVhOGYyNmEtNjBjYi00MzA5LTkxNDgtMDE1NWQ2N2ExMWI4Iiwicm9sZSI6IiJ9.44EAKSmbmHyPLJIoLCLXeFbpV-CtOt-KZajfvvDNN44'
t = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

fecha_ini_str = '2022-01-01T00:00:00UTC' # str | Fecha Inicial (AAAA-MM-DDTHH:MM:SSUTC)
fecha_fin_str = t[6:10]+'-'+t[0:2]+'-'+t[3:5]+'T00:00:00UTC' # str | Fecha Final (AAAA-MM-DDTHH:MM:SSUTC)
idema = '3195' # Madrid Retiro
# idema = '3194U' # Madrid Ciudad Univesitaria
print('fecha_fin_str: ', fecha_fin_str)

# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['api_key'] = apikey


# ::::::::::::::::::: Get data from Api ::::::::::::::::::

api_instance_radiacion = swagger_client.RedesEspecialesApi(swagger_client.ApiClient(configuration))

try:
    # Datos de radiación global, directa o difusa. Tiempo actual.
    api_response_radiation = api_instance_radiacion.datos_de_radiacin_global_directa_o_difusa__tiempo_actual_()
    pprint(api_response_radiation)
except ApiException as e:
    print("Exception when calling RedesEspecialesApi->datos_de_radiacin_global_directa_o_difusa__tiempo_actual_: %s\n" % e)

r = requests.get(api_response_radiation.to_dict()['datos'])
meta = (requests.get(api_response_radiation.to_dict()['metadatos'])).json()
day = r.text.split('\n')[1].rstrip('\r').strip('"')
month_day = day.split('-')[1]+day.split('-')[0]

print('\ndate: \n ',day)

with open('./data_radiation_{}.csv'.format(month_day),'w', encoding='utf-8') as f:
    f.write(r.text)
    f.close()



m_d = input('type month and day (mmdd): ')
if m_d.strip() != '':
    month_day = m_d

plot_radiation(month_day)

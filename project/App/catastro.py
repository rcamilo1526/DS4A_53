#streamlit
import streamlit as st
import streamlit.components.v1 as components
from streamlit_folium import folium_static
import markdown

#database connection
import psycopg2
# import sqlalchemy
#data
import numpy as np
import pandas as pd
import geopandas as gpd
from geopandas import GeoDataFrame
import io
import branca
from typing import List, Optional
import json

#plots n maps
import folium
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import math

import time
#secrets
import config_db
##############
import warnings

warnings.filterwarnings("ignore")

# matplotlib.use("TkAgg")
matplotlib.use("Agg")
COLOR = "black"
BACKGROUND_COLOR = "#fff"
st.set_option('deprecation.showPyplotGlobalUse', False)
cols_traduccion = {'oft_codigo': ['Id Oferta', 'Id Oferta'],
                   'All': ['All', 'All'],
                   'lotcodigo': ['Codigo Lote', 'Lot Code'],
                   'nombre_barrio': ['Nombre Barrio', 'Name Neighbor'],
                   'oft_tipo_inmueble': ['Tipo Inmueble', 'Type Property'],
                   'oft_tipo_norma_juridica': ['Tipo Norma Jurídica', 'Type Legal Standard'],
                   'oic_area_terreno': ['Área Terreno', 'Land Area'],
                   'oic_area_construccion': ['Área Construcción', 'Construction Area'],
                   'oic_valor_adm': ['Valor Administración', 'Administration Value'],
                   'oic_valor_anexos': ['Valor Anexos', 'Value Annexes'],
                   'oia_tiene_ascensor': ['Tiene Ascensor', 'Has Elevator'],
                   'oia_cant_garajes': ['Cantidad Garajes', 'Number of Garages'],
                   'vfventa2020': ['Valor Final Venta 2020', 'Final Sale Value 2020'],
                   'codigo_con': ['Codigo Con', 'Code With'],
                   'codigo_res': ['Codigo Res', 'Code Res'],
                   'x': ['Ubicación X', 'Location X'],
                   'y': ['Ubicación Y', 'Location Y'],
                   'd_park': ['Parque Distancia', 'Park Distance'],
                   'd_highway': ['Autopista Distancia', 'Highway Distance'],
                   'd_bikeway': ['Cicloruta Distancia', 'Cycle Path Distance'],
                   'd_ssf': ['Cancha de Futbol Distancia', 'Soccer Field Distance'],
                   'd_mus': ['Museo Distancia', 'Museum Distance'],
                   'd_lib': ['Librería Distancia', 'Library Distance'],
                   'd_sitp': ['SITP Estación Distancia', 'SITP Station Distance'],
                   'd_tm': ['Transmilenio Estación Distancia', 'Transmilenio Station Distance'],
                   'd_p_tm': ['Portal TM Distancia', 'Portal TM Distance'],
                   'd_gy': ['Gym Distancia', 'Gym Distance'],
                   'd_ies': ['Inst_educación Superior Distancia', 'Higher Education Distance'],
                   'd_bom': ['Bomberos Distancia', 'Firefighters Distance'],
                   'd_col': ['Colegio Distancia', 'School Distance'],
                   'd_ips': ['IPS Distancia', 'IPS Distance'],
                   'dm_bikeway': ['Cicloruta Distancia_M', 'Cycle Path Distancia_M'],
                   'dm_bom': ['Bomberos Distancia_M', 'Firefighters Distance_M'],
                   'dm_col': ['Colegio Distancia_M', 'School Distance_M'],
                   'dm_gy': ['Gym Distancia_M', 'Gym Distance_M'],
                   'dm_highway': ['Autopista Distancia_M', 'Highway Distance_M'],
                   'dm_ies': ['Inst_educación Superior Distancia_M', 'High Education Distancia_M'],
                   'dm_ips': ['IPS Distancia_M', 'IPS Distance_M'],
                   'dm_lib': ['Librería Distancia_M', 'Library Distance_M'],
                   'dm_mus': ['Museo Distancia_M', 'Museum Distance_M'],
                   'dm_park': ['Parque Distancia_M', 'Park Distance_M'],
                   'dm_p_tm': ['Portal TM Distancia_M', 'Portal TM Distancia_M'],
                   'dm_sitp': ['SITP Estación Distancia_M', 'SITP Station Distance_M'],
                   'dm_ssf': ['Cancha de Futbol Distancia_M', 'Soccer Field Distance _M'],
                   'dm_tm': ['Transmilenio Estación Distancia_M', 'Transmilenio Station Distance_M'],
                   'loccodigo': ['Localidad Código', 'City Code'],
                   'locnombre': ['Localidad Nombre', 'City Name'],
                   'z': ['Elevación', 'Elevation'],

                   'suelo': ['Suelo Categoría', 'Soil Category'],
                   'actividad': ['Actividad Categoría', 'Activity Category'],
                   'tratamiento_urb': ['Tratamiento urbano Categoría', 'Urban treatment Category'],
                   'topografia': ['Topografía Categoría', 'Topography Category'],
                   'serpub': ['Servicio publicos', 'Public service'],
                   'serpub_tipo': ['Tipo servicio publico', 'Public service type'],
                   'serpub_especif': ['Especificidad de servicio publico', 'Specificity of public service'],
                   'via': ['Vía', 'Via'],
                   'clase_via': ['Clase de la Vía', 'Class of the Way'],
                   'estado_via': ['Estado de la Vía', 'State of the Road'],
                   'influencia_via': ['Influencia de la Vía', 'Influence of the Way'],
                   'actividad_economica': ['Actividad económica Categoría', 'Economic activity Category'],
                   'actividad_economica_tipo': ['Tipo Actividad económica', 'Type Economic activity'],
                   'tipo_segun_actividad': ['Tipo según Actividad', 'Type according to Activity'],
                   'manzana_id': ['ID Manzana', 'Block ID'],

                   'avaluo_com': ['Avalúo Comercial', 'Commercial Appraisal'],
                   'avaluo_cat': ['Avalúo Catastro', 'Property valuation'],
                   'log_vfventa2020': ['Log Valor Final Venta 2020', 'Log Final Value Sell 2020'],
                   'estrato': ['Estrato', 'Stratum'],
                   'prevetustz': ['Vetustez', 'Antiquity']}
cols_traduccion_geo = {'gid': ['ID', 'ID'],
                       'scacodigo': ['Code', 'Code'],
                       'scanombre': ['Name', 'Name'],
                       'area_terreno': ['Área Terreno', 'Land Area'],
                       'area_construccion': ['Área Construcción', 'Construction Area'],
                       'cantidad_garajes': ['Cantidad Garajes', 'Number of Garages'],
                       'valor_venta_2020': ['Valor Final Venta 2020', 'Final Sale Value 2020'],
                       'x': ['Ubicación X', 'Location X'],
                       'y': ['Ubicación Y', 'Location Y'],
                       'd_park': ['Parque Distancia', 'Park Distance'],
                       'd_highway': ['Autopista Distancia', 'Highway Distance'],
                       'd_bikeway': ['Cicloruta Distancia', 'Cycle Path Distance'],
                       'd_ssf': ['Cancha de Futbol Distancia', 'Soccer Field Distance'],
                       'd_mus': ['Museo Distancia', 'Museum Distance'],
                       'd_lib': ['Librería Distancia', 'Library Distance'],
                       'd_sitp': ['SITP Estación Distancia', 'SITP Station Distance'],
                       'd_tm': ['Transmilenio Estación Distancia', 'Transmilenio Station Distance'],
                       'd_p_tm': ['Portal TM Distancia', 'Portal TM Distance'],
                       'd_gy': ['Gym Distancia', 'Gym Distance'],
                       'd_ies': ['Inst_educación Superior Distancia', 'Higher Education Distance'],
                       'd_bom': ['Bomberos Distancia', 'Firefighters Distance'],
                       'd_col': ['Colegio Distancia', 'School Distance'],
                       'd_ips': ['IPS Distancia', 'IPS Distance'],
                       'dm_bikeway': ['Cicloruta Distancia_M', 'Cycle Path Distancia_M'],
                       'dm_bom': ['Bomberos Distancia_M', 'Firefighters Distance_M'],
                       'dm_col': ['Colegio Distancia_M', 'School Distance_M'],
                       'dm_gy': ['Gym Distancia_M', 'Gym Distance_M'],
                       'dm_highway': ['Autopista Distancia_M', 'Highway Distance_M'],
                       'dm_ies': ['Inst_educación Superior Distancia_M', 'High Education Distancia_M'],
                       'dm_ips': ['IPS Distancia_M', 'IPS Distance_M'],
                       'dm_lib': ['Librería Distancia_M', 'Library Distance_M'],
                       'dm_mus': ['Museo Distancia_M', 'Museum Distance_M'],
                       'dm_park': ['Parque Distancia_M', 'Park Distance_M'],
                       'dm_p_tm': ['Portal TM Distancia_M', 'Portal TM Distancia_M'],
                       'dm_sitp': ['SITP Estación Distancia_M', 'SITP Station Distance_M'],
                       'dm_ssf': ['Cancha de Futbol Distancia_M', 'Soccer Field Distance _M'],
                       'dm_tm': ['Transmilenio Estación Distancia_M', 'Transmilenio Station Distance_M'],
                       'z': ['Elevación', 'Elevation'],
                       'avaluo_comercial': ['Avalúo Comercial', 'Commercial Appraisal'],
                       'avaluo_catastral': ['Avalúo Catastro', 'Property valuation'],
                       'log_valor_venta_2020': ['Log Valor Final Venta 2020', 'Log Final Value Sell 2020'],
                       'zona_homogenea_fisica': ['Zona Física Homogenea', 'Homogenous Physical Zone'],
                       'tipo_inmueble': ['Tipo Inmueble', 'Type Property'],
                       'tipo_norma': ['Tipo Norma Jurídica', 'Type Legal Standard'],
                       'tiene_ascensor': ['Tiene Ascensor', 'Has Elevator'],
                       'loccodigo': ['Localidad Código', 'City Code'],
                       'suelo': ['Suelo Categoría', 'Soil Category'],
                       'actividad': ['Actividad Categoría', 'Activity Category'],
                       'tratamient': ['Tratamiento', 'Treatment'],
                       'topografia': ['Topografía Categoría', 'Topography Category'],
                       'serpub': ['Servicio publicos', 'Public service'],
                       'serpub_tip': ['serpub_tip', 'serpub_tip'],
                       'serpub_esp': ['serpub_esp', 'serpub_esp'],
                       'via': ['Vía', 'Via'],
                       'clase_via': ['Clase de la Vía', 'Class of the Way'],
                       'estado_via': ['Estado de la Vía', 'State of the Road'],
                       'influencia_via': ['Influencia de la Vía', 'Influence of the Way'],
                       'actividad_economica': ['Actividad económica Categoría', 'Economic activity Category'],
                       'actividad_economica_tipo': ['Tipo Actividad económica', 'Type Economic activity'],
                       'tipo_segun_actividad': ['Tipo según Actividad', 'Type according to Activity'],
                       'estrato': ['Estrato', 'Stratum'],
                       'geom': ['Geometría', 'Geometry']}

zhfg = {
    'zona_homogenea_fisica': ['Zona Física Homogenea', 'Homogenous Physical Zone'],
                       'tipo_inmueble': ['Tipo Inmueble', 'Type Property'],
                       'tipo_norma': ['Tipo Norma Jurídica', 'Type Legal Standard'],
                       'tiene_ascensor': ['Tiene Ascensor', 'Has Elevator'],
                       'loccodigo': ['Localidad Código', 'City Code'],
                       'suelo': ['Suelo Categoría', 'Soil Category'],
                       'actividad': ['Actividad Categoría', 'Activity Category'],
                       'tratamient': ['Tratamiento', 'Treatment'],
                       'topografia': ['Topografía Categoría', 'Topography Category'],
                       'serpub': ['Servicio publicos', 'Public service'],
                       'serpub_tip': ['serpub_tip', 'serpub_tip'],
                       'serpub_esp': ['serpub_esp', 'serpub_esp'],
                       'via': ['Vía', 'Via'],
                       'clase_via': ['Clase de la Vía', 'Class of the Way'],
                       'estado_via': ['Estado de la Vía', 'State of the Road'],
                       'influencia_via': ['Influencia de la Vía', 'Influence of the Way'],
                       'actividad_economica': ['Actividad económica Categoría', 'Economic activity Category'],
                       'actividad_economica_tipo': ['Tipo Actividad económica', 'Type Economic activity'],
                       'tipo_segun_actividad': ['Tipo según Actividad', 'Type according to Activity'],
    
}
def main(table_data, poly_data):
    # style
    st.markdown("""
    <style>
    body {

    }
    .sidebar .sidebar-content {
     background: rgb(244,241,241);
background: linear-gradient(rgba(25,25,112,1) 100%);
        color: black;
    }
    </style>
        """, unsafe_allow_html=True)
    # /style
    # principal
    ttitle = st.title("Appraisal Model - Catastro Distrital")
    st.markdown("""
        ## Team 53 - Correlation One
        """)
    # /principal
    # sidebar
    st.sidebar.title("Unidad Administrativa Especial de Catastro Distrital ")
    st.sidebar.image('img/logon.png')
    selection = st.sidebar.selectbox("Select from the Dropdown", ("Home","EDA", "ESDA", "Models"))
    st.sidebar.header("Team 53")
    st.sidebar.markdown("""
    - Laura Palacios R.
    - [Raúl Camilo Martín] (https://www.linkedin.com/in/ra%C3%BAl-camilo-mart%C3%ADn-bernal/)
    - [Juan Manuel Jaramillo](https://www.linkedin.com/in/juanmjriesgos)
    - [Bernardo Macías] (https://www.linkedin.com/in/bernardo-j-macias/)
    - [Camilo Montenegro] (https://linkedin.com/in/montenegro456)
    - David Pardey
    - Daniel Santiago Lopez
    """)
    st.sidebar.markdown(
        """
    - [Repository] (https://github.com/rcamilo1526/DS4A_53)

    """
    )


    if selection == "EDA":
        eda(table_data)
    elif selection == "ESDA":
        esda(poly_data)
    elif selection == "Home":
        home_page()
    else:
        models()

def home_page():
    st.title("Home")
    st.markdown("""

    ### **Project : ** Automated valuation models (AVMs) properties sales for obtain the cadastral values
    ### **Entity : ** Unidad Administrativa Especial de Catastro Distrital

    ## **Guide**

     In this application you can see an overview of the process that was made for the project of sales prices of AVM houses by cadastral value, carried out for the "Unidad Administrativa Especial de Catastro Distrital", the project consists of the realization and comparison of machine learning models to obtain the sales value of different commercial offers for diferents types of properties in the city of Bogotá D.C. Colombia.

    In the application there are three sections which can be accessed from the selector on the left

   
    - **EDA:** Exploratory Data Analysis. 

    *"Exploratory Data Analysis refers to the critical process of performing initial investigations on data so as to discover patterns,to spot anomalies,to test hypothesis and to check assumptions with the help of summary statistics and graphical representations.."* 
    [What is Exploratory Data Analysis?, Prasad Patil, 2018][1]

    [1]: https://towardsdatascience.com/exploratory-data-analysis-8fc1cb20fd15
    - **ESDA:** Exploratory Spatial Data Analysis

    *"Exploratory spatial data analysis (ESDA) is the extension of exploratory data analysis (EDA) to
    the problem of detecting spatial properties of data sets where, for each attribute value, there is a
    locational datum. This locational datum references the point or the area to which the attribute
    refers."*
    [Exploratory Spatial Data Analysis, R. Haining  S. Wise  J. Ma, 2002][2]

    [2]: https://rss.onlinelibrary.wiley.com/doi/abs/10.1111/1467-9884.00147#:~:text=Introduction,to%20which%20the%20attribute%20refers.
    - **Models:** Summary and results of the models that we obtain in the project
    """)

# @st.cache(suppress_st_warning=True)
def get_data_db():
    data = pd.read_parquet('https://ds4aavaluos.s3.us-east-2.amazonaws.com/ofertas_10000.parquet.gzip')

    # for cd in cat_data:
    #     try:
    #         data[cd] = data[cd].astype('category')
    return data

@st.cache(suppress_st_warning=True)
def get_pol_db():
    con = psycopg2.connect(database=config_db.database,user=config_db.user,password=config_db.password,host=config_db.host)
    sdf = gpd.GeoDataFrame.from_postgis("select * from neighborhood", con, geom_col='geom')
    time.sleep(3)  
    return sdf



#EDA
# @st.cache(suppress_st_warning=True)
def eda(data):

    st.markdown("""
    ### Exploratory data analysis
        """)
    st.markdown("""
        ### In this section you can explore the available data used along the project
        """)
    # print('init1')
    # con = psycopg2.connect(database=config_db.database, user=config_db.user, password=config_db.password,
    #                       host=config_db.host)
    # print('init2')
    # data = pd.read_sql("select * from datos limit 50000", con)

    # print('init')
    
    
    real_length = len(data.index)
    texto = ['Showing a resample of', str(real_length), 'rows']
    st.markdown(' '.join(texto))
    # print(data.head())
    ##data.reset_index(drop=False,inplace=True)
    # vars = ['All']
    # vars += (list(data.columns))
    cols_english = []
    for val in cols_traduccion.values():
        cols_english.append(val[1])

    filter_var = st.selectbox(
        "Select a variable to filter by, otherwise choose the option 'All' to use all the data ",
        cols_english, 1)
    # filter_var = st.radio(
    #    "Choose ONE variable to filter by", ['nombre_barrio', 'oft_tipo_inmueble'])
    neighbors = ""
    if not filter_var:
        st.error('Please select a value')
    if filter_var == 'All':
        # st.warning("Using a resample of the data")
        pass
        # return
    else:
        for k, v in cols_traduccion.items():
            if v[1] == filter_var:
                filter_var = k
                break
        
        prev = data[filter_var].unique()[0]
        variable_values = list(data[filter_var].unique())
        neighbors = st.multiselect(
            "Choose its values", variable_values)
        st.markdown("""
        ##### Leave empty to analyze along all data
        """)
    if filter_var == 'All':
        dataShow = data
    else:
        if not neighbors:
            dataShow = data.loc[data[filter_var].isin(data[filter_var].unique())]
        else:
            dataShow = data.loc[data[filter_var].isin(neighbors)]

    dataShow.reset_index(drop=False, inplace=True)
    st.write("### Example of Available data", dataShow.sort_index())

    # BarPlot
    st.markdown("### First, lets understand how is the data distributed per location in Bogotá city")
    plt.figure(figsize=(8, 6))
    plt.subplot(1, 2, 1)
    barrioTemp = dataShow[['locnombre', 'lotcodigo']].groupby('locnombre').count().sort_values(by='lotcodigo',
                                                                                               ascending=True).reset_index()
    plt.barh(barrioTemp.locnombre, barrioTemp.lotcodigo)
    plt.title('Distribution of data per location')
    plt.ylabel("Location")
    first = barrioTemp.iloc[len(barrioTemp) - 1]
    plt.subplot(1, 2, 2)

    barrioTemp = dataShow[['estrato', 'lotcodigo']].groupby('estrato').count().sort_values(by='estrato',
                                                                                           ascending=True).reset_index()

    estra = barrioTemp.iloc[barrioTemp['lotcodigo'].idxmax()]['estrato']
    tempText = ' '.join(["As we can see", str(first[0]), "is the location with more available data overall and the stratum", str(
        estra[0]), "as well"])
    st.markdown(str(tempText))
    plt.barh(barrioTemp.estrato, barrioTemp.lotcodigo)
    plt.title('Distribution of data per stratum')
    plt.ylabel("Stratum")
    st.pyplot()

    st.markdown("### Now, lets understand some key attributes of the records than can be interesting for our analysis")

    ### Area Terreno
    st.markdown("")
    st.markdown("First, we have land area. This is how much Area (in meters) belongs to a property. Here is possible "
                "to see how is the land area related to the amount of available records")

    plt.hist(np.log(dataShow['oic_area_terreno'] + 1), bins=100)
    plt.xlabel("log(Land Area +1)")
    plt.ylabel("Amount")
    st.pyplot()

    st.markdown(
        "As you can see, there are some bars higher than others which represents the amount of records that have a "
        "similar Land Area")
    st.markdown("This said, the following table show the top 10 land areas measured in meters")
    temp = pd.DataFrame()
    temp['oic_area_terreno'] = np.round(dataShow['oic_area_terreno'], 2)
    temp['log_oic_area_terreno'] = np.log(dataShow['oic_area_terreno'] + 1)
    rest = temp.groupby(by='log_oic_area_terreno').count().sort_values(by='oic_area_terreno',
                                                                       ascending=False).reset_index()
    rest['Land Area (mts)'] = np.exp(rest['log_oic_area_terreno'] + 1)
    rest = rest.rename(columns={'oic_area_terreno': 'Amount of records'})
    st.table(rest[['Land Area (mts)', 'Amount of records']].head(10))

    ### Area Construcción

    st.markdown("Here is possible to see how is the construction area related to the amount of available records")
    plt.hist(np.log(dataShow['oic_area_construccion'] + 1), bins=100)
    plt.xlabel("log(Area Construcción+1)")
    plt.ylabel("Amount")
    st.pyplot()
    st.markdown("As you can see, there're some bars higher than others which represents the amount of records that "
                "have a similar Constructed Area")
    st.markdown("This said, the following table show the top 10 constructed areas measured in meters")
    temp = pd.DataFrame()
    temp['oic_area_construccion'] = np.round(dataShow['oic_area_construccion'], 2)
    temp['log_oic_area_construccion'] = np.log(dataShow['oic_area_construccion'] + 1)
    rest = temp.groupby(by='log_oic_area_construccion').count().sort_values(by='oic_area_construccion',
                                                                            ascending=False).reset_index()
    rest['Construction Area (mts)'] = np.exp(rest['log_oic_area_construccion'] + 1)
    rest = rest.rename(columns={'oic_area_construccion': 'Amount of records'})
    st.table(rest[['Construction Area (mts)', 'Amount of records']].head(10))

    ### Distances to interest places
    st.markdown("### Furthermore, we included in the data set the distance from the evaluated property to some "
                "interesting places, such as parks, highways, museums, Transmilenio stations, and others.")
    st.markdown("Whereas a distance of 0 represents that there's no close interest place, 1Km means that within the "
                "first 1Kms radius from the property there's an interesting place, 2Km means than within the 1st km "
                "and the 2nd km there's an interesting place, and so on so forth with the other distances")
    distancias = ['D_PARK', 'D_HIGHWAY', 'D_BIKEWAY', 'D_SSF',
                  'D_MUS', 'D_LIB', 'D_SITP', 'D_TM', 'D_P_TM',
                  'D_GY', 'D_IES', 'D_BOM', 'D_COL', 'D_IPS',
                  'DM_BIKEWAY', 'DM_BOM', 'DM_COL', 'DM_GY',
                  'DM_HIGHWAY', 'DM_IES', 'DM_IPS', 'DM_LIB',
                  'DM_MUS', 'DM_PARK', 'DM_P_TM', 'DM_SITP', 'DM_SSF', 'DM_TM']
    distancias = [str(x).lower() for x in distancias]
    distancias_km = []
    for var in distancias:
        dataShow[var + '_KM'] = dataShow[var].map(lambda x: math.ceil(x / 1000))
        distancias_km.append(var + '_KM')
    dataShow = dataShow.rename(columns={'d_park_KM': 'd_park_KM',
                                        'd_mus_KM': 'd_museum_KM',
                                        'd_gy_KM': 'd_cemetery_KM',
                                        'd_highway_KM': 'd_highway_KM',
                                        'd_lib_KM': 'd_library_KM',
                                        'd_ies_KM': 'd_higher_education_institution_KM',
                                        'd_bikeway_KM': 'd_bikeway_KM',
                                        'd_sitp_KM': 'd_sitp_station_KM',
                                        'd_bom_KM': 'd_firefighter_station_KM',
                                        'd_ssf_KM': 'd_soccer_court_KM',
                                        'd_tm_KM': 'd_transmilenio_station_KM',
                                        'd_col_KM': 'd_school_KM',
                                        'd_p_tm_KM': 'd_tm_portal_KM',
                                        'd_ips_KM': 'd_ips_KM',
                                        'dm_bikeway_KM': 'dm_bikeway_KM',
                                        'dm_highway_KM': 'dm_highway_KM',
                                        'dm_mus_KM': 'dm_museum_KM',
                                        'dm_bom_KM': 'dm_firefighter_station_KM',
                                        'dm_ies_KM': 'dm_higher_education_institution_KM',
                                        'dm_park_KM': 'dm_park_KM',
                                        'dm_col_KM': 'dm_school_KM',
                                        'dm_ips_KM': 'dm_ips_KM',
                                        'dm_p_tm_KM': 'dm_tm_portal_KM',
                                        'dm_gy_KM': 'dm_cemetery_KM',
                                        'dm_lib_KM': 'dm_library_KM',
                                        'dm_sitp_KM': 'dm_sitp_station_KM',
                                        'dm_tm_KM': 'dm_transmilenio_station_KM',
                                        'dm_ssf_KM': 'dm_soccer_court_KM'})
    # print(dataShow.columns)
    varsToShow = ['oft_codigo', 'lotcodigo', 'nombre_barrio', 'vfventa2020']
    varsToShow += ['d_park_KM', 'd_museum_KM', 'd_cemetery_KM', 'd_highway_KM', 'd_library_KM',
                   'd_higher_education_institution_KM', 'd_bikeway_KM', 'd_sitp_station_KM',
                   'd_firefighter_station_KM', 'd_soccer_court_KM', 'd_transmilenio_station_KM',
                   'd_school_KM', 'd_tm_portal_KM', 'd_ips_KM', 'dm_bikeway_KM', 'dm_highway_KM',
                   'dm_museum_KM', 'dm_firefighter_station_KM', 'dm_higher_education_institution_KM',
                   'dm_park_KM', 'dm_school_KM', 'dm_ips_KM', 'dm_tm_portal_KM', 'dm_cemetery_KM',
                   'dm_library_KM', 'dm_sitp_station_KM', 'dm_transmilenio_station_KM', 'dm_soccer_court_KM']
    # print(varsToShow)
    st.write("### Example of Available data and interesting places", dataShow[varsToShow].sort_index())

    st.markdown("### Now lets understand how these interesting places distances are related to the final sale value")
    st.markdown("#### Here you can only focus your eyes in those darker and lighter colors, this is because those are "
                "the distances that are more related to the final sale value!")
    correlation = dataShow[varsToShow[3:17]].corr()
    #mask = np.zeros_like(correlation)
    #mask[np.triu_indices_from(mask)] = True
    #with sns.axes_style("white"):
    #    f, ax = plt.subplots(figsize=(25, 15))
    #    ax = sns.heatmap(correlation, mask=mask, vmax=.3, square=True, cmap="YlGnBu", annot=True)
    #st.pyplot()

    corr_dist = pd.DataFrame(correlation['vfventa2020'])
    max = 0
    maxi = 0
    min = 10000000
    mini = 0
    for k, v in corr_dist.iterrows():
        if v[0] != 1.0 and v[0] > max:
            max = v[0]
            maxi = k
        if v[0] < min:
            min = v[0]
            mini = k
    textoCorrelation = 'According to this relations, the distance to the place {} is related to the final ' \
                       'property value, this means that while the distance increases, the final value increases ' \
                       'in {} value units.'.format(maxi, round(max, 3))
    textoCorrelation2 = 'On the other hand, while the distance to the place {} increases, the price change in {} ' \
                        'value units'.format(mini, round(min, 3))
    st.markdown(textoCorrelation)
    st.markdown("")
    st.markdown(textoCorrelation2)
    f, ax = plt.subplots(figsize=(12, 8))
    ax = sns.heatmap(corr_dist, annot=True, cmap="YlGnBu", vmax=.3)
    st.pyplot()

#ESDA
def esda(sdf):
    # sdf = get_pol_db()
    sdf = sdf.fillna(0)
    sdf.estrato = sdf.estrato.astype(int)
    variables = [v[1] for v in cols_traduccion_geo.values()][3:-1]
    # variables = sdf.columns[3:-1]
    variables.insert(0,'Select')

    st.markdown("""
    ### Exploratory spatial data analysis: 
    The data showed is on neighborhood level this data is not exactly the complete data, but works to get a better visualization
    """)
    # st.title('El eda')
    var_name = st.selectbox("Select a variable (the map is the mean (continuous) and mode (categorical) of the variable of each neighborhoood)",variables)
    
    if var_name != 'Select':
        var = [k for k,v in cols_traduccion_geo.items() if v[1] == var_name][0]
        folium_static(neighborhoodmap(sdf,var,var_name))


#Models
def models():
    st.markdown("""
    ### Model Evaluation
    """)
    # st.title('Los modelos')

    with open('models/models_final.json') as f:
        json_data = json.load(f)
    models = [i['name'] for i in json_data]
    model_name = st.selectbox("Choose a model: ",models[:-1])

    models_data = [i['data'] for i in json_data if i['name'] == model_name][0]
    st.write([i['Description'] for i in json_data if i['name'] == model_name][0])

    try:
        test_Estr = [i['data'] for i in models_data if i['Type'] == "Estrato"][0]
        by_estratos = st.checkbox('Modelo por estratos')
    except:
        by_estratos = False

    if by_estratos:
        estrato_selected = st.selectbox("",["All",1,2,3,4,5,6])
        m_t = [i['data'] for i in models_data if i['Type'] == "Estrato"][0]
        if estrato_selected == "All":
            for estrato in m_t:
                #st.write(m_t)
                show_model_atributes(estrato)
                st.write ("\n \n")
        else:
            m_t_e = [i for i in m_t if i['Estrato'] == estrato_selected][0]
            show_model_atributes(m_t_e)
    else:
        m_t = [i for i in models_data if i['Type'] == "General"][0]
        show_model_atributes(m_t)


#for models show
def show_model_atributes(model):
    for k,v in model.items():
        if k == 'Type':
            pass
        elif k == 'variables':
            vars_data = model['variables']
            st.write("***Variables:*** ")
            df_var = pd.DataFrame(vars_data)
            try:
                df_var = df_var[['Variable','Coefficient','p_value']]
                df_var['Coefficient'] = df_var['Coefficient'].apply(lambda x: round(x,3))
            except:
                df_var = df_var[['Variable','Importance']]

            st.write(df_var)

        elif k == 'Estrato':
            st.markdown(f"### ***{k}:*** {v} ")
        elif k == 'Variables':
            st.markdown(f"**{k}:**")
            st.write(pd.Series(v))
        else:
            if type(v)==float:
                st.markdown(f"**{k}:** {round(v,3)} ")
            else:
                st.markdown(f"**{k}:** {v} ")
            

def neighborhoodmap(sdf,column,column_alias):
    m = folium.Map(location=[4.65, -74.1],
                                zoom_start=11,
                                tiles="OpenStreetMap")
    try:
        min_cn, max_cn = sdf[column].quantile([0.01,0.99]).apply(round, 2)

        colormap = branca.colormap.LinearColormap(
            colors=['white','yellow','green','blue'],
            vmin=min_cn,
            vmax=max_cn
        )

        colormap.caption=column
        style_function = lambda x: {
            'fillColor': colormap(x['properties'][column]),
            'color': 'white',
            'weight':0.6,
            'fillOpacity':0.7
        }


        stategeo = folium.GeoJson(
            sdf,
            name=column,
            style_function=style_function,
            tooltip=folium.GeoJsonTooltip(
                fields=['scanombre',column],
                aliases=['Neighborhood',column_alias],
                localize=True
            )
        ).add_to(m)
        colormap.add_to(m)
    except:
        cantities = len(sdf[column].unique())

        colormap = branca.colormap.LinearColormap(
                colors=['yellow','green','blue','red',"purple","black","brown"],
                vmin=1,
                vmax=cantities-5
            )


        colors = dict(zip(sdf[column].unique(),[colormap.rgba_hex_str(i+1) for i in range(len(sdf[column].unique()))]))
        
        def return_col(colors,v):
            return colors[v]


        style_function = lambda x: {
                    'fillColor': return_col(colors,x['properties'][column]),
                    'color': 'white',
                    'weight':0.6,
                    'fillOpacity':0.7
                }

        stategeo = folium.GeoJson(
                sdf,
                    name=column,
                    style_function=style_function,
                    tooltip=folium.GeoJsonTooltip(
                        fields=['scanombre',column],
                        aliases=['Neighborhood',column],
                        localize=True
                    )
                ).add_to(m)
    return m


if __name__ == "__main__":
    table_data = get_data_db()
    poly_data = get_pol_db()
    main(table_data,poly_data)
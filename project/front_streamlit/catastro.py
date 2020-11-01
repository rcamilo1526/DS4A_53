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

#plots n maps
import folium
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import math
# import plotly.graph_objects as go
# from plotly import express as px
# from plotly.subplots import make_subplots

#secrets
import config_db
##############

# matplotlib.use("TkAgg")
matplotlib.use("Agg")
COLOR = "black"
BACKGROUND_COLOR = "#fff"


def main():
    #style
    st.markdown("""
    <style>
    body {

    }
    .sidebar .sidebar-content {
        background-image: linear-gradient(#199BD8,#199BD8);
        color: white;
    }
    </style>
        """, unsafe_allow_html=True)
    select_block_container_style()
    #/style
    #principal
    ttitle = st.title("Modelo avaluatorio catastro distrital ")
    st.markdown("""
        ## Equipo 53
        """)
    #/principal
    #sidebar
    st.sidebar.title("UAECD")
    st.sidebar.image('img/logon.png')
    selection = st.sidebar.selectbox("Elija",("EDA","ESDA","Models"))
    st.sidebar.header("Team 53")
    st.sidebar.markdown(
            """
    - [Repositorio] (https://github.com/rcamilo1526/DS4A_53)

    """
        )
    # with Grid("1 1 1", color=COLOR, background_color=BACKGROUND_COLOR) as grid:
    #     grid.cell(
    #         class_="a",
    #         grid_column_start=1,
    #         grid_column_end=3,
    #         grid_row_start=1,
    #         grid_row_end=4,
    #     ).markdown("# This is A Markdown Cell")
    #     grid.cell("b", 3, 4, 1, 4).text("The cell to the left is a dataframe")






    #/sidebar
    #data
    # df = get_data_db()


    #/data

    if selection == "EDA":
        eda()
    elif selection == "ESDA":
        esda()
    else:
        models()

def get_dataframe():
    data_types = {'preczhf':'category',
                'OFT_TIPO_INMUEBLE':'category',
                'OFT_TIPO_NORMA_JURIDICA':'category',
                'OIA_TIENE_ASCENSOR':'category',
                'LOCCODIGO':'category',
                'suelo':'category',
                'actividad':'category',
                'tratamiento_urb':'category',
                'topografia':'category',
                'serpub':'category',
                'serpub_tipo':'category',
                'serpub_especif':'category',
                'via':'category',
                'clase_via':'category',
                'estado_via':'category',
                'influencia_via':'category',
                'actividad_economica':'category',
                'actividad_economica_tipo':'category',
                'tipo_segun_actividad':'category',
                'CP_TERR_AR':'category',
                }
    columns_useless = ['Unnamed: 0','OFT_CODIGO','LOTCODIGO','CODIGO_CON',
                        'barmanpre','preczhf','CODIGO_RES','MANZANA_ID','NOMBRE_BARRIO']

    ofertas = pd.read_csv('data/ofertas_v1_1.csv',dtype=data_types)
    ofertas.drop(columns=columns_useless,inplace=True)
    for i in ofertas.columns:
        if i.startswith("DM"):
            ofertas.drop(columns=i,inplace=True)
    ofertas.dropna(inplace= True)
    return ofertas



def get_data_db():
    con = psycopg2.connect(database=config_db.database,user=config_db.user,password=config_db.password,host=config_db.host)
    data = pd.read_sql("select * from datos", con)

    return data

def get_pol_db():
    pass



#EDA
def eda():
    st.markdown("""
    ### Exploratory data analysis
    """)
    con = psycopg2.connect(database=config_db.database,user=config_db.user,password=config_db.password,host=config_db.host)
    data = pd.read_sql("select * from datos", con)
    print('init')
    print(data.head())
    ##data.reset_index(drop=False,inplace=True)

    filter_var = st.multiselect(
    "Choose ONE variable to filter by", list(['nombre_barrio','oft_tipo_inmueble']), ['nombre_barrio'])

    if not filter_var:
        st.error("Please select at least one variable.")
        return
    
    if filter_var[0]=='oft_tipo_inmueble':
        prev = 'Apartamento'
    else:
        prev = 'PUENTE LARGO'
    
    neighbors = st.multiselect(
    "Choose its values", list(data[filter_var[0]].unique()), [prev])
    st.markdown("""
    ##### Leave empty to analyze along all data
    """)

    if not neighbors:
        neighbors = list(data[filter_var[0]].unique())
        st.warning("Using all values")
        #st.error("Showing all values")
        #return
    
    dataShow = data.loc[data[filter_var[0]].isin(neighbors)]
    
    dataShow.reset_index(drop=False,inplace=True)
    st.write("### Example of Available data", dataShow.sort_index())

    #histogram
    st.markdown("""
    #### Relation among logarithm of catastral appraisal and the data as general
    """)
    st.set_option('deprecation.showPyplotGlobalUse', False)
    plt.figure(figsize=(15,10))
    plt.subplot(1,2,1)
    plt.hist(np.log(dataShow['avaluo_cat']+1), bins=100)
    plt.title('Distribution of Catastral appraisal')
    plt.xlabel("log(Avaluo_cat+1)")
    plt.ylabel("count")

    plt.subplot(1,2,2)
    plt.hist(np.log(dataShow['avaluo_com']+1), bins=100)
    plt.title('Distribution of Comercial appraisal')
    plt.xlabel("log(Avaluo_com+1)")
    plt.ylabel("count")
    st.pyplot()


    #######################

    st.markdown("""
    #### Relation among logarithm of catastral appraisal and some interesting columns
    """)

    dataShow['Log_AVALUO_CAT'] = np.log(dataShow['avaluo_cat'])
    dataShow['Log_OIC_AREA_TERRENO'] = np.log(dataShow['oic_area_terreno'])
    dataShow['Log_OIC_AREA_CONSTRUCCION'] = np.log(dataShow['oic_area_construccion'])

    plt.figure(figsize=(20,15))
    for i,var in enumerate(["oft_tipo_norma_juridica", "Log_OIC_AREA_TERRENO", "Log_OIC_AREA_CONSTRUCCION","log_vfventa2020"]):
        plt.subplot(2,2,i+1)
        plt.title('Distribution of Catastral appraisal')
        if var in ['oft_tipo_norma_juridica']:
            sns.violinplot(x=var, y='Log_AVALUO_CAT', data=dataShow)
        elif var in ["Log_OIC_AREA_TERRENO", "Log_OIC_AREA_CONSTRUCCION","log_vfventa2020"]:
            sns.scatterplot(x=var,y='Log_AVALUO_CAT',data=dataShow, alpha=0.10,color='b')
    st.pyplot()

    st.markdown("""
    #### Relation among logarithm of catastral appraisal and the distance in KMs to interesting places
    """)
    st.markdown("""
    ###### Whereas 0 KM represents that there's no distance registered, 1 Km means that the place is located less than 1 Km from the property, 2 Km located less than 2 Km from the property, so on ans so forth.
    """)

    distancias = ['d_park', 'd_highway', 'd_bikeway', 'd_ssf', 'd_mus', 'd_lib', 'd_sitp','d_tm', 'd_p_tm', 'd_gy', 'd_ies', 'd_bom', 'd_col', 'd_ips']

    title_distancias = ['Distance to Park','Distance to Highway', 'Distance to Bikeway','Distance to SSF',
              'Distance to MUS','Distance to Library','Distance to SITP','Distance to Transmilenio Station', 'D_P_TM','Distance to Transmilenio Portal',
              'Distance to GY','Distance to IES','Distance to BOM','Distance to Col','Distance to IPS']

    distancias_km = []
    for var in distancias:
      dataShow[var + '_KM'] = dataShow[var].map(lambda x: math.ceil(x/1000))
      distancias_km.append(var+'_KM')

    j=0
    for i,var in enumerate(distancias_km):
        if i%2==0:
            plt.figure(figsize=(15,8))
        plt.subplot(1,2,j+1)
        plt.title(title_distancias[i])
        sns.violinplot(x=var, y='Log_AVALUO_CAT', data=dataShow)
        j += 1 
        if (i+1)%2==0:
            st.pyplot()
            j = 0
    
    st.markdown("""
    #### Correlation among interesting places and the catastral appraisal.
    """)
    corr_dist = dataShow[['d_park', 'd_highway', 'd_bikeway', 'd_ssf', 'd_mus', 'd_lib', 'd_sitp','d_tm', 'd_p_tm', 'd_gy', 'd_ies', 'd_bom', 'd_col', 'd_ips','Log_AVALUO_CAT']].corr()
    corr_dist = pd.DataFrame(corr_dist['Log_AVALUO_CAT'])
    plt.subplots(figsize=(15, 8))
    sns.heatmap(corr_dist,annot=True)
    st.pyplot()
#ESDA
def esda():
    con = psycopg2.connect(database=config_db.database,user=config_db.user,password=config_db.password,host=config_db.host)

    sdf = gpd.GeoDataFrame.from_postgis("select * from barrios_data", con, geom_col='geom')
    sdf = sdf.fillna(0)
    
    variables = sdf.columns[3:-1]
    variables.insert(0,'<select>')

    st.markdown("""
    ### Exploratory spatial data analysis: The data showed is on level of neighborhood this data is not exactly the data, but works to get a better visualization
    """)
    # st.title('El eda')
    var = st.selectbox("Select a variable (the map is the mean of this variable of each neighborhoood)",variables)
    if var != '<select>':
        folium_static(neighborhoodmap(sdf,var))


#Models
def models():
    st.markdown("""
    ### Evaluación de los modelos
    """)
    # st.title('Los modelos')
    model = st.selectbox("Elija un modelo",("Regresion linear","Lasso","Random forest","Log"))


def neighborhoodmap(sdf,column):
    m = folium.Map(location=[4.65, -74.1],
                            zoom_start=11,
                            tiles="OpenStreetMap")
    min_cn, max_cn = sdf[column].quantile([0.01,0.99]).apply(round, 2)

    colormap = branca.colormap.LinearColormap(
        colors=['white','yellow','green','blue'],
    #     #index=beat_cn['count'].quantile([0.2,0.4,0.6,0.8]),b
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
            aliases=['Barrio',column], 
            localize=True
        )
    ).add_to(m)
    
    # Save to html
    colormap.add_to(m)
    # m.save('esda_maps/vfventa2020.html')

    # m.fit_bounds(stategeo.get_bounds()) 
    return m


def select_block_container_style():
    """Add selection section for setting setting the max-width and padding
    of the main block container"""
    # st.sidebar.header("Block Container Style")
    max_width_100_percent = True #st.sidebar.checkbox("Max-width: 100%?", False)
    if not max_width_100_percent:
        max_width = st.sidebar.slider("Select max-width in px", 100, 2000, 1200, 100)
    else:
        max_width = 900
    dark_theme = False# st.sidebar.checkbox("Dark Theme?", False)
    padding_top = 2 #st.sidebar.number_input("Select padding top in rem", 0, 200, 5, 1)
    padding_right = 15 # st.sidebar.number_input("Select padding right in rem", 0, 200, 1, 1)
    padding_left = 15 #st.sidebar.number_input("Select padding left in rem", 0, 200, 1, 1)
    padding_bottom = 15# st.sidebar.number_input("Select padding bottom in rem", 0, 200, 10, 1)
    if dark_theme:
        global COLOR
        global BACKGROUND_COLOR
        BACKGROUND_COLOR = "rgb(17,17,17)"
        COLOR = "#fff"

    _set_block_container_style(
        max_width,
        max_width_100_percent,
        padding_top,
        padding_right,
        padding_left,
        padding_bottom,
    )


def _set_block_container_style(
    max_width: int = 1200,
    max_width_100_percent: bool = False,
    padding_top: int = 5,
    padding_right: int = 1,
    padding_left: int = 1,
    padding_bottom: int = 10,
):
    if max_width_100_percent:
        max_width_str = f"max-width: 100%;"
    else:
        max_width_str = f"max-width: {max_width}px;"
    st.markdown(
        f"""
<style>
    .reportview-container .main .block-container{{
        {max_width_str}
        padding-top: {padding_top}rem;
        padding-right: {padding_right}rem;
        padding-left: {padding_left}rem;
        padding-bottom: {padding_bottom}rem;
    }}
    .reportview-container .main {{
        color: {COLOR};
        background-color: {BACKGROUND_COLOR};
    }}
</style>
""",
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    main()
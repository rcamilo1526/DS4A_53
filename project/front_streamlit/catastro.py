import streamlit as st 
import streamlit.components.v1 as components

# import pandas as pd
import numpy as np
import pandas as pd


from sklearn import datasets 
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.decomposition import PCA

import matplotlib.pyplot as plt

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

df = get_dataframe()
variables = df.columns
#style
st.markdown("""
<style>
body {

}
.sidebar .sidebar-content {
    background-image: linear-gradient(#199BD8,#199BD8);
    color: white;
}
.sidebar .sidebar-close{

}

.main .block-container{
        padding-top: 0 rem !important;
        padding-right: 1 rem !important;
        padding-left: 1 rem !important;
        padding-bottom: 0 rem !important;
    }
</style>
    """, unsafe_allow_html=True)
#/style
#principal
ttitle = st.title("Modelo avaluatorio catastro distrital ")
st.markdown("""
    ## Equipo 53
    """)
#/principal
#sidebar
st.sidebar.title("UACD")
st.sidebar.image('img/logon.png')
selection = st.sidebar.selectbox("Elija",("EDA","Models"))
st.sidebar.header("Team 53")
st.sidebar.markdown(
        """
- [Repositorio] (https://github.com/rcamilo1526/DS4A_53)

"""
    )

#/sidebar
#EDA
def eda():
    st.markdown("""
    ### Exploratory data analysis
    """)
    # st.title('El eda')
    var = st.selectbox("Elija una variable",variables)
    components.iframe("https://ds4aavaluos.s3.us-east-2.amazonaws.com/map_avaluo.html"
                    ,width=700, height=800)


#Models
def models():
    st.markdown("""
    ### Evaluación de los modelos
    """)
    # st.title('Los modelos')
    model = st.selectbox("Elija un modelo",("Regresion linear","Lasso","Random forest","Log"))




if selection == "EDA":
    eda()
else:
    models()



# ofertas = pd.read_csv('data/')



# if st.sidebar.button('EDA'):
#     eda()
    
# if st.sidebar.button('Modelos'):
#     models()



# dataset_name = st.selectbox("Select Dataset",("Iris","Breast Cancer","Wine dataset"))
# #st.write(dataset_name)

# classifier_name = st.sidebar.selectbox("Select Classifier",("KNN","SVM","Random Forest"))

# def get_dataset(dataset_name):
#     if dataset_name == "Iris":
#         data = datasets.load_iris()
#     elif dataset_name == "Breast Cancer":
#         data = datasets.load_breast_cancer()
#     else:
#         data = datasets.load_wine()
#     X = data.data
#     y = data.target
    
#     return X,y

# X,y = get_dataset(dataset_name)

# st.write(f"Shape of the dataset: {X.shape}")

# st.write(f"Number of classes: {len(np.unique(y))}")

# def add_parameter_ui(clf_name):
#     params = dict()
#     if clf_name == "KNN":
#         K = st.sidebar.slider("K",1,15)
#         params["K"] = K

#     elif clf_name == "SVM":
#         C = st.sidebar.slider("C",0.01,10.0)
#         params["C"] = C
#     else:
#         max_depth = st.sidebar.slider("max_depth",2,15)
#         n_estimators = st.sidebar.slider("n_estimators",1,100)
#         params["max_depth"] = max_depth
#         params['n_estimators'] = n_estimators
#     return params

# params = add_parameter_ui(classifier_name)

# def get_classifier(clf_name,params):
#     if clf_name == "KNN":
#         clf = KNeighborsClassifier(n_neighbors = params['K'])
#     elif clf_name == "SVM":
#         clf = SVC(C=params['C'])
#     else:
#         clf = RandomForestClassifier(n_estimators=params['n_estimators'],
#                                         max_depth=params['max_depth'],random_state=1234)
#     return clf                                       
    
# clf = get_classifier(classifier_name,params)   
    
# X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.25,random_state=1234)

# clf.fit(X_train,y_train)

# y_pred = clf.predict(X_test)

# acc = accuracy_score(y_test, y_pred)
# st.write(f"Classifier= {classifier_name}")
# st.write(f"Accuracy = {acc}")

# #plot
# pca = PCA(2)
# X_projected = pca.fit_transform(X)
# x1 = X_projected[:,0]
# x2 = X_projected[:,1]

# fig = plt.figure()
# plt.scatter(x1,x2,c=y,alpha=0.8,cmap='viridis')
# plt.xlabel("pc 1")
# plt.ylabel("pc 2")
# plt.colorbar()

# st.pyplot(fig)

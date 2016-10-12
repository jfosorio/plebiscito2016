
# coding: utf-8

# # Mostrando los resultados usando Bohek

# In[1]:

import numpy as np
import pickle
import numpy
from bokeh.plotting import figure, show, output_file
from bokeh.io import output_notebook
from bokeh.mpl import  to_bokeh 
from bokeh.resources import INLINE
output_notebook(resources=INLINE)
from scipy.stats import linregress
from numpy import logspace, sin, cos, pi


# ## Importe los datos y haga los calculos simples

# In[2]:

municipios_y_victimas = pickle.load(open('./plebicito_municipios_y_victimas20161010.pickle', 'rb'))
municipios_y_victimas['CocienteSi'] = municipios_y_victimas['Si']/municipios_y_victimas['habilitados'] 
municipios_y_victimas['CocienteNo'] = municipios_y_victimas['No']/municipios_y_victimas['habilitados'] 
municipios_y_victimas['CocienteVictimas'] = municipios_y_victimas['TOTAL']/municipios_y_victimas['habilitados']


# ## creando una simple regresion

# In[3]:

slope_si, intercept_si, r_si, p_si, stderr_si = linregress(municipios_y_victimas['CocienteVictimas'], municipios_y_victimas['CocienteSi'])
slope, intercept, r, p, stderr = linregress(municipios_y_victimas['CocienteVictimas'], municipios_y_victimas['CocienteNo'])
XMIN = min(municipios_y_victimas['CocienteVictimas'])
XMAX = max(municipios_y_victimas['CocienteVictimas'])
x = np.linspace(XMIN, XMAX, 10)


# ## generando una grafica con bohek

# In[7]:


# Modelos de datos usados
from bokeh.models import (
    ColumnDataSource,
    HoverTool,
    LogColorMapper
)


# Create colores
municipios_y_victimas['Color'] = "#F1EEF6"
municipios_y_victimas.loc[municipios_y_victimas['departamento'] =='ANTIOQUIA', 'Color'] = "#980043"

source = ColumnDataSource(data=dict(
    cocientevictimas=municipios_y_victimas['CocienteVictimas'].values,
    cocienteSi=municipios_y_victimas['CocienteSi'].values,
    cocienteNo=municipios_y_victimas['CocienteNo'].values,
    municipio=municipios_y_victimas['municipio'],
    departamento=municipios_y_victimas['departamento'],
    colores = municipios_y_victimas['Color'],
))




TOOLS="pan,wheel_zoom,box_zoom,reset,hover,save"

p = figure(tools=TOOLS, width=700, height=500)

p.grid.grid_line_color = None

p.scatter('cocientevictimas', 'cocienteSi', source=source, 
          fill_color='colores', size=6)

p.line(x, slope_si*x+intercept_si, legend='Regresión',
       line_dash="dashed", line_width=2)
# p.scatter('cocientevictimas', 'cocienteNo', source=source, legend='votos No')
hover = p.select_one(HoverTool)
hover.point_policy = "follow_mouse"
hover.tooltips = [
    ("Municipio", "@municipio"),
    ("Departamento", "@departamento")
]
# 

p.xaxis.axis_label = "# de victimas / # numero de votos validos"
p.yaxis.axis_label = 'votos Sí / # numero de votos validos'
p.xaxis.axis_label_text_font_size = "12pt"
p.yaxis.axis_label_text_font_size = "12pt"
output_file("victimas_si.html", title="log plot example")
# show(p)


# In[ ]:




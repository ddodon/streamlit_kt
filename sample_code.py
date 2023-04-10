# -*- coding: utf-8 -*-
import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as html
from  PIL import Image
import numpy as np
import pandas as pd
import altair as alt
import io
import plotly.express as px
from outside import outside
from inside import inside

st.title('KT 가치고객영업지원팀 (대구/경북)')
## 사이드바
with st.sidebar:
    chanel = option_menu("가치팀", ["사내채널", "사외채널"],
        icons=['house', 'bar-chart-fill', 'bar-chart-line'],
        menu_icon="app-indicator", default_index=0,
        styles={
            "container": {"padding": "5!important", "background-color": "#fafafa"},
            "icon": {"color": "orange", "font-size": "25px"}, 
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "#02ab21"},
        }
    )

if chanel == '사내채널':
    inside()

else:
    outside()

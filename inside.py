# -*- coding: utf-8 -*-
import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as html
from  PIL import Image
import numpy as np
import pandas as pd
import altair as alt
import plotly.express as px

def inside():
    st.header('사내채널 성과 현황')
    st.header('\n')

    ##데이터 로딩 화면 및 데이터 로드
    @st.cache_data
    def load_data():
        data_load_state = st.text('데이터를 불러오는 중 입니다...')
        url = 'https://github.com/ddodon/streamlit_kt/raw/main/b2b_in_230411.xlsx'
        #url = '/Users/don/Desktop/스트림릿/b2b_in_230411.xlsx' # 디버깅용 로컬데이터 경로
        
        df = pd.read_excel(url, engine = "openpyxl")
        data_load_state.text('데이터 로드 완료! (~4/11 데이터)')
        return df
    data_load_state = st.empty()
    df = load_data()

    # 영업부 이름에서 '법인고객영업부' 부분 제거하고 짧은 이름으로 변경
    df['영업부'] = df['영업부'].str.replace('법인고객영업부', '').str.strip()
        
    if st.checkbox('원본데이터(raw_data) 보기'):
        st.subheader('원본')
        st.write(df)
        
    st.subheader('영업부별 영업기회 개수')
    ## 1.영업부별 영업기회 차트
    b2b_class1 = df['영업부'].value_counts()
    b2b_counts_chart = alt.Chart(b2b_class1.reset_index()).mark_bar().encode(
        x=alt.X('index:N', axis=alt.Axis(title='영업부',labelAngle=45)),
        y=alt.Y('영업부:Q', axis=alt.Axis(title='영업기회 개수')),
        color=alt.Color('index:N', scale=alt.Scale(range=['steelblue']), legend=None))
    text = b2b_counts_chart.mark_text(dy=-10).encode(
            text=alt.Text('영업부'))
    st.altair_chart(b2b_counts_chart+text,use_container_width=True) ##반응형차트

    ## 2. 영업부별 영업기회 합계
    b2b_sum = df.groupby('영업부').sum()
    b2b_sum_chart = alt.Chart(b2b_sum.reset_index()).mark_bar().encode(
        x=alt.X('영업부', axis=alt.Axis(title='영업부',labelAngle=45)),
        y=alt.Y('영업기회금액', axis=alt.Axis(title='영업기회금액 (G=10억원)', format='s')),
        color=alt.Color('index:N', legend=None)
    )
    text = b2b_sum_chart.mark_text(dy=-10).encode(
            text=alt.Text('영업기회금액', format=',.0f')
        )
    st.altair_chart(b2b_sum_chart+text, use_container_width=True)


    ## 3. 판매 상품별 차트
    st.subheader('판매상품별 영업기회 개수')
    # 영업부 선택
    b2b_team = df['영업부'].unique().tolist()
    b2b_team.sort()
    #리스트 순서에 맞게 재정렬
    b2b_team.insert(0, b2b_team.pop(b2b_team.index('동대구'))) 
    b2b_team.insert(1, b2b_team.pop(b2b_team.index('달서')))
    b2b_team.insert(2, b2b_team.pop(b2b_team.index('서대구')))
    b2b_team.insert(0, '전체')
    b2b_box1 = st.selectbox("영업부 선택", b2b_team, key='1레벨')

    # 선택된 영업부의 판매상품 대분류별 개수 시각화
    if b2b_box1 =='전체':
        b2b_class1 = df['영업기회대표상품1레벨'].value_counts()
    else:
        b2b_class1 = df.loc[df['영업부'] == b2b_box1, '영업기회대표상품1레벨'].value_counts()
        
    b2b_class1_chart = alt.Chart(b2b_class1.reset_index()).mark_bar().encode(
        x=alt.X('index:N', axis=alt.Axis(title='상품 대분류',labelAngle=45)),
        y=alt.Y('영업기회대표상품1레벨:Q', axis=alt.Axis(title='개수')),
        color=alt.Color('index:N', scale=alt.Scale(range=['steelblue']), legend=None)
    )
    text = b2b_class1_chart.mark_text(dy=-8).encode(
        text=alt.Text('영업기회대표상품1레벨:Q')
    )
    st.altair_chart(b2b_class1_chart+text, use_container_width=True)



    ## 4.판매 상품 소분류별 차트
    b2b_box2 = st.selectbox("영업부 선택", b2b_team,key='2레벨')
    if b2b_box2 =='전체':
        b2b_class2 = df['영업기회대표상품2레벨'].value_counts()
    else:
        b2b_class2 = df.loc[df['영업부'] == b2b_box2, '영업기회대표상품2레벨'].value_counts()
    b2b_class2_chart = alt.Chart(b2b_class2.reset_index()).mark_bar().encode(
        x=alt.X('index:N', axis=alt.Axis(title='상품 소분류',labelAngle=90,labelLimit=0)),
        y=alt.Y('영업기회대표상품2레벨:Q', axis=alt.Axis(title='개수')),
        color=alt.Color('index:N', scale=alt.Scale(range=['steelblue']), legend=None)
    )
    text = b2b_class2_chart.mark_text(dy=-8).encode(
        text=alt.Text('영업기회대표상품2레벨:Q')
    )
    st.altair_chart(b2b_class2_chart+text,use_container_width=True)
    
    # 5. 각 영업부별 최다 판매 항목 구하기
    b2b_rank = df.groupby('영업부')['영업기회대표상품1레벨'].apply(lambda x: x.value_counts().index[0]).reset_index()
    b2b_rank['영업기회대표상품2레벨'] = b2b_rank['영업부'].apply(lambda x: df.loc[df['영업부'] == x, '영업기회대표상품2레벨'].value_counts().index[0])
    b2b_rank['영업기회대표상품3레벨'] = b2b_rank['영업부'].apply(lambda x: df.loc[df['영업부'] == x, '영업기회대표상품3레벨'].value_counts().index[0])
    b2b_rank['영업기회대표상품4레벨'] = b2b_rank['영업부'].apply(lambda x: df.loc[df['영업부'] == x, '영업기회대표상품4레벨'].value_counts().index[0])
    b2b_rank = b2b_rank.rename(columns={'영업기회대표상품1레벨':'최다판매(대분류)'})
    b2b_rank = b2b_rank.rename(columns={'영업기회대표상품2레벨':'최다판매(소분류)'})
    b2b_rank = b2b_rank.rename(columns={'영업기회대표상품3레벨':'최다판매(자세히)'})
    b2b_rank = b2b_rank.rename(columns={'영업기회대표상품4레벨':'최다판매 상품'})
    b2b_rank = b2b_rank.reindex([4, 3, 5, 1, 2, 0])
    # 인덱스 재정렬
    b2b_rank = b2b_rank.reset_index(drop=True)

    st.write(b2b_rank)


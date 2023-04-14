import streamlit as st
import pandas as pd
import altair as alt

def outside():
    st.header('사외 채널 성과 현황')
    st.header('\n')
    
    @st.cache_data
    def load_data():
        data_load_state = st.text('데이터를 불러오는 중 입니다...')
        #url = 'https://github.com/ddodon/streamlit_kt/raw/main/sample_data.xlsx'
        url = '/Users/don/Desktop/스트림릿/b2b_out_230411.xlsx' # 디버깅용 로컬데이터 경로
        
        df = pd.read_excel(url, engine = "openpyxl")
        data_load_state.text('데이터 로드 완료! (22/12/26 ~ 23/4/11 데이터)')
        return df
    data_load_state = st.empty()
    df = load_data()
    
    if st.checkbox('원본데이터(raw_data) 보기'):
        st.subheader('원본')
        st.write(df)
    
    ## 0. SA 채널 이름 요약
    df['SA'] = df['SA'].replace({'(주)크래프트_B2B Sales Agent': '크래프트', 
                                '(주)대운정보_B2B Sales Agent': '대운',
                                '(주)다우통신': '다우',
                                '(주)세존_B2B세일즈존_B2BSalesAgent': '세존',
                                '주식회사 엠텍': '엠텍',
                                '(주)베네솔루션': '베네솔루션',
                                '제이솔루션_유선': '제이솔루션',
                                '주식회사 네트아이티': '네트아이티',
                                '세나정보통신_B2B Sales Agent': '세나',
                                '유비텍_유선': '유비텍'})
    

    st.subheader('SA별 실적 개수')
    ## 1.SA별 실적 차트
    b2b_class1 = df['SA'].value_counts()
    b2b_counts_chart = alt.Chart(b2b_class1.reset_index()).mark_bar().encode(
        x=alt.X('index:N', axis=alt.Axis(title='SA',labelAngle=-90, labelFontSize=15)),
        y=alt.Y('SA:Q', axis=alt.Axis(title='실적 개수')),
        color=alt.Color('index:N', scale=alt.Scale(range=['grey']), legend=None))
    text = b2b_counts_chart.mark_text(dy=-10).encode(
            text=alt.Text('SA'))
    st.altair_chart(b2b_counts_chart+text,use_container_width=True) ##반응형차트
    
    ## 2. 판매상품별 차트
    st.subheader('판매상품별 실적개수')
    # SA 선택
    sa_team = df['SA'].unique().tolist()
    sa_team.sort()
    sa_team.insert(0, '전체')
    b2b_box1 = st.selectbox("SA 선택", sa_team, key='1레벨')
    
    if b2b_box1 =='전체':
        b2b_class1 = df['분석상품레벨1'].value_counts()
    else:
        b2b_class1 = df.loc[df['SA'] == b2b_box1, '분석상품레벨1'].value_counts()
        
    b2b_class1_chart = alt.Chart(b2b_class1.reset_index()).mark_bar().encode(
        x=alt.X('index:N', axis=alt.Axis(title='Telco/Digico 분류',labelAngle=45)),
        y=alt.Y('분석상품레벨1:Q', axis=alt.Axis(title='개수')),
        color=alt.Color('index:N', scale=alt.Scale(range=['grey']), legend=None)
    )
    text = b2b_class1_chart.mark_text(dy=-8).encode(
        text=alt.Text('분석상품레벨1:Q')
    )
    st.altair_chart(b2b_class1_chart+text, use_container_width=True)
    
        ## 3. 2레벨 차트
    b2b_box2 = st.selectbox("",sa_team,key='2레벨')
    if b2b_box2 =='전체':
        b2b_class2 = df['분석상품레벨2'].value_counts()
    else:
        b2b_class2 = df.loc[df['SA'] == b2b_box2, '분석상품레벨2'].value_counts()
    b2b_class2_chart = alt.Chart(b2b_class2.reset_index()).mark_bar().encode(
        x=alt.X('index:N', axis=alt.Axis(title='상품 대분류',labelAngle=90,labelLimit=0)),
        y=alt.Y('분석상품레벨2:Q', axis=alt.Axis(title='개수')),
        color=alt.Color('index:N', scale=alt.Scale(range=['grey']), legend=None)
    )
    text = b2b_class2_chart.mark_text(dy=-8).encode(
        text=alt.Text('분석상품레벨2:Q')
    )
    st.altair_chart(b2b_class2_chart+text,use_container_width=True)
    
        ## 4. 3레벨 차트
    b2b_box2 = st.selectbox("",sa_team,key='3레벨')
    if b2b_box2 =='전체':
        b2b_class2 = df['분석상품레벨3'].value_counts()
    else:
        b2b_class2 = df.loc[df['SA'] == b2b_box2, '분석상품레벨3'].value_counts()
    b2b_class2_chart = alt.Chart(b2b_class2.reset_index()).mark_bar().encode(
        x=alt.X('index:N', axis=alt.Axis(title='상품 소분류1',labelAngle=90,labelLimit=0)),
        y=alt.Y('분석상품레벨3:Q', axis=alt.Axis(title='개수')),
        color=alt.Color('index:N', scale=alt.Scale(range=['grey']), legend=None)
    )
    text = b2b_class2_chart.mark_text(dy=-8).encode(
        text=alt.Text('분석상품레벨3:Q')
    )
    st.altair_chart(b2b_class2_chart+text,use_container_width=True)
    
            ## 5. 4레벨 차트
    b2b_box2 = st.selectbox("",sa_team,key='4레벨')
    if b2b_box2 =='전체':
        b2b_class2 = df['분석상품레벨4'].value_counts()
    else:
        b2b_class2 = df.loc[df['SA'] == b2b_box2, '분석상품레벨4'].value_counts()
    b2b_class2_chart = alt.Chart(b2b_class2.reset_index()).mark_bar().encode(
        x=alt.X('index:N', axis=alt.Axis(title='상품 소분류2',labelAngle=90,labelLimit=0)),
        y=alt.Y('분석상품레벨4:Q', axis=alt.Axis(title='개수')),
        color=alt.Color('index:N', scale=alt.Scale(range=['grey']), legend=None)
    )
    text = b2b_class2_chart.mark_text(dy=-8).encode(
        text=alt.Text('분석상품레벨4:Q')
    )
    st.altair_chart(b2b_class2_chart+text,use_container_width=True)
    
            ## 6. 5레벨 차트
    b2b_box2 = st.selectbox("",sa_team,key='5레벨')
    if b2b_box2 =='전체':
        b2b_class2 = df['분석상품레벨5'].value_counts()
    else:
        b2b_class2 = df.loc[df['SA'] == b2b_box2, '분석상품레벨5'].value_counts()
    b2b_class2_chart = alt.Chart(b2b_class2.reset_index()).mark_bar().encode(
        x=alt.X('index:N', axis=alt.Axis(title='상품 소분류3',labelAngle=90,labelLimit=0)),
        y=alt.Y('분석상품레벨5:Q', axis=alt.Axis(title='개수')),
        color=alt.Color('index:N', scale=alt.Scale(range=['grey']), legend=None)
    )
    text = b2b_class2_chart.mark_text(dy=-8).encode(
        text=alt.Text('분석상품레벨5:Q')
    )
    st.altair_chart(b2b_class2_chart+text,use_container_width=True)
    
                ## 7. 6레벨 차트
    b2b_box2 = st.selectbox("",sa_team,key='6레벨')
    if b2b_box2 =='전체':
        b2b_class2 = df['분석상품레벨6'].value_counts()
    else:
        b2b_class2 = df.loc[df['SA'] == b2b_box2, '분석상품레벨6'].value_counts()
    b2b_class2_chart = alt.Chart(b2b_class2.reset_index()).mark_bar().encode(
        x=alt.X('index:N', axis=alt.Axis(title='상품 소분류4',labelAngle=90,labelLimit=0)),
        y=alt.Y('분석상품레벨6:Q', axis=alt.Axis(title='개수')),
        color=alt.Color('index:N', scale=alt.Scale(range=['grey']), legend=None)
    )
    text = b2b_class2_chart.mark_text(dy=-8).encode(
        text=alt.Text('분석상품레벨6:Q')
    )
    st.altair_chart(b2b_class2_chart+text,use_container_width=True)
    
                    ## 9. 판매고객 분류 차트
    b2b_box2 = st.selectbox("",sa_team,key='분류')
    if b2b_box2 =='전체':
        b2b_class2 = df['분류'].value_counts()
    else:
        b2b_class2 = df.loc[df['SA'] == b2b_box2, '분류'].value_counts()
    b2b_class2_chart = alt.Chart(b2b_class2.reset_index()).mark_bar().encode(
        x=alt.X('index:N', axis=alt.Axis(title='고객 분류',labelAngle=90,labelLimit=0)),
        y=alt.Y('분류:Q', axis=alt.Axis(title='개수')),
        color=alt.Color('index:N', legend=None)
    )
    text = b2b_class2_chart.mark_text(dy=-8).encode(
        text=alt.Text('분류:Q')
    )
    st.altair_chart(b2b_class2_chart+text,use_container_width=True)
    
    st.subheader('SA별 최다판매상품')
    b2b_rank = df.groupby('SA')['분류'].apply(lambda x: x.value_counts().index[0]).reset_index()
    b2b_rank['분석상품레벨1'] = b2b_rank['SA'].apply(lambda x: df.loc[df['SA'] == x, '분석상품레벨1'].value_counts().index[0])
    b2b_rank['분석상품레벨2'] = b2b_rank['SA'].apply(lambda x: df.loc[df['SA'] == x, '분석상품레벨2'].value_counts().index[0])
    b2b_rank['분석상품레벨3'] = b2b_rank['SA'].apply(lambda x: df.loc[df['SA'] == x, '분석상품레벨3'].value_counts().index[0])
    b2b_rank['분석상품레벨4'] = b2b_rank['SA'].apply(lambda x: df.loc[df['SA'] == x, '분석상품레벨4'].value_counts().index[0])
    b2b_rank['분석상품레벨5'] = b2b_rank['SA'].apply(lambda x: df.loc[df['SA'] == x, '분석상품레벨5'].value_counts().index[0])
    b2b_rank['분석상품레벨6'] = b2b_rank['SA'].apply(lambda x: df.loc[df['SA'] == x, '분석상품레벨6'].value_counts().index[0])
    b2b_rank = b2b_rank.reset_index(drop=True)

    st.write(b2b_rank)
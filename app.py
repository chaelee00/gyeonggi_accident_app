import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 폰트 경로 지정
font_path = "./fonts/NanumGothic.ttf"
fontprop = fm.FontProperties(fname=font_path)

plt.rcParams['font.family'] = fontprop.get_name()
plt.rcParams['axes.unicode_minus'] = False

import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# CSV 파일 로드 (인코딩 지정)
df = pd.read_csv("북부 사고 다발 지역 데이터.csv", encoding='cp949')

# 제목
st.title("📊 경기 북부 사고 다발 지역 분석")

# 필터 위젯
years = sorted(df['사고년도'].unique())
regions = sorted(df['시군명'].unique())
types = sorted(df['사고유형구분'].unique())

col1, col2, col3 = st.columns(3)
with col1:
    selected_year = st.selectbox("사고 년도", years)
with col2:
    selected_region = st.selectbox("시군명", ["전체"] + regions)
with col3:
    selected_type = st.selectbox("사고 유형", ["전체"] + types)

# 필터 적용
df_filtered = df[df['사고년도'] == selected_year]
if selected_region != "전체":
    df_filtered = df_filtered[df_filtered['시군명'] == selected_region]
if selected_type != "전체":
    df_filtered = df_filtered[df_filtered['사고유형구분'] == selected_type]

# 사고 위치 지도 표시
st.subheader("📍 사고 위치 지도")
if not df_filtered.empty:
    m = folium.Map(location=[df_filtered['위도'].mean(), df_filtered['경도'].mean()], zoom_start=12)
    for _, row in df_filtered.iterrows():
        # 마커 및 발생건수 텍스트 함께 추가
        folium.Marker(
            location=[row['위도'], row['경도']],
            popup=f"{row['사고지역위치명']}<br>발생건수: {row['발생건수']}"
        ).add_to(m)
        
        # 발생건수 숫자를 마커 위에 간단히 텍스트로 표시
        folium.map.Marker(
            [row['위도'], row['경도']],
            icon=folium.DivIcon(html=f"""
                <div style="font-size:10pt; color:crimson; font-weight:bold; text-align:center;">
                    {row['발생건수']}
                </div>
            """)
        ).add_to(m)

    st_folium(m, width=700, height=500)
else:
    st.info("해당 조건에 맞는 데이터가 없습니다.")


# 그래프 그리기
import matplotlib.pyplot as plt

# 전역 폰트 설정 (NanumGothic은 리눅스에서도 호환됨)
plt.rcParams['font.family'] = 'NanumGothic'
plt.rcParams['axes.unicode_minus'] = False

st.subheader("🔥 사고 다발 지역 TOP 5")
top5 = df_filtered.groupby("사고지역위치명")["발생건수"].sum().sort_values(ascending=False).head(5)

if not top5.empty:
    fig, ax = plt.subplots()
    top5.plot(kind='barh', ax=ax, color='crimson')
    ax.set_xlabel("발생건수")
    ax.set_ylabel("사고지역위치명")
    ax.set_title("사고 다발 지역 TOP 5")
    ax.tick_params(labelsize=10)

    for label in ax.get_yticklabels():
        label.set_fontsize(10)

    ax.invert_yaxis()
    st.pyplot(fig)
else:
    st.info("TOP 5 사고 지역 데이터를 표시할 수 없습니다.")


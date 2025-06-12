import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import folium
from streamlit_folium import st_folium
import re

# ✅ 한글 폰트 설정
font_path = "./font/NanumGothic.ttf"
fontprop = fm.FontProperties(fname=font_path)
plt.rcParams['font.family'] = fontprop.get_name()
plt.rcParams['axes.unicode_minus'] = False

# ✅ 데이터 로드
df = pd.read_csv("북부 사고 다발 지역 데이터.csv", encoding='cp949')

# ✅ 앱 제목
st.title("📊 경기 북부 사고 다발 지역 분석")

# ✅ 필터 설정
years = sorted(df['사고년도'].unique())
regions = sorted(df['시군명'].unique())
types = sorted(df['사고유형구분'].unique())

col1, col2, col3 = st.columns(3)
with col1:
    selected_year = st.selectbox("사고 년도", years, key="year")
with col2:
    selected_region = st.selectbox("시군명", ["전체"] + regions, key="region")
with col3:
    selected_type = st.selectbox("사고 유형", ["전체"] + types, key="type")

# ✅ 필터 적용
df_filtered = df[df['사고년도'] == selected_year]
if selected_region != "전체":
    df_filtered = df_filtered[df_filtered['시군명'] == selected_region]
if selected_type != "전체":
    df_filtered = df_filtered[df_filtered['사고유형구분'] == selected_type]

# ✅ 지도 출력
st.subheader("📍 사고 위치 지도")
if not df_filtered.empty:
    m = folium.Map(location=[df_filtered['위도'].mean(), df_filtered['경도'].mean()], zoom_start=12)

    for _, row in df_filtered.iterrows():
        # 간단한 위치 추출
        match = re.search(r'\((.*?)\)', row['사고지역위치명'])
        short_name = match.group(1) if match else row['사고지역위치명'].split()[-1]
        popup_text = f"{short_name} 부근<br>발생건수: {row['발생건수']}"

        folium.Marker(
            location=[row['위도'], row['경도']],
            popup=popup_text
        ).add_to(m)

        folium.map.Marker(
            [row['위도'], row['경도']],
            icon=folium.DivIcon(html=f"""
                <div style='font-size:10pt; color:crimson; font-weight:bold; text-align:center;'>
                    {row['발생건수']}
                </div>
            """)
        ).add_to(m)

    st_folium(m, width=700, height=500)
else:
    st.info("해당 조건에 맞는 데이터가 없습니다.")

# ✅ 그래프 출력
st.subheader("🔥 사고 다발 지역 TOP 5")
top5 = df_filtered.groupby("사고지역위치명")["발생건수"].sum().sort_values(ascending=False).head(5)

if not top5.empty:
    fig, ax = plt.subplots()
    top5.plot(kind='barh', ax=ax, color='crimson')
    ax.set_xlabel("발생건수", fontproperties=fontprop)
    ax.set_ylabel("사고지역위치명", fontproperties=fontprop)
    ax.set_title("사고 다발 지역 TOP 5", fontproperties=fontprop)

    for label in ax.get_yticklabels():
        label.set_fontproperties(fontprop)

    ax.tick_params(labelsize=10)
    ax.invert_yaxis()
    st.pyplot(fig)
else:
    st.info("TOP 5 사고 지역 데이터를 표시할 수 없습니다.")

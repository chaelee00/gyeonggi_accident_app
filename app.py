import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import matplotlib.pyplot as plt


# CSV 파일 로드 (인코딩 지정)
df = pd.read_csv("북부 사고 다발 지역 데이터.csv", encoding='cp949')

# 제목
st.title("\ud6a8\uc790\uc801\uc778 \uacbd\uae30 \ubd81\ubd80 \uc0ac\uace0 \ub2e8\ub2f5 \uc9c0\uc5ed \ud3c9\uac00 \uc704\ube44 \ud648")

# 필터 위젯
years = sorted(df['사고년도'].unique())
regions = sorted(df['시군명'].unique())
types = sorted(df['사고유형구분'].unique())

col1, col2, col3 = st.columns(3)
with col1:
    selected_year = st.selectbox("\uc0ac\uace0 \ub144\ub3c4", years)
with col2:
    selected_region = st.selectbox("\uc2dc\uad70\uba85", ["전체"] + regions)
with col3:
    selected_type = st.selectbox("\uc0ac\uace0 \uc720\ud615", ["전체"] + types)

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
        folium.Marker(
            location=[row['위도'], row['경도']],
            popup=f"{row['사고지역위치명']}\n발생건수: {row['발생건수']}"
        ).add_to(m)
    st_folium(m, width=700, height=500)
else:
    st.info("해당 조건에 맞는 데이터가 없습니다.")


# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'  # Windows 기본 한글 폰트
plt.rcParams['axes.unicode_minus'] = Fal
import matplotlib.pyplot as plt


# 그래프 그리기
top5 = df.groupby("사고지역위치명")["발생건수"].sum().sort_values(ascending=False).head(5)
top5.plot(kind='barh', color='crimson')
plt.xlabel("발생건수")
plt.ylabel("사고지역위치명")
plt.title("사고 다발 지역 TOP 5")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()



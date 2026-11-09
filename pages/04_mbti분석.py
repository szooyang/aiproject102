
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# 기본 설정
st.set_page_config(
    page_title="국가별 MBTI 비율 분석",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 국가별 MBTI 비율 분석")
st.caption("국가를 선택하면 MBTI 16가지 유형별 비율을 확인할 수 있습니다.")

# CSV 파일 경로
BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / "countriesMBTI_16types(8).csv"

# CSV 읽기
@st.cache_data
def load_data(file_path):
    encodings = ["utf-8-sig", "utf-8", "cp949"]

    for encoding in encodings:
        try:
            return pd.read_csv(file_path, encoding=encoding)
        except UnicodeDecodeError:
            continue

    return pd.read_csv(file_path)

if not CSV_PATH.exists():
    st.error("CSV 파일을 찾을 수 없습니다.")
    st.info(
        "app.py와 같은 폴더에 "
        "countriesMBTI_16types(8).csv 파일을 넣어주세요."
    )
    st.stop()

try:
    df = load_data(CSV_PATH)
except Exception as error:
    st.error(f"CSV 파일 읽기 오류: {error}")
    st.stop()

# 데이터 확인
if "Country" not in df.columns:
    st.error("Country 열을 찾을 수 없습니다.")
    st.stop()

mbti_columns = [
    column for column in df.columns
    if column != "Country"
]

if len(mbti_columns) != 16:
    st.warning(
        f"MBTI 열이 {len(mbti_columns)}개입니다. "
        "CSV 파일을 확인해주세요."
    )

# 숫자형으로 변환
for column in mbti_columns:
    df[column] = pd.to_numeric(
        df[column], errors="coerce"
    )

# 국가명 정리
df = df.dropna(subset=["Country"])
df["Country"] = df["Country"].astype(str).str.strip()
df = df[df["Country"] != ""]

# 국가 선택
countries = sorted(df["Country"].unique().tolist())

if not countries:
    st.error("국가 데이터가 없습니다.")
    st.stop()

selected_country = st.selectbox(
    "국가를 선택하세요.",
    countries
)

# 선택한 국가 데이터 추출
country_data = df[
    df["Country"] == selected_country
]

if country_data.empty:
    st.error("선택한 국가의 데이터가 없습니다.")
    st.stop()

country_row = country_data.iloc[0]

# MBTI 데이터 정리 및 백분율 변환
chart_data = pd.DataFrame({
    "MBTI": mbti_columns,
    "비율": [
        country_row[column] * 100
        for column in mbti_columns
    ]
})

chart_data = chart_data.dropna(subset=["비율"])

# 비율이 높은 순서대로 정렬
chart_data = chart_data.sort_values(
    "비율",
    ascending=False
).reset_index(drop=True)

if chart_data.empty:
    st.error("그래프로 표시할 데이터가 없습니다.")
    st.stop()

# 색상 지정
# 1위는 빨간색
# 나머지는 진한 파란색에서 연한 파란색으로
blue_gradient = [
    "#2563EB", "#3478E5", "#4388E8",
    "#5297EA", "#62A5EC", "#72B2EE",
    "#82BFF0", "#92CAF2", "#A2D4F4",
    "#B2DDF5", "#C2E5F7", "#D1ECF9",
    "#DDF1FA", "#E6F5FC", "#EDF8FD"
]

bar_colors = ["#EF4444"]
bar_colors.extend(
    blue_gradient[:len(chart_data) - 1]
)

# 1위 유형 확인
top_mbti = chart_data.iloc[0]["MBTI"]
top_ratio = chart_data.iloc[0]["비율"]

st.subheader(
    f"📊 {selected_country}의 MBTI 유형별 비율"
)

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "가장 높은 MBTI 유형",
        top_mbti
    )

with col2:
    st.metric(
        "1위 유형 비율",
        f"{top_ratio:.2f}%"
    )

# 가로 막대그래프
fig = px.bar(
    chart_data,
    x="비율",
    y="MBTI",
    orientation="h",
    text="비율"
)

fig.update_traces(
    marker_color=bar_colors,
    texttemplate="%{text:.2f}%",
    textposition="outside",
    cliponaxis=False,
    hovertemplate=(
        "<b>%{y}</b><br>"
        "비율: %{x:.2f}%<extra></extra>"
    )
)

fig.update_layout(
    xaxis_title="비율(%)",
    yaxis_title="MBTI 유형",
    yaxis=dict(
        categoryorder="array",
        categoryarray=chart_data["MBTI"].tolist(),
        autorange="reversed"
    ),
    xaxis=dict(
        rangemode="tozero",
        ticksuffix="%"
    ),
    showlegend=False,
    height=650,
    margin=dict(
        l=30,
        r=55,
        t=30,
        b=50
    ),
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(size=13)
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# 데이터 표
with st.expander("📋 MBTI 비율 데이터 보기"):
    display_data = chart_data.copy()

    display_data["비율"] = display_data["비율"].map(
        lambda value: f"{value:.2f}%"
    )

    st.dataframe(
        display_data,
        use_container_width=True,
        hide_index=True
    )

st.caption(
    "※ 원본 데이터에 100을 곱하여 백분율로 표시했습니다. "
    "자료의 조사 대상과 수집 방법에 따라 실제 인구의 "
    "분포와 다를 수 있습니다."
)

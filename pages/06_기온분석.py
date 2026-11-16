
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

# --------------------------------
# 1. 페이지 기본 설정
# --------------------------------
st.set_page_config(
    page_title="월별 기온분석",
    page_icon="🌡️",
    layout="wide"
)

st.title("🌡️ 월별 기온분석")
st.write("월을 선택하면 연도별 최고기온과 최저기온의 변화를 확인할 수 있습니다.")

# --------------------------------
# 2. CSV 파일 불러오기
# --------------------------------
# 현재 파일이 pages 폴더에 있다면 상위 폴더에서 CSV 검색
current_dir = Path(__file__).resolve().parent

if current_dir.name == "pages":
    csv_path = current_dir.parent / "temperature.csv"
else:
    csv_path = current_dir / "temperature.csv"

# 파일이 현재 작업 폴더에 있는 경우도 확인
if not csv_path.exists():
    csv_path = Path.cwd() / "temperature(7).csv"

@st.cache_data
def load_data(file_path):
    # 한글 CSV 인코딩: cp949
    df = pd.read_csv(file_path, encoding="cp949")

    # 날짜 데이터 분리
    df["월영문"] = df["일시"].str.split("-").str[0]
    df["연도두자리"] = pd.to_numeric(
        df["일시"].str.split("-").str[1],
        errors="coerce"
    )

    # 월 이름을 숫자로 변환
    month_dict = {
        "Jan": 1, "Feb": 2, "Mar": 3,
        "Apr": 4, "May": 5, "Jun": 6,
        "Jul": 7, "Aug": 8, "Sep": 9,
        "Oct": 10, "Nov": 11, "Dec": 12
    }

    df["월"] = df["월영문"].map(month_dict)

    # 중복된 날짜가 처음 다시 등장하는 지점을 찾음
    # 첫 번째 구간: 1907~2006년
    # 두 번째 구간: 2007~2026년
    duplicate_indices = df.index[
        df["일시"].duplicated(keep="first")
    ].tolist()

    if duplicate_indices:
        split_index = duplicate_indices[0]

        first_period = df.index < split_index

        # 첫 번째 구간의 연도 복원
        df.loc[first_period, "연도"] = (
            df.loc[first_period, "연도두자리"].apply(
                lambda y: 1900 + y if y >= 7 else 2000 + y
            )
        )

        # 두 번째 구간의 연도 복원
        df.loc[~first_period, "연도"] = (
            2000 + df.loc[~first_period, "연도두자리"]
        )

    else:
        # 중복 날짜가 없다면 일반적인 2000년대 날짜로 처리
        df["연도"] = 2000 + df["연도두자리"]

    df["연도"] = df["연도"].astype("Int64")

    # 기온 데이터 숫자형으로 변환
    temp_columns = [
        "최고기온(℃)",
        "최저기온(℃)"
    ]

    for col in temp_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


# --------------------------------
# 3. 데이터 불러오기
# --------------------------------
try:
    if not csv_path.exists():
        st.error("temperature(7).csv 파일을 찾을 수 없습니다.")
        st.stop()

    df = load_data(str(csv_path))

except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
    st.stop()


# --------------------------------
# 4. 월 선택
# --------------------------------
month_names = [
    "1월", "2월", "3월", "4월",
    "5월", "6월", "7월", "8월",
    "9월", "10월", "11월", "12월"
]

selected_month = st.selectbox(
    "📅 분석할 월을 선택하세요.",
    options=list(range(1, 13)),
    format_func=lambda x: month_names[x - 1],
    index=0
)

# --------------------------------
# 5. 선택한 월 데이터 추출
# --------------------------------
month_df = df[df["월"] == selected_month].copy()

month_df = month_df.sort_values("연도")

# --------------------------------
# 6. 월별 기온 꺾은선 그래프
# --------------------------------
st.subheader(f"📊 {selected_month}월 기온분석")

fig = go.Figure()

# 최고기온 그래프
fig.add_trace(
    go.Scatter(
        x=month_df["연도"].astype(str),
        y=month_df["최고기온(℃)"],
        mode="lines+markers",
        name="최고기온",
        line=dict(
            color="#FF1493",
            width=3
        ),
        marker=dict(size=6),
        connectgaps=False
    )
)

# 최저기온 그래프
fig.add_trace(
    go.Scatter(
        x=month_df["연도"].astype(str),
        y=month_df["최저기온(℃)"],
        mode="lines+markers",
        name="최저기온",
        line=dict(
            color="#87CEEB",
            width=3
        ),
        marker=dict(size=6),
        connectgaps=False
    )
)

# 그래프 디자인
fig.update_layout(
    title={
        "text": "월별 기온분석",
        "x": 0.5,
        "xanchor": "center"
    },
    xaxis_title="연도",
    yaxis_title="온도(℃)",
    legend_title="기온 구분",
    hovermode="x unified",
    template="plotly_white",
    font=dict(
        family="Malgun Gothic, Apple SD Gothic Neo, Noto Sans CJK KR, sans-serif",
        size=13
    ),
    height=550,
    xaxis=dict(
        tickangle=-45,
        dtick=5
    ),
    yaxis=dict(
        showgrid=True,
        zeroline=True
    )
)

fig.update_traces(
    hovertemplate="%{x}년 : %{y:.1f}℃<extra></extra>"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------
# 7. 분석 정보
# --------------------------------
st.divider()

col1, col2 = st.columns(2)

with col1:
    st.metric(
        label="선택한 월",
        value=f"{selected_month}월"
    )

with col2:
    st.metric(
        label="분석 데이터 개수",
        value=f"{len(month_df)}개"
    )

st.caption(
    "※ 기온 결측치는 임의로 채우지 않았으며, "
    "그래프에서 해당 연도의 선이 끊어져 표시될 수 있습니다."
)

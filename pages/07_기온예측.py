
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

from sklearn.linear_model import LinearRegression
from pathlib import Path


# --------------------------------
# 1. 페이지 설정
# --------------------------------

st.set_page_config(
    page_title="월별 평균기온 예측",
    page_icon="🌡️",
    layout="wide"
)

st.title("🌡️ 월별 평균기온 예측")

st.write(
    "과거 기온 데이터를 학습하여 "
    "선형회귀 알고리즘으로 미래의 평균기온을 예측합니다."
)

st.divider()


# --------------------------------
# 2. CSV 파일 불러오기
# --------------------------------

@st.cache_data
def load_data():

    current_dir = Path(__file__).resolve().parent

    # CSV 파일 경로
    paths = [
        current_dir / "temperature.csv",
        current_dir.parent / "temperature.csv",
        Path.cwd() / "temperature.csv"
    ]

    file_path = None

    for path in paths:
        if path.exists():
            file_path = path
            break

    if file_path is None:
        raise FileNotFoundError(
            "temperature.csv 파일을 찾을 수 없습니다."
        )

    # 한글 인코딩 처리
    try:
        data = pd.read_csv(
            file_path,
            encoding="utf-8-sig"
        )
    except UnicodeDecodeError:
        data = pd.read_csv(
            file_path,
            encoding="cp949"
        )

    return data


try:
    df = load_data()

except Exception as e:
    st.error(f"데이터를 불러오지 못했습니다: {e}")
    st.stop()


# --------------------------------
# 3. 날짜 및 기온 데이터 처리
# --------------------------------

# 날짜 형식: Oct-07, Jan-08 등 처리

month_dict = {
    "Jan": 1,
    "Feb": 2,
    "Mar": 3,
    "Apr": 4,
    "May": 5,
    "Jun": 6,
    "Jul": 7,
    "Aug": 8,
    "Sep": 9,
    "Oct": 10,
    "Nov": 11,
    "Dec": 12
}


def convert_date(value):

    try:
        parts = str(value).strip().split("-")

        if len(parts) == 2:

            month_name = parts[0].title()
            short_year = int(parts[1])

            if month_name in month_dict:

                if short_year <= 69:
                    year = 2000 + short_year
                else:
                    year = 1900 + short_year

                month = month_dict[month_name]

                return pd.Timestamp(
                    year=year,
                    month=month,
                    day=1
                )

    except (ValueError, TypeError):
        pass

    return pd.to_datetime(
        value,
        errors="coerce"
    )


# 날짜 변환
df["날짜"] = df["일시"].apply(convert_date)

# 연도와 월 추출
df["연도"] = df["날짜"].dt.year
df["월"] = df["날짜"].dt.month

# 평균기온 숫자 변환
df["평균기온(℃)"] = pd.to_numeric(
    df["평균기온(℃)"],
    errors="coerce"
)

# 결측치 제거
df = df.dropna(
    subset=[
        "날짜",
        "연도",
        "월",
        "평균기온(℃)"
    ]
)


# --------------------------------
# 4. 실제 데이터 2025년까지만 사용
# --------------------------------

df = df[df["연도"] <= 2025].copy()

df = df.sort_values("날짜")

if df.empty:
    st.error("2025년까지의 기온 데이터가 없습니다.")
    st.stop()


min_year = int(df["연도"].min())
max_year = int(df["연도"].max())


# --------------------------------
# 5. 사용자 입력
# --------------------------------

st.subheader("📌 예측 조건 선택")

col1, col2 = st.columns(2)

with col1:

    month = st.selectbox(
        "분석할 월을 선택하세요.",
        options=list(range(1, 13)),
        format_func=lambda x: f"{x}월",
        index=10
    )


with col2:

    predict_year = st.number_input(
        "예측할 연도를 입력하세요.",
        min_value=max_year + 1,
        max_value=2100,
        value=max_year + 1,
        step=1
    )

predict_year = int(predict_year)


# --------------------------------
# 6. 선택한 월의 데이터 추출
# --------------------------------

month_data = df[
    df["월"] == month
].copy()

month_data = month_data.sort_values("연도")

if len(month_data) < 2:

    st.error(
        "선택한 월의 데이터가 2개 이상 필요합니다."
    )

    st.stop()


# 학습 데이터
X = month_data[["연도"]]

y = month_data["평균기온(℃)"]


# --------------------------------
# 7. 선형회귀 모델 학습
# --------------------------------

model = LinearRegression()

model.fit(X, y)


# --------------------------------
# 8. 미래 기온 예측
# --------------------------------

prediction_data = pd.DataFrame({
    "연도": [predict_year]
})

prediction = model.predict(
    prediction_data
)[0]


# 기울기와 절편
slope = model.coef_[0]

intercept = model.intercept_


# --------------------------------
# 9. 실제 데이터 범위의 회귀선 생성
# --------------------------------

# 회귀선은 실제 데이터가 존재하는 기간까지만 표시

actual_min_year = int(
    month_data["연도"].min()
)

actual_max_year = int(
    month_data["연도"].max()
)

line_years = np.arange(
    actual_min_year,
    actual_max_year + 1
)

line_predictions = model.predict(
    pd.DataFrame({
        "연도": line_years
    })
)


# --------------------------------
# 10. 예측 결과 표시
# --------------------------------

st.divider()

st.subheader(
    f"🌡️ {month}월 평균기온 예측 결과"
)

result1, result2, result3 = st.columns(3)

with result1:

    st.metric(
        "예측 연도",
        f"{predict_year}년"
    )

with result2:

    st.metric(
        "예측 평균기온",
        f"{prediction:.2f} ℃"
    )

with result3:

    st.metric(
        "학습 데이터 개수",
        f"{len(month_data)}개"
    )


# --------------------------------
# 11. 그래프 시각화
# --------------------------------

fig = go.Figure()


# 실제 평균기온 데이터
fig.add_trace(
    go.Scatter(
        x=month_data["연도"],
        y=month_data["평균기온(℃)"],
        mode="markers",
        name="실제 평균기온",
        marker=dict(
            color="royalblue",
            size=9
        ),
        hovertemplate=
        "%{x}년<br>"
        "평균기온: %{y:.1f}℃"
        "<extra></extra>"
    )
)


# 선형회귀 추세선
fig.add_trace(
    go.Scatter(
        x=line_years,
        y=line_predictions,
        mode="lines",
        name="선형회귀 추세선",
        line=dict(
            color="red",
            width=3
        ),
        hovertemplate=
        "%{x}년<br>"
        "회귀 예측: %{y:.2f}℃"
        "<extra></extra>"
    )
)


# 미래 예측 기온
fig.add_trace(
    go.Scatter(
        x=[predict_year],
        y=[prediction],
        mode="markers",
        name="미래 예측 기온",
        marker=dict(
            color="red",
            size=17,
            symbol="star"
        ),
        hovertemplate=
        "%{x}년<br>"
        "예측 기온: %{y:.2f}℃"
        "<extra></extra>"
    )
)


# 실제 데이터 마지막 연도 표시
fig.add_vline(
    x=actual_max_year,
    line_dash="dash",
    line_color="gray",
    annotation_text="실제 데이터 마지막 연도",
    annotation_position="top left"
)


# 그래프 설정
fig.update_layout(
    title=f"{month}월 평균기온 및 선형회귀 예측",
    xaxis_title="연도",
    yaxis_title="평균기온 (℃)",
    template="plotly_white",
    hovermode="closest",
    height=550,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="center",
        x=0.5
    )
)


st.plotly_chart(
    fig,
    use_container_width=True
)


# --------------------------------
# 12. 선형회귀 알고리즘 설명
# --------------------------------

st.divider()

st.subheader("📖 선형회귀 알고리즘 이해하기")


st.markdown("""
### ① 선형회귀란?

선형회귀는 과거 데이터의 전체적인 변화 경향을 분석하여
가장 적합한 직선을 찾고, 그 직선을 이용해
미래의 값을 예측하는 알고리즘입니다.

### ② 그래프는 어떻게 만들어질까요?

1. 파란색 점은 과거 각 연도의 실제 평균기온입니다.
2. 알고리즘은 파란색 점들을 가장 잘 설명하는 직선을 찾습니다.
3. 빨간색 선이 바로 선형회귀 알고리즘이 찾은 직선입니다.
4. 이 직선을 이용하여 미래 연도의 평균기온을 예측합니다.
5. 빨간색 별표가 사용자가 선택한 연도의 예측 기온입니다.

### ③ 선형회귀의 핵심 원리

선형회귀는 실제 데이터 점과 직선 사이의
세로 방향 거리인 오차를 제곱하여 모두 더한 값이
가장 작아지도록 직선을 찾습니다.

즉, 여러 데이터 점을 종합하여
전체적인 경향을 가장 잘 나타내는 직선을 찾는 것입니다.

### ④ 선형회귀의 예측 공식

예측값 = 기울기 × 연도 + 절편

- 기울기: 연도가 1년 증가할 때 기온이 얼마나 변하는지 나타냅니다.
- 절편: 직선의 위치를 결정합니다.
- 예측값: 직선에 예측 연도를 대입하여 계산한 기온입니다.
""")


# --------------------------------
# 13. 학습된 선형회귀 모델 정보
# --------------------------------

st.subheader("🔍 선형회귀 학습 결과")

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "기울기",
        f"{slope:.4f}"
    )

with col2:

    st.metric(
        "절편",
        f"{intercept:.2f}"
    )


st.info(
    f"이번 분석의 회귀식은 "
    f"평균기온 = {slope:.4f} × 연도 + "
    f"({intercept:.2f}) 입니다."
)


# --------------------------------
# 14. 예측 결과 안내
# --------------------------------

st.divider()

if predict_year > actual_max_year:

    st.warning(
        "미래 예측은 과거의 선형적인 변화 경향이 "
        "앞으로도 유지된다고 가정한 결과입니다. "
        "실제 기온은 기후 변화, 이상기온 등 "
        "다양한 요인에 따라 달라질 수 있습니다."
    )


# --------------------------------
# 15. 과거 데이터 확인
# --------------------------------

with st.expander("📊 선택한 월의 과거 데이터 확인"):

    show_data = month_data[
        ["연도", "평균기온(℃)"]
    ].copy()

    st.dataframe(
        show_data,
        use_container_width=True,
        hide_index=True
    )


# --------------------------------
# 16. 데이터 정보
# --------------------------------

st.caption(
    f"분석 기간: {min_year}년 ~ {max_year}년 | "
    "실제 데이터 기준: 2025년까지 | "
    "알고리즘: Scikit-learn LinearRegression"
)

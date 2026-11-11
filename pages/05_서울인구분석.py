
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
import re

# ==========================================
# 1. 페이지 설정
# ==========================================

st.set_page_config(
    page_title="연령별 인구 분석",
    page_icon="📊",
    layout="wide"
)

st.title("📊 서울시 연령별 인구 분석")
st.write("행정구역, 연도, 성별을 선택하여 연령별 인구를 분석해 보세요.")

# ==========================================
# 2. CSV 파일 경로 설정 및 불러오기
# ==========================================

@st.cache_data
def load_data():

    # 현재 py 파일이 있는 pages 폴더의 상위 폴더
    base_path = Path(__file__).resolve().parent.parent

    # 상위 폴더에 있는 CSV 파일
    file_path = base_path / "population.csv"

    if not file_path.exists():
        raise FileNotFoundError(
            f"CSV 파일을 찾을 수 없습니다.\n경로: {file_path}"
        )

    # 한글 인코딩 처리
    for encoding in ["euc-kr", "cp949", "utf-8-sig", "utf-8"]:
        try:
            data = pd.read_csv(
                file_path,
                encoding=encoding
            )
            return data

        except UnicodeDecodeError:
            continue

    raise ValueError("CSV 파일의 인코딩을 확인해 주세요.")


try:
    df = load_data()

except Exception as e:
    st.error(f"데이터를 불러오지 못했습니다: {e}")
    st.stop()


# ==========================================
# 3. 데이터 전처리
# ==========================================

# 첫 번째 열은 행정구역 정보이므로 제외
for col in df.columns[1:]:

    df[col] = pd.to_numeric(
        df[col].astype(str).str.replace(",", "", regex=False),
        errors="coerce"
    )


# 행정구역 이름 정리
def get_district_name(name):

    match = re.search(
        r"서울특별시\s*(.*?)\s*\(",
        str(name)
    )

    if match:
        district = match.group(1).strip()

        if district == "":
            return "서울특별시 전체"

        return district

    return str(name)


df["자치구"] = df["행정구역"].apply(get_district_name)


# ==========================================
# 4. 행정구역, 연도, 성별 선택
# ==========================================

st.subheader("🔎 분석 조건 선택")

col1, col2, col3 = st.columns(3)

with col1:

    district_list = df["자치구"].tolist()

    selected_district = st.selectbox(
        "① 행정구역 선택",
        district_list
    )

with col2:

    years = sorted(
        set(
            re.findall(r"(\d{4})년_", " ".join(df.columns))
        )
    )

    if not years:
        st.error("연도 열을 찾을 수 없습니다.")
        st.stop()

    selected_year = st.selectbox(
        "② 연도 선택",
        years,
        index=len(years) - 1
    )

with col3:

    selected_gender = st.selectbox(
        "③ 성별 선택",
        ["전체", "남자", "여자"]
    )


# ==========================================
# 5. 성별에 따른 열 이름 설정
# ==========================================

if selected_gender == "전체":

    gender_prefix = "거주자"

elif selected_gender == "남자":

    gender_prefix = "남_거주자"

else:

    gender_prefix = "여_거주자"


# ==========================================
# 6. 연령별 인구 데이터 추출
# ==========================================

age_columns = []

prefix = f"{selected_year}년_{gender_prefix}_"

for col in df.columns:

    if col.startswith(prefix):

        age = col.replace(prefix, "")

        if re.fullmatch(
            r"\d+~\d+세|100세 이상",
            age
        ):

            age_columns.append((age, col))


# 연령 순서대로 정렬
def age_sort(age):

    if age == "100세 이상":
        return 100

    return int(age.split("~")[0])


age_columns.sort(key=lambda x: age_sort(x[0]))


# ==========================================
# 7. 선택한 행정구역 데이터 가져오기
# ==========================================

selected_data = df[
    df["자치구"] == selected_district
]

if selected_data.empty:

    st.error("선택한 행정구역의 데이터가 없습니다.")
    st.stop()

selected_data = selected_data.iloc[0]


# ==========================================
# 8. 그래프 데이터 생성
# ==========================================

chart_data = []

for age, col in age_columns:

    value = selected_data[col]

    chart_data.append({
        "연령": age,
        "인구수": value
    })


chart_df = pd.DataFrame(chart_data)

# 결측치 제거
chart_df = chart_df.dropna(
    subset=["인구수"]
)

if chart_df.empty:

    st.warning("분석할 인구 데이터가 없습니다.")
    st.stop()


# ==========================================
# 9. 분석 조건 표시
# ==========================================

st.divider()

st.subheader("📈 연령별 인구 분석 결과")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "행정구역",
        selected_district
    )

with col2:
    st.metric(
        "분석 연도",
        selected_year + "년"
    )

with col3:
    st.metric(
        "성별",
        selected_gender
    )


# ==========================================
# 10. 초록색 꺾은선 그래프
# ==========================================

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=chart_df["연령"],
        y=chart_df["인구수"],
        mode="lines+markers",
        name="인구수",

        line=dict(
            color="green",
            width=3
        ),

        marker=dict(
            color="green",
            size=8
        ),

        hovertemplate=
        "%{x}<br>인구수: %{y:,.0f}명<extra></extra>"
    )
)


# 그래프 디자인
fig.update_layout(

    title=dict(
        text=f"{selected_district} {selected_year}년 {selected_gender} 연령별 인구",
        x=0.5
    ),

    xaxis=dict(
        title="나이",
        type="category"
    ),

    yaxis=dict(
        title="인구수 (명)",

        rangemode="tozero",

        # 숫자 눈금은 10,000명 단위
        dtick=10000,

        # 보조 구분선은 1,000명 단위
        minor=dict(
            dtick=1000,
            showgrid=True,
            gridcolor="rgba(0, 128, 0, 0.15)",
            gridwidth=1
        ),

        tickformat=",",

        showgrid=True,
        gridcolor="lightgray"
    ),

    hovermode="x unified",

    height=550,

    plot_bgcolor="white",

    margin=dict(
        l=60,
        r=30,
        t=80,
        b=60
    ),

    showlegend=False
)


# 그래프 화면 출력
st.plotly_chart(
    fig,
    use_container_width=True
)


# ==========================================
# 11. 연령별 데이터 표
# ==========================================

with st.expander("📋 연령별 인구 데이터 확인하기"):

    display_df = chart_df.copy()

    display_df["인구수"] = display_df["인구수"].map(
        lambda x: f"{x:,.0f}명"
    )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )


# ==========================================
# 12. CSV 다운로드
# ==========================================

csv_data = chart_df.to_csv(
    index=False,
    encoding="utf-8-sig"
)

st.download_button(
    label="📥 분석 결과 CSV 다운로드",

    data=csv_data,

    file_name=f"{selected_district}_{selected_year}_{selected_gender}_인구분석.csv",

    mime="text/csv"
)


st.divider()

st.caption(
    "서울시 인구 데이터를 활용한 연령별 인구 분석 프로그램입니다."
)

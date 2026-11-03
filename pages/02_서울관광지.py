
import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(
    page_title="Seoul Travel Map",
    page_icon="🗺️",
    layout="wide"
)

# ----------------------------------
# 1. 관광지 데이터
# ----------------------------------

places = [
    {
        "name": "명동",
        "english": "Myeongdong",
        "category": "쇼핑 · 먹거리",
        "lat": 37.5636, "lon": 126.9850,
        "description": "화장품 매장과 패션 상점, 길거리 음식이 모여 있는 서울 대표 쇼핑 거리입니다. 다양한 먹거리와 활기찬 거리 분위기를 즐길 수 있습니다.",
        "tip": "저녁 시간에는 길거리 음식과 야간 분위기를 함께 즐겨 보세요."
    },
    {
        "name": "N서울타워",
        "english": "N Seoul Tower",
        "category": "전망 · 야경",
        "lat": 37.5512, "lon": 126.9882,
        "description": "남산에 자리한 서울의 대표 전망 명소입니다. 전망대에서 서울 도심을 넓게 바라볼 수 있으며 야경과 사랑의 자물쇠로도 유명합니다.",
        "tip": "해 질 무렵 방문하면 낮 풍경과 야경을 모두 감상할 수 있습니다."
    },
    {
        "name": "코엑스 · 별마당도서관",
        "english": "COEX & Starfield Library",
        "category": "쇼핑 · 문화",
        "lat": 37.5116, "lon": 127.0593,
        "description": "대형 쇼핑·전시 공간인 코엑스 안에 있는 별마당도서관은 높은 책장과 개방적인 실내 공간으로 잘 알려져 있습니다.",
        "tip": "쇼핑, 식사, 전시 관람을 한곳에서 즐기기 좋습니다."
    },
    {
        "name": "강남역 일대",
        "english": "Gangnam Station Area",
        "category": "쇼핑 · 도시문화",
        "lat": 37.4979, "lon": 127.0276,
        "description": "상점과 음식점, 카페가 밀집한 번화가입니다. 현대적인 서울의 거리 풍경과 한국의 유행 문화를 경험하기 좋습니다.",
        "tip": "지하상가와 큰길 주변 상점을 함께 둘러보세요."
    },
    {
        "name": "홍대거리",
        "english": "Hongdae",
        "category": "공연 · 거리문화",
        "lat": 37.5563, "lon": 126.9236,
        "description": "젊은 예술가와 공연 문화로 유명한 거리입니다. 거리 공연, 개성 있는 상점, 카페와 음식점이 많아 활기찬 분위기를 느낄 수 있습니다.",
        "tip": "주말 저녁에는 거리 공연과 다양한 볼거리가 많습니다."
    },
    {
        "name": "경복궁",
        "english": "Gyeongbokgung Palace",
        "category": "역사 · 전통문화",
        "lat": 37.5796, "lon": 126.9770,
        "description": "조선 왕조의 중심 궁궐로, 웅장한 전각과 아름다운 정원을 통해 한국의 전통 건축과 역사를 살펴볼 수 있습니다.",
        "tip": "한복을 입고 방문하면 특별한 추억과 사진을 남길 수 있습니다."
    },
    {
        "name": "북촌한옥마을",
        "english": "Bukchon Hanok Village",
        "category": "전통 · 골목길",
        "lat": 37.5826, "lon": 126.9830,
        "description": "전통 한옥이 모여 있는 마을로, 서울의 옛 주거 모습과 골목 풍경을 만날 수 있습니다. 실제 주민이 거주하는 생활 공간이기도 합니다.",
        "tip": "주민 생활을 배려해 조용히 관람하고 안내 표지를 따라 주세요."
    },
    {
        "name": "동대문디자인플라자(DDP)",
        "english": "Dongdaemun Design Plaza",
        "category": "건축 · 디자인",
        "lat": 37.5669, "lon": 127.0095,
        "description": "독특한 곡선 형태의 건축물로 유명한 복합문화공간입니다. 전시와 행사, 디자인 관련 공간을 둘러볼 수 있습니다.",
        "tip": "건물 외관과 주변 조명은 밤에도 멋진 사진을 남기기 좋습니다."
    },
    {
        "name": "광장시장",
        "english": "Gwangjang Market",
        "category": "전통시장 · 음식",
        "lat": 37.5700, "lon": 126.9997,
        "description": "오랜 역사를 지닌 전통시장으로 빈대떡, 마약김밥, 육회 등 다양한 한국 음식을 맛볼 수 있습니다.",
        "tip": "점심시간에는 사람이 많을 수 있으니 여유 있게 방문하세요."
    },
    {
        "name": "남대문시장",
        "english": "Namdaemun Market",
        "category": "전통시장 · 쇼핑",
        "lat": 37.5592, "lon": 126.9777,
        "description": "의류와 잡화, 생활용품, 먹거리를 판매하는 대규모 전통시장입니다. 한국의 일상적인 시장 문화를 경험하기 좋습니다.",
        "tip": "골목마다 판매 품목이 다르므로 천천히 둘러보세요."
    }
]

# ----------------------------------
# 2. 앱 제목
# ----------------------------------

st.title("🗺️ 외국인이 사랑하는 서울 여행 명소 10")

st.caption(
    "서울의 대표 관광지를 지도에서 찾아보고, "
    "각 장소의 특징을 확인해 보세요."
)

st.info(
    "서울의 대표 관광 명소를 선정한 목록입니다. "
    "공식적인 외국인 관광지 방문 순위 1~10위는 아닙니다."
)

# ----------------------------------
# 3. 서울 지도 만들기
# ----------------------------------

seoul_map = folium.Map(
    location=[37.5665, 126.9780],
    zoom_start=12,
    tiles="OpenStreetMap",
    control_scale=True
)

# ----------------------------------
# 4. 지도에 관광지 표시
# ----------------------------------

for number, place in enumerate(places, start=1):

    popup_html = f"""
    <div style="width:220px; font-family:Arial,sans-serif;">
        <b>{number}. {place['name']}</b><br>
        <span style="color:#666;">
            {place['english']}
        </span><br>
        <small>{place['category']}</small>
    </div>
    """

    marker_html = f"""
    <div style="
        background:#e53935;
        color:white;
        border:2px solid white;
        border-radius:50%;
        width:30px;
        height:30px;
        line-height:26px;
        text-align:center;
        font-weight:bold;
        font-size:14px;
        box-shadow:0 1px 5px rgba(0,0,0,0.45);
    ">{number}</div>
    """

    folium.Marker(
        location=[place["lat"], place["lon"]],
        tooltip=f"{number}. {place['name']}",
        popup=folium.Popup(
            popup_html,
            max_width=260
        ),
        icon=folium.DivIcon(
            html=marker_html,
            icon_size=(30, 30),
            icon_anchor=(15, 15)
        )
    ).add_to(seoul_map)

# 관광지 전체가 보이도록 지도 범위 설정
seoul_map.fit_bounds(
    [[p["lat"], p["lon"]] for p in places],
    padding=(25, 25)
)

# ----------------------------------
# 5. 지도 화면에 출력
# ----------------------------------

st.subheader("📍 서울 관광지 위치")

st.caption(
    "지도 위의 빨간색 숫자를 누르면 "
    "관광지 이름을 확인할 수 있습니다."
)

st_folium(
    seoul_map,
    height=600,
    use_container_width=True,
    returned_objects=[]
)

# ----------------------------------
# 6. 관광지 설명
# ----------------------------------

st.divider()

st.subheader("✨ 관광지 알아보기")

st.write("번호는 지도에 표시된 번호와 같습니다.")

# 2열로 관광지 설명 표시
for start in range(0, len(places), 2):

    cols = st.columns(2)

    for col_index, place_index in enumerate(
        range(start, min(start + 2, len(places)))
    ):

        place = places[place_index]
        number = place_index + 1

        with cols[col_index]:

            with st.container(border=True):

                st.markdown(
                    f"### {number}. {place['name']}"
                )

                st.caption(
                    f"{place['english']} · {place['category']}"
                )

                st.write(place["description"])

                st.markdown(
                    f"💡 **여행 팁:** {place['tip']}"
                )

                map_url = (
                    "https://www.google.com/maps/search/"
                    f"?api=1&query={place['lat']},{place['lon']}"
                )

                st.link_button(
                    "구글 지도에서 위치 보기",
                    map_url,
                    use_container_width=True
                )

# ----------------------------------
# 7. 하단 안내
# ----------------------------------

st.divider()

st.caption(
    "※ 지도는 OpenStreetMap을 사용하므로 "
    "인터넷 연결이 필요합니다."
)

st.caption(
    "※ 좌표는 대표 위치이며, "
    "운영 시간과 휴무일은 방문 전 확인하세요."
)


import streamlit as st

# ---------------------------------------
# 1. 페이지 기본 설정
# ---------------------------------------
st.set_page_config(
    page_title="MBTI 진로 탐험소",
    page_icon="🚀",
    layout="wide"
)

# ---------------------------------------
# 2. MBTI별 진로 데이터
# ---------------------------------------
career_data = {
    "ISTJ": {
        "nickname": "청렴결백한 논리주의자",
        "emoji": "📊",
        "intro": "꼼꼼하고 책임감이 강한 현실적인 계획가!",
        "strength": "체계적인 업무 처리, 분석력, 성실함",
        "careers": [
            {
                "name": "회계사",
                "emoji": "💰",
                "major": "회계학과, 경영학과, 세무학과",
                "personality": "숫자를 정확하게 다루고 규칙과 원칙을 중요하게 생각하는 사람",
                "salary": "약 5,000만~9,000만 원",
                "work": "기업의 재무 상태를 분석하고 회계 장부와 재무제표를 검토해요."
            },
            {
                "name": "데이터 분석가",
                "emoji": "📈",
                "major": "통계학과, 데이터사이언스학과, 컴퓨터공학과",
                "personality": "자료를 꼼꼼하게 살펴보고 논리적으로 문제를 해결하는 사람",
                "salary": "약 3,500만~6,000만 원",
                "work": "다양한 데이터를 분석해 기업이 더 나은 결정을 내리도록 도와요."
            }
        ]
    },
    "ISFJ": {
        "nickname": "용감한 수호자",
        "emoji": "🛡️",
        "intro": "따뜻한 마음과 책임감으로 주변을 챙기는 배려왕!",
        "strength": "배려심, 성실함, 꼼꼼함",
        "careers": [
            {
                "name": "간호사",
                "emoji": "🩺",
                "major": "간호학과",
                "personality": "다른 사람을 세심하게 돌보고 책임감 있게 행동하는 사람",
                "salary": "약 3,500만~5,500만 원",
                "work": "환자의 건강 상태를 살피고 치료와 회복 과정을 도와요."
            },
            {
                "name": "초등학교 교사",
                "emoji": "🍎",
                "major": "초등교육과",
                "personality": "아이들을 좋아하고 인내심과 따뜻한 소통 능력을 가진 사람",
                "salary": "약 3,500만~6,000만 원",
                "work": "초등학생에게 다양한 교과를 가르치고 올바른 성장을 도와요."
            }
        ]
    },
    "INFJ": {
        "nickname": "선의의 옹호자",
        "emoji": "🌱",
        "intro": "사람의 마음을 잘 이해하고 더 나은 세상을 꿈꾸는 이상주의자!",
        "strength": "공감 능력, 통찰력, 창의적인 사고",
        "careers": [
            {
                "name": "심리상담사",
                "emoji": "💬",
                "major": "심리학과, 상담심리학과",
                "personality": "다른 사람의 이야기를 잘 들어주고 감정을 이해하는 사람",
                "salary": "약 2,800만~4,500만 원",
                "work": "사람들의 고민을 듣고 마음의 어려움을 해결하도록 도와요."
            },
            {
                "name": "작가",
                "emoji": "✍️",
                "major": "국어국문학과, 문예창작학과",
                "personality": "생각이 깊고 상상력이 풍부하며 자신의 생각을 글로 표현하는 사람",
                "salary": "약 2,500만~5,000만 원",
                "work": "소설, 에세이, 시나리오 등 다양한 글을 창작해요."
            }
        ]
    },
    "INTJ": {
        "nickname": "용의주도한 전략가",
        "emoji": "♟️",
        "intro": "큰 그림을 보고 치밀하게 계획하는 전략의 달인!",
        "strength": "전략적 사고, 독립성, 분석력",
        "careers": [
            {
                "name": "소프트웨어 개발자",
                "emoji": "💻",
                "major": "컴퓨터공학과, 소프트웨어학과",
                "personality": "논리적으로 생각하고 복잡한 문제를 해결하는 것을 좋아하는 사람",
                "salary": "약 3,500만~7,000만 원",
                "work": "컴퓨터 프로그램과 웹사이트, 다양한 응용 소프트웨어를 개발해요."
            },
            {
                "name": "경영전략 컨설턴트",
                "emoji": "🧠",
                "major": "경영학과, 경제학과, 산업공학과",
                "personality": "문제를 분석하고 장기적인 목표와 해결 방법을 설계하는 사람",
                "salary": "약 4,000만~8,000만 원",
                "work": "기업의 문제점을 분석하고 성장할 수 있는 전략을 제안해요."
            }
        ]
    },
    "ISTP": {
        "nickname": "만능 재주꾼",
        "emoji": "🔧",
        "intro": "직접 해보고 문제를 해결하는 실전형 해결사!",
        "strength": "실용적인 사고, 관찰력, 문제 해결 능력",
        "careers": [
            {
                "name": "기계공학 기술자",
                "emoji": "⚙️",
                "major": "기계공학과, 자동차공학과",
                "personality": "기계의 작동 원리에 관심이 많고 직접 실험하고 만드는 것을 좋아하는 사람",
                "salary": "약 3,500만~6,000만 원",
                "work": "기계와 장비를 설계하고 성능을 개선하는 일을 해요."
            },
            {
                "name": "항공정비사",
                "emoji": "✈️",
                "major": "항공정비학과, 항공기계과",
                "personality": "세밀한 관찰력과 집중력을 갖추고 기계를 다루는 데 흥미가 있는 사람",
                "salary": "약 3,500만~6,000만 원",
                "work": "항공기가 안전하게 운항할 수 있도록 점검하고 수리해요."
            }
        ]
    },
    "ISFP": {
        "nickname": "호기심 많은 예술가",
        "emoji": "🎨",
        "intro": "감각적이고 자유로운 표현을 즐기는 감성 크리에이터!",
        "strength": "미적 감각, 공감 능력, 유연한 사고",
        "careers": [
            {
                "name": "시각디자이너",
                "emoji": "🖌️",
                "major": "시각디자인학과, 산업디자인학과",
                "personality": "색과 형태에 대한 감각이 뛰어나고 새로운 디자인을 만드는 것을 좋아하는 사람",
                "salary": "약 2,800만~4,500만 원",
                "work": "광고, 포스터, 상품 이미지 등 다양한 시각 자료를 디자인해요."
            },
            {
                "name": "제과제빵사",
                "emoji": "🥐",
                "major": "제과제빵과, 호텔조리학과, 식품영양학과",
                "personality": "섬세한 손재주와 미적 감각을 갖추고 새로운 음식을 만드는 것을 좋아하는 사람",
                "salary": "약 2,500만~4,000만 원",
                "work": "빵과 과자, 디저트를 만들고 새로운 메뉴를 개발해요."
            }
        ]
    },
    "INFP": {
        "nickname": "열정적인 중재자",
        "emoji": "🌈",
        "intro": "자신만의 가치관과 풍부한 상상력을 가진 꿈꾸는 사람!",
        "strength": "창의력, 공감 능력, 풍부한 상상력",
        "careers": [
            {
                "name": "콘텐츠 기획자",
                "emoji": "📱",
                "major": "미디어학과, 광고홍보학과, 문화콘텐츠학과",
                "personality": "새로운 아이디어를 떠올리고 사람들에게 전달하는 것을 좋아하는 사람",
                "salary": "약 3,000만~5,000만 원",
                "work": "사람들이 관심을 가질 만한 영상과 온라인 콘텐츠를 기획해요."
            },
            {
                "name": "일러스트레이터",
                "emoji": "🖍️",
                "major": "회화과, 시각디자인학과, 애니메이션학과",
                "personality": "상상력이 풍부하고 그림으로 자신의 생각과 감정을 표현하는 사람",
                "salary": "약 2,500만~4,500만 원",
                "work": "책, 광고, 상품 등에 활용되는 그림과 삽화를 제작해요."
            }
        ]
    },
    "INTP": {
        "nickname": "논리적인 사색가",
        "emoji": "🔬",
        "intro": "궁금한 것은 끝까지 파고드는 호기심 대장!",
        "strength": "논리력, 탐구심, 분석력",
        "careers": [
            {
                "name": "인공지능 연구원",
                "emoji": "🤖",
                "major": "인공지능학과, 컴퓨터공학과, 수학과",
                "personality": "새로운 기술과 원리를 탐구하고 복잡한 문제를 분석하는 사람",
                "salary": "약 4,000만~8,000만 원",
                "work": "인공지능 기술과 학습 방법을 연구하고 새로운 기술을 개발해요."
            },
            {
                "name": "과학 연구원",
                "emoji": "🧪",
                "major": "물리학과, 화학과, 생명과학과",
                "personality": "끊임없이 질문하고 실험과 관찰을 통해 답을 찾는 사람",
                "salary": "약 3,500만~6,000만 원",
                "work": "자연 현상과 과학 원리를 연구하고 새로운 지식을 발견해요."
            }
        ]
    },
    "ESTP": {
        "nickname": "모험을 즐기는 사업가",
        "emoji": "🔥",
        "intro": "에너지 넘치고 새로운 도전을 즐기는 행동파!",
        "strength": "순발력, 도전 정신, 사교성",
        "careers": [
            {
                "name": "영업 전문가",
                "emoji": "🤝",
                "major": "경영학과, 마케팅학과, 유통학과",
                "personality": "사람들과 대화하는 것을 좋아하고 목표 달성에 적극적인 사람",
                "salary": "약 3,000만~6,000만 원",
                "work": "고객에게 상품과 서비스를 소개하고 판매 활동을 해요."
            },
            {
                "name": "이벤트 기획자",
                "emoji": "🎉",
                "major": "이벤트학과, 광고홍보학과, 관광학과",
                "personality": "활동적이고 현장 대처 능력이 뛰어나며 사람들과 어울리기를 좋아하는 사람",
                "salary": "약 2,800만~4,500만 원",
                "work": "축제, 행사, 공연 등 사람들이 즐길 수 있는 이벤트를 기획하고 운영해요."
            }
        ]
    },
    "ESFP": {
        "nickname": "자유로운 영혼의 연예인",
        "emoji": "🎤",
        "intro": "밝은 에너지로 주변 사람들을 즐겁게 만드는 분위기 메이커!",
        "strength": "표현력, 친화력, 적응력",
        "careers": [
            {
                "name": "방송인",
                "emoji": "📺",
                "major": "방송연예과, 미디어학과, 연극영화과",
                "personality": "표현력이 풍부하고 사람들 앞에서 자신을 드러내는 것을 즐기는 사람",
                "salary": "약 3,000만~6,000만 원",
                "work": "방송과 영상 콘텐츠에 출연하거나 다양한 프로그램을 진행해요."
            },
            {
                "name": "호텔 서비스 전문가",
                "emoji": "🏨",
                "major": "호텔경영학과, 관광학과, 항공서비스학과",
                "personality": "친절하고 사교적이며 사람들에게 즐거운 경험을 제공하는 것을 좋아하는 사람",
                "salary": "약 2,800만~4,500만 원",
                "work": "호텔을 이용하는 고객에게 객실, 식음료, 안내 등의 서비스를 제공해요."
            }
        ]
    },
    "ENFP": {
        "nickname": "재기발랄한 활동가",
        "emoji": "🚀",
        "intro": "새로운 가능성을 발견하고 아이디어를 현실로 만드는 열정가!",
        "strength": "창의력, 소통 능력, 열정",
        "careers": [
            {
                "name": "광고 기획자",
                "emoji": "📢",
                "major": "광고홍보학과, 미디어학과, 경영학과",
                "personality": "독창적인 생각을 즐기고 사람들의 관심을 끄는 아이디어가 풍부한 사람",
                "salary": "약 3,000만~5,500만 원",
                "work": "상품과 브랜드를 알리기 위한 광고와 홍보 전략을 만들어요."
            },
            {
                "name": "여행 기획자",
                "emoji": "🌍",
                "major": "관광학과, 호텔관광학과, 국제관광학과",
                "personality": "새로운 장소와 문화를 좋아하고 사람들과 소통하는 것을 즐기는 사람",
                "salary": "약 2,800만~4,500만 원",
                "work": "여행 상품을 개발하고 고객에게 특별한 여행 경험을 제공해요."
            }
        ]
    },
    "ENTP": {
        "nickname": "뜨거운 논쟁을 즐기는 변론가",
        "emoji": "💡",
        "intro": "기존의 틀을 깨고 새로운 아이디어를 제시하는 혁신가!",
        "strength": "창의력, 논리력, 도전 정신",
        "careers": [
            {
                "name": "창업가",
                "emoji": "🚀",
                "major": "경영학과, 창업학과, 경제학과",
                "personality": "새로운 사업 아이디어를 생각하고 위험을 감수하며 도전하는 사람",
                "salary": "수익에 따라 차이가 매우 큼",
                "work": "새로운 사업을 시작하고 상품이나 서비스를 만들어 시장에 선보여요."
            },
            {
                "name": "제품 기획자",
                "emoji": "📦",
                "major": "산업공학과, 경영학과, 산업디자인학과",
                "personality": "새로운 상품을 구상하고 다양한 의견을 조율하는 것을 좋아하는 사람",
                "salary": "약 3,500만~6,000만 원",
                "work": "고객의 요구를 분석해 새로운 상품과 서비스의 방향을 결정해요."
            }
        ]
    },
    "ESTJ": {
        "nickname": "엄격한 관리자",
        "emoji": "📋",
        "intro": "목표를 정하면 체계적으로 실행하는 책임감 강한 리더!",
        "strength": "리더십, 추진력, 조직 관리 능력",
        "careers": [
            {
                "name": "경영 관리자",
                "emoji": "🏢",
                "major": "경영학과, 경제학과, 행정학과",
                "personality": "조직을 이끌고 목표를 달성하기 위해 계획적으로 행동하는 사람",
                "salary": "약 4,000만~8,000만 원",
                "work": "기업의 업무와 인력을 관리하고 조직의 목표 달성을 이끌어요."
            },
            {
                "name": "공무원",
                "emoji": "🏛️",
                "major": "행정학과, 법학과, 정치외교학과 등",
                "personality": "책임감이 강하고 규칙을 잘 지키며 공공의 이익을 중요하게 생각하는 사람",
                "salary": "직급과 경력에 따라 차이가 있음",
                "work": "국민 생활과 관련된 행정 업무를 수행하고 공공 서비스를 제공해요."
            }
        ]
    },
    "ESFJ": {
        "nickname": "사교적인 외교관",
        "emoji": "💗",
        "intro": "사람들과 함께할 때 더욱 빛나는 따뜻한 협력가!",
        "strength": "협동심, 친화력, 배려심",
        "careers": [
            {
                "name": "인사 담당자",
                "emoji": "👥",
                "major": "경영학과, 심리학과, 행정학과",
                "personality": "사람들의 장점을 잘 발견하고 원활한 관계 형성을 돕는 사람",
                "salary": "약 3,200만~5,500만 원",
                "work": "기업의 채용, 교육, 인사 관리 등 직원과 관련된 업무를 담당해요."
            },
            {
                "name": "사회복지사",
                "emoji": "🤲",
                "major": "사회복지학과, 아동복지학과",
                "personality": "다른 사람을 돕는 데 보람을 느끼고 공감과 소통 능력이 뛰어난 사람",
                "salary": "약 2,800만~4,000만 원",
                "work": "도움이 필요한 사람들에게 상담과 복지 서비스를 제공해요."
            }
        ]
    },
    "ENFJ": {
        "nickname": "정의로운 사회운동가",
        "emoji": "🌟",
        "intro": "사람들의 가능성을 발견하고 함께 성장하도록 돕는 리더!",
        "strength": "의사소통 능력, 공감 능력, 리더십",
        "careers": [
            {
                "name": "교사",
                "emoji": "👩‍🏫",
                "major": "교육학과, 사범대학 관련 학과",
                "personality": "다른 사람의 성장을 돕는 데 보람을 느끼고 설명과 소통을 잘하는 사람",
                "salary": "약 3,500만~6,000만 원",
                "work": "학생들에게 지식을 전달하고 학습과 성장을 이끌어요."
            },
            {
                "name": "기업 교육 전문가",
                "emoji": "🎓",
                "major": "교육학과, 교육공학과, 경영학과",
                "personality": "사람들의 능력을 키우는 데 관심이 많고 교육 프로그램을 기획하는 사람",
                "salary": "약 3,000만~5,500만 원",
                "work": "기업 구성원들의 업무 능력을 높이기 위한 교육을 기획하고 운영해요."
            }
        ]
    },
    "ENTJ": {
        "nickname": "대담한 통솔자",
        "emoji": "👑",
        "intro": "큰 목표를 세우고 사람들을 이끄는 타고난 전략가!",
        "strength": "리더십, 결단력, 목표 지향성",
        "careers": [
            {
                "name": "기업 경영자",
                "emoji": "🏆",
                "major": "경영학과, 경제학과, 산업공학과",
                "personality": "목표 의식이 뚜렷하고 결정을 내리는 데 주저함이 없는 사람",
                "salary": "직급과 기업 규모에 따라 차이가 매우 큼",
                "work": "기업의 방향과 전략을 결정하고 조직 전체를 이끌어요."
            },
            {
                "name": "변호사",
                "emoji": "⚖️",
                "major": "법학과 등 법학전문대학원 진학 관련 전공",
                "personality": "논리적인 사고력과 설득력이 뛰어나며 정의와 원칙을 중요하게 생각하는 사람",
                "salary": "약 5,000만~1억 원 이상",
                "work": "법률 지식을 바탕으로 의뢰인의 권리를 보호하고 법적 문제를 해결해요."
            }
        ]
    }
}

# ---------------------------------------
# 3. 화면 디자인
# ---------------------------------------
st.markdown("""
<style>
    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: 900;
        color: #5B6EE1;
        padding: 10px;
    }
    .sub-title {
        text-align: center;
        font-size: 17px;
        color: #777777;
        margin-bottom: 25px;
    }
    .career-card {
        background-color: #F3F5FF;
        padding: 22px;
        border-radius: 18px;
        border: 1px solid #E0E5FF;
        min-height: 310px;
    }
    .career-name {
        color: #4355B9;
        font-size: 23px;
        font-weight: bold;
        margin-bottom: 12px;
    }
    .info-title {
        font-weight: bold;
        color: #3949AB;
        margin-top: 12px;
    }
    .salary {
        color: #E05B75;
        font-size: 19px;
        font-weight: bold;
    }
    .result-box {
        background-color: #EEF8FF;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 20px;
    }
    @media (prefers-color-scheme: dark) {
        .career-card {
            background-color: #252B42;
            border-color: #454D70;
        }
        .career-name, .info-title {
            color: #AAB7FF;
        }
        .result-box {
            background-color: #202D40;
        }
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------
# 4. 메인 화면
# ---------------------------------------
st.markdown(
    '<div class="main-title">🚀 MBTI 진로 탐험소</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">'
    '나의 성격 유형으로 알아보는 흥미로운 미래 직업!'
    '</div>',
    unsafe_allow_html=True
)

st.markdown("---")

st.markdown("### 🧩 나의 MBTI 유형을 선택해 보세요!")
st.write("16가지 유형 중 나와 가장 가까운 유형을 골라주세요.")

mbti_list = list(career_data.keys())

selected_mbti = st.selectbox(
    "MBTI 선택하기",
    mbti_list,
    format_func=lambda x: (
        career_data[x]["emoji"] + " " + x + " - "
        + career_data[x]["nickname"]
    )
)

# ---------------------------------------
# 5. 선택한 유형 정보 출력
# ---------------------------------------
data = career_data[selected_mbti]

st.markdown("---")

st.markdown(
    f'<div class="result-box">'
    f'<h1>{data["emoji"]} {selected_mbti}</h1>'
    f'<h3>{data["nickname"]}</h3>'
    f'<p>{data["intro"]}</p>'
    f'</div>',
    unsafe_allow_html=True
)

st.markdown("### ✨ 나의 성격 강점")

st.info("💪 " + data["strength"])

st.markdown("---")

st.markdown("## 💼 나에게 추천하는 직업 TOP 2")
st.write("나의 성향과 강점을 참고하여 두 가지 직업을 소개할게요!")

# ---------------------------------------
# 6. 직업 카드 출력
# ---------------------------------------
col1, col2 = st.columns(2)

for col, career in zip([col1, col2], data["careers"]):
    with col:
        st.markdown(
            f"""
            <div class="career-card">
                <div class="career-name">
                    {career["emoji"]} {career["name"]}
                </div>
                <p>{career["work"]}</p>
                <div class="info-title">🎓 관련 학과</div>
                <p>{career["major"]}</p>
                <div class="info-title">🌟 어울리는 성격</div>
                <p>{career["personality"]}</p>
                <div class="info-title">💰 예상 연봉</div>
                <div class="salary">{career["salary"]}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("")

# ---------------------------------------
# 7. 진로 탐색 마무리
# ---------------------------------------
st.markdown("---")

st.markdown("## 🌈 나의 진로 탐험 TIP")

st.success(
    "MBTI는 나의 성격을 이해하는 하나의 참고 자료일 뿐이에요! "
    "MBTI가 같더라도 좋아하는 일과 잘하는 일은 모두 다를 수 있어요."
)

st.markdown("""
**진로를 선택할 때 함께 생각해 보세요!**

- ❤️ 내가 좋아하고 즐겁게 할 수 있는 일은 무엇일까?
- 💪 내가 잘하는 능력은 무엇일까?
- 🔍 내가 더 배우고 싶은 분야는 무엇일까?
- 🚀 미래에 어떤 모습으로 성장하고 싶을까?
""")

st.markdown("---")

st.caption(
    "📌 직업 및 연봉 정보는 진로 탐색을 위한 참고용 추정 범위입니다. "
    "실제 연봉은 경력, 직무, 기업 규모, 근무 지역 등에 따라 달라집니다."
)

st.caption("Made with ❤️ for your future | MBTI 진로 탐험소")

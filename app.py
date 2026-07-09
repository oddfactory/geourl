import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
import json
import plotly.graph_objects as go
from google import genai
from google.genai import types
from urllib.parse import urlparse

# Set page configuration with a modern look
st.set_page_config(
    page_title="AI-SEO & GEO Insight Dashboard",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom premium CSS styling for a sophisticated dark-mode UI
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* Global Font & Background adjustments */
html, body, [data-testid="stAppViewContainer"] {
    background-color: #0b0c10;
    color: #e0e6ed;
    font-family: 'Outfit', sans-serif;
}

[data-testid="stHeader"] {
    background-color: rgba(11, 12, 16, 0.8);
    backdrop-filter: blur(10px);
}

[data-testid="stSidebar"] {
    background-color: #11141c;
    border-right: 1px solid rgba(102, 252, 241, 0.1);
}

/* Titles and Headers */
h1, h2, h3, h4, h5, h6 {
    color: #66fcf1;
    font-family: 'Outfit', sans-serif;
    font-weight: 600;
}

.main-title {
    font-size: 2.8rem;
    font-weight: 700;
    background: linear-gradient(135deg, #66fcf1 0%, #45b3e0 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
    text-align: center;
}

.sub-title {
    font-size: 1.1rem;
    color: #e2e8f0; /* Ultra-bright gray for maximum readability */
    text-align: center;
    margin-bottom: 2.5rem;
}

/* Custom premium container cards */
.custom-card {
    background: #161a23; /* Solid card background for perfect high contrast */
    border: 1px solid rgba(102, 252, 241, 0.3); /* Brighter neon-teal border */
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 20px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    backdrop-filter: blur(8px);
}

.custom-card:hover {
    border-color: rgba(102, 252, 241, 0.6);
    box-shadow: 0 6px 24px rgba(102, 252, 241, 0.15);
    transition: all 0.3s ease;
}

/* Metric displays */
.metric-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
}

.metric-val {
    font-size: 2.5rem;
    font-weight: 700;
    color: #66fcf1;
}

.metric-lbl {
    font-size: 1rem;
    color: #a5f3fc; /* High-contrast soft cyan */
    text-transform: uppercase;
    letter-spacing: 1.5px;
    font-weight: 500;
}

/* Custom Alert Badges */
.status-badge {
    padding: 4px 10px;
    border-radius: 8px;
    font-size: 0.85rem;
    font-weight: 600;
    display: inline-block;
}
.status-pass {
    background-color: rgba(46, 204, 113, 0.15);
    color: #2ecc71;
    border: 1px solid rgba(46, 204, 113, 0.3);
}
.status-warn {
    background-color: rgba(241, 196, 15, 0.15);
    color: #f1c40f;
    border: 1px solid rgba(241, 196, 15, 0.3);
}
.status-fail {
    background-color: rgba(231, 76, 60, 0.15);
    color: #e74c3c;
    border: 1px solid rgba(231, 76, 60, 0.3);
}

/* Section Dividers */
hr {
    border: 0;
    height: 1px;
    background: linear-gradient(to right, rgba(102, 252, 241, 0), rgba(102, 252, 241, 0.3), rgba(102, 252, 241, 0));
    margin: 2rem 0;
}

/* Sidebar Input styling to make them pop out and have clear contrast */
[data-testid="stSidebar"] [data-testid="stTextInput"] input {
    background-color: #1a1f2c !important;
    color: #ffffff !important;
    border: 2px solid #66fcf1 !important;
    border-radius: 8px !important;
    font-size: 1rem !important;
    font-weight: 500 !important;
    box-shadow: 0 0 12px rgba(102, 252, 241, 0.35) !important;
    padding: 10px 12px !important;
    transition: all 0.3s ease !important;
}

[data-testid="stSidebar"] [data-testid="stTextInput"] input:focus {
    border-color: #45b3e0 !important;
    box-shadow: 0 0 16px rgba(69, 179, 224, 0.55) !important;
    background-color: #1e2535 !important;
}

/* Style label text specifically for the API Key inside the sidebar */
[data-testid="stSidebar"] [data-testid="stTextInput"] label,
[data-testid="stSidebar"] [data-testid="stSelectbox"] label {
    color: #66fcf1 !important;
    font-weight: 700 !important;
    font-size: 1.05rem !important;
    margin-bottom: 8px !important;
    letter-spacing: 0.5px !important;
    display: inline-block !important;
}

/* Sidebar Selectbox Custom Style for visibility */
[data-testid="stSidebar"] [data-testid="stSelectbox"] div[data-baseweb="select"] {
    background-color: #1a1f2c !important;
    border: 2px solid rgba(102, 252, 241, 0.6) !important;
    border-radius: 8px !important;
    color: #ffffff !important;
}

[data-testid="stSidebar"] [data-testid="stSelectbox"] div[data-baseweb="select"]:hover {
    border-color: #66fcf1 !important;
}

/* Custom Problem and Action cards based on reference design */
.problem-card {
    display: flex;
    align-items: flex-start;
    background: #161a23 !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 12px !important;
    padding: 16px !important;
    margin-bottom: 14px !important;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3) !important;
    transition: all 0.3s ease !important;
}
.problem-card:hover {
    border-color: rgba(102, 252, 241, 0.5) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(102, 252, 241, 0.15) !important;
}
.problem-badge {
    font-size: 0.95rem !important;
    font-weight: 700 !important;
    padding: 4px 10px !important;
    border-radius: 6px !important;
    margin-right: 14px !important;
    flex-shrink: 0 !important;
    font-family: 'JetBrains Mono', monospace !important;
}
.seo-badge {
    background: rgba(102, 252, 241, 0.15) !important;
    color: #66fcf1 !important;
    border: 1px solid rgba(102, 252, 241, 0.3) !important;
}
.geo-badge {
    background: rgba(168, 85, 247, 0.15) !important;
    color: #c084fc !important;
    border: 1px solid rgba(168, 85, 247, 0.3) !important;
}
.problem-text {
    font-size: 0.92rem !important;
    color: #e2e8f0 !important;
    line-height: 1.65 !important;
}

.action-item {
    display: flex;
    align-items: flex-start;
    padding: 18px !important;
    background: #161a23 !important;
    border-radius: 12px !important;
    margin-bottom: 14px !important;
    border: 1px solid rgba(255, 255, 255, 0.05) !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2) !important;
}
.action-num-badge {
    width: 26px !important;
    height: 26px !important;
    border-radius: 50% !important;
    color: #ffffff !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    font-size: 0.9rem !important;
    font-weight: 700 !important;
    margin-right: 14px !important;
    flex-shrink: 0 !important;
}
.action-content {
    font-size: 0.95rem !important;
    color: #e2e8f0 !important;
    line-height: 1.6 !important;
}
.priority-badge {
    font-size: 0.75rem !important;
    padding: 2px 8px !important;
    border-radius: 4px !important;
    font-weight: 600 !important;
    margin-left: 8px !important;
    display: inline-block !important;
}
.priority-high {
    background: rgba(239, 68, 68, 0.18) !important;
    color: #f87171 !important;
    border: 1px solid rgba(239, 68, 68, 0.35) !important;
}
.priority-medium {
    background: rgba(245, 158, 11, 0.18) !important;
    color: #fbbf24 !important;
    border: 1px solid rgba(245, 158, 11, 0.35) !important;
}
.priority-low {
    background: rgba(16, 185, 129, 0.18) !important;
    color: #34d399 !important;
    border: 1px solid rgba(16, 185, 129, 0.35) !important;
}
</style>
""", unsafe_allow_html=True)

# ----------------- 1. Web Scraper Module -----------------

def parse_html_content(html: str, url: str):
    """
    Parses raw HTML content, extracts primary HTML elements, meta tags, and body text.
    Shared by both the automatic web scraper and the manual HTML paste input mode.
    """
    soup = BeautifulSoup(html, 'html.parser')

    # Basic metadata extraction
    title_tag = soup.find('title')
    title = title_tag.get_text().strip() if title_tag else ""

    meta_desc_tag = (
        soup.find('meta', attrs={'name': re.compile(r'^description$', re.IGNORECASE)}) or
        soup.find('meta', attrs={'property': re.compile(r'^og:description$', re.IGNORECASE)})
    )
    meta_desc = meta_desc_tag.get('content', '').strip() if meta_desc_tag else ""

    # OpenGraph Tags extraction
    og_tags = {}
    for tag in soup.find_all('meta', property=re.compile(r'^og:')):
        prop = tag.get('property', '')
        content = tag.get('content', '')
        if prop and content:
            og_tags[prop] = content

    # Headers structure analysis
    headers_dict = {f"h{i}": [h.get_text().strip() for h in soup.find_all(f"h{i}")] for i in range(1, 7)}

    # Body text processing (excluding scripts, styles, navigations)
    for element in soup(["script", "style", "nav", "footer", "header", "noscript"]):
        element.decompose()
    
    paragraphs = [p.get_text().strip() for p in soup.find_all(['p', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]
    # Filter out empty entries
    paragraphs = [p for p in paragraphs if p]
    body_text = " ".join(paragraphs)

    # Images alt attribute check
    images = soup.find_all('img')
    total_images = len(images)
    missing_alt_images = 0
    for img in images:
        alt = img.get('alt')
        if alt is None or alt.strip() == "":
            missing_alt_images += 1

    # Structured Schema Markup (JSON-LD) extraction
    json_ld_scripts = soup.find_all('script', type='application/ld+json')
    json_ld_parsed = []
    json_ld_raw = []
    
    for script in json_ld_scripts:
        raw_content = script.string
        if raw_content:
            json_ld_raw.append(raw_content.strip())
            try:
                parsed = json.loads(raw_content)
                json_ld_parsed.append(parsed)
            except Exception:
                # Store unparsed strings to indicate formatting error
                json_ld_parsed.append(None)

    return {
        "url": url,
        "title": title,
        "meta_description": meta_desc,
        "og_tags": og_tags,
        "headers": headers_dict,
        "body_text": body_text,
        "total_images": total_images,
        "missing_alt_images": missing_alt_images,
        "json_ld_scripts": json_ld_raw,
        "json_ld_parsed": json_ld_parsed,
        "paragraphs_list": paragraphs
    }


def scrape_url(url: str):
    """
    Scrapes the target URL using highly optimized modern browser headers,
    extracts primary HTML elements, and delegates to parse_html_content.
    Handles network exceptions gracefully and flags 403 Forbidden specifically.
    """
    # Clean the URL input
    url = url.strip()
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Ch-Ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Cache-Control': 'max-age=0'
    }

    try:
        response = requests.get(url, headers=headers, timeout=12)
        response.raise_for_status()
    except requests.exceptions.MissingSchema:
        raise ValueError("올바르지 않은 URL 형식입니다. 프로토콜(http://, https://)을 확인해 주세요.")
    except requests.exceptions.ConnectionError:
        raise ValueError("해당 서버에 연결할 수 없습니다. URL 주소가 정확한지 혹은 오프라인 상태인지 확인해 주세요.")
    except requests.exceptions.Timeout:
        raise ValueError("요청 시간이 초과되었습니다. 웹페이지가 너무 느리거나 차단되었을 수 있습니다.")
    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code
        if status_code == 403:
            raise ValueError("HTTP 403 Forbidden 에러가 발생했습니다. 대상 사이트의 강력한 보안 방화벽(Cloudflare 등)이 자동 차단 기능을 적용한 경우입니다.")
        else:
            raise ValueError(f"HTTP 에러가 발생했습니다: Status Code {status_code}")
    except Exception as e:
        raise ValueError(f"페이지 크롤링 도중 예기치 못한 에러가 발생했습니다: {str(e)}")

    return parse_html_content(response.text, url)


# ----------------- 2. SEO & GEO Scoring Engine -----------------

def calculate_scores(data: dict):
    """
    Computes precise 0-100 scores for SEO and GEO based on parsed website metrics.
    Returns calculated values and diagnostic check-list statuses.
    """
    # Initialize checklist results
    seo_checks = []
    geo_checks = []

    # ----------------- A. SEO SCORE CALCULATION (Max 100) -----------------
    seo_score = 0

    # 1. Title Existence and Length (Max 30 pts)
    title = data["title"]
    title_len = len(title)
    if not title:
        title_pts = 0
        seo_checks.append({
            "category": "메타데이터",
            "item": "Title 태그 존재 여부",
            "status": "FAIL",
            "msg": "Title 태그가 정의되지 않았습니다. 검색 결과에 노출되지 않을 수 있습니다.",
            "value": "없음"
        })
    else:
        title_pts = 20
        if 30 <= title_len <= 60:
            title_pts += 10
            seo_checks.append({
                "category": "메타데이터",
                "item": "Title 태그 길이 최적성",
                "status": "PASS",
                "msg": f"Title의 길이가 이상적입니다 ({title_len}자). 검색 엔진에 정상 노출됩니다.",
                "value": f"{title_len}자"
            })
        elif 15 <= title_len < 30 or 60 < title_len <= 80:
            title_pts += 5
            seo_checks.append({
                "category": "메타데이터",
                "item": "Title 태그 길이 최적성",
                "status": "WARN",
                "msg": f"Title 길이({title_len}자)가 다소 짧거나 깁니다 (추천: 30~60자).",
                "value": f"{title_len}자"
            })
        else:
            title_pts += 2
            seo_checks.append({
                "category": "메타데이터",
                "item": "Title 태그 길이 최적성",
                "status": "FAIL",
                "msg": f"Title이 너무 극단적입니다 ({title_len}자). 요약되거나 누락될 가능성이 큽니다.",
                "value": f"{title_len}자"
            })
    seo_score += title_pts

    # 2. Meta Description Existence and Length (Max 30 pts)
    desc = data["meta_description"]
    desc_len = len(desc)
    if not desc:
        desc_pts = 0
        seo_checks.append({
            "category": "메타데이터",
            "item": "Meta Description 존재 여부",
            "status": "FAIL",
            "msg": "Meta Description이 존재하지 않습니다. 검색 엔진이 임의로 본문을 요약해 노출합니다.",
            "value": "없음"
        })
    else:
        desc_pts = 20
        if 80 <= desc_len <= 160:
            desc_pts += 10
            seo_checks.append({
                "category": "메타데이터",
                "item": "Meta Description 길이 최적성",
                "status": "PASS",
                "msg": f"설명 길이({desc_len}자)가 매우 적절합니다. 스니펫 최적화가 보장됩니다.",
                "value": f"{desc_len}자"
            })
        elif 40 <= desc_len < 80 or 160 < desc_len <= 200:
            desc_pts += 5
            seo_checks.append({
                "category": "메타데이터",
                "item": "Meta Description 길이 최적성",
                "status": "WARN",
                "msg": f"설명 길이({desc_len}자)가 권장치(80~160자)를 약간 벗어납니다.",
                "value": f"{desc_len}자"
            })
        else:
            desc_pts += 2
            seo_checks.append({
                "category": "메타데이터",
                "item": "Meta Description 길이 최적성",
                "status": "FAIL",
                "msg": f"설명이 너무 짧거나 긴 편입니다 ({desc_len}자). 가독성이 떨어집니다.",
                "value": f"{desc_len}자"
            })
    seo_score += desc_pts

    # 3. H1 Heading Appropriateness (Max 20 pts)
    h1s = data["headers"]["h1"]
    h1_count = len(h1s)
    if h1_count == 1:
        h1_pts = 20
        seo_checks.append({
            "category": "콘텐츠 구조",
            "item": "H1 Heading 태그 개수",
            "status": "PASS",
            "msg": "가장 중요한 핵심 주제를 나타내는 H1 태그가 정확히 1개 구성되어 있습니다.",
            "value": "1개"
        })
    elif h1_count > 1:
        h1_pts = 10
        seo_checks.append({
            "category": "콘텐츠 구조",
            "item": "H1 Heading 태그 개수",
            "status": "WARN",
            "msg": f"H1 태그가 {h1_count}개 존재합니다. 페이지당 하나의 독자적 H1 태그 사용을 적극 권장합니다.",
            "value": f"{h1_count}개"
        })
    else:
        h1_pts = 0
        seo_checks.append({
            "category": "콘텐츠 구조",
            "item": "H1 Heading 태그 개수",
            "status": "FAIL",
            "msg": "H1 태그가 아예 없습니다. 검색 엔진이 이 페이지의 메인 헤드라인을 파악하기 어렵습니다.",
            "value": "0개"
        })
    seo_score += h1_pts

    # 4. Image Alt Attribute (Max 20 pts)
    total_imgs = data["total_images"]
    missing_alt = data["missing_alt_images"]
    if total_imgs == 0:
        img_pts = 20
        seo_checks.append({
            "category": "이미지 최적화",
            "item": "이미지 Alt 속성 부여",
            "status": "PASS",
            "msg": "페이지에 이미지가 없어 alt 누락 이슈가 존재하지 않습니다.",
            "value": "이미지 없음"
        })
    else:
        with_alt_count = total_imgs - missing_alt
        ratio = with_alt_count / total_imgs
        img_pts = int(ratio * 20)
        
        if missing_alt == 0:
            seo_checks.append({
                "category": "이미지 최적화",
                "item": "이미지 Alt 속성 부여",
                "status": "PASS",
                "msg": f"모든 이미지({total_imgs}개)에 alt 묘사 속성이 완벽하게 추가되어 있습니다.",
                "value": "100%"
            })
        elif ratio >= 0.7:
            seo_checks.append({
                "category": "이미지 최적화",
                "item": "이미지 Alt 속성 부여",
                "status": "WARN",
                "msg": f"일부 이미지에 alt 속성이 누락되었습니다 ({total_imgs}개 중 {missing_alt}개 누락).",
                "value": f"{int(ratio*100)}%"
            })
        else:
            seo_checks.append({
                "category": "이미지 최적화",
                "item": "이미지 Alt 속성 부여",
                "status": "FAIL",
                "msg": f"이미지 대다수의 alt 속성이 비어 있습니다 ({total_imgs}개 중 {missing_alt}개 누락). 이미지 검색 랭킹에 악영향을 줍니다.",
                "value": f"{int(ratio*100)}%"
            })
    seo_score += img_pts

    # ----------------- B. GEO SCORE CALCULATION (Max 100) -----------------
    geo_score = 0

    # 1. Statistical Data, Numbers & Citations Presence (Max 50 pts)
    body = data["body_text"]
    
    # Check for statistics/numbers
    stat_matches = re.findall(r'\b\d+(?:\.\d+)?%?|\b\d+퍼센트\b|백분율|통계', body)
    # Check for quote marks / citations
    quote_matches = re.findall(r'["\'“‘」」]|따르면|밝혔다|인용|에 의하면|according to|cited|source', body)
    
    stat_density = len(stat_matches)
    quote_density = len(quote_matches)
    
    # Calculate points
    stat_pts = min(20, stat_density * 4) # Max 20 points
    quote_pts = min(30, quote_density * 5) # Max 30 points
    citations_pts = stat_pts + quote_pts
    
    if citations_pts >= 40:
        geo_checks.append({
            "category": "신뢰성 및 인용도",
            "item": "통계 및 외부 자료 인용 밀도",
            "status": "PASS",
            "msg": f"본문 내 수치 데이터(약 {stat_density}회) 및 인용 표현(약 {quote_density}회)이 활발히 쓰였습니다. AI 추천 신뢰도가 매우 높습니다.",
            "value": f"수치 {stat_density} / 인용 {quote_density}"
        })
    elif citations_pts >= 20:
        geo_checks.append({
            "category": "신뢰성 및 인용도",
            "item": "통계 및 외부 자료 인용 밀도",
            "status": "WARN",
            "msg": "본문에 객관적인 통계 수치나 인용 자료 표현이 다소 미흡합니다. 구체적 통계나 권위적 인용을 가미하면 AI 검색 채택율이 증가합니다.",
            "value": f"수치 {stat_density} / 인용 {quote_density}"
        })
    else:
        geo_checks.append({
            "category": "신뢰성 및 인용도",
            "item": "통계 및 외부 자료 인용 밀도",
            "status": "FAIL",
            "msg": "본문에 근거 수치(통계치)나 출처/인용문 등이 전혀 식별되지 않습니다. 주관적이고 입증되지 않은 글로 인식될 여지가 큽니다.",
            "value": "매우 낮음"
        })
    geo_score += citations_pts

    # 2. Readability & Clear Structure (Max 50 pts)
    # Sentence tokenization approximation (splits on periods)
    sentences = [s.strip() for s in re.split(r'[.!?]\s+', body) if s.strip()]
    num_sentences = len(sentences)
    avg_sentence_len = sum(len(s) for s in sentences) / num_sentences if num_sentences > 0 else 0
    
    # Paragraph structure check
    para_count = len(data["paragraphs_list"])
    
    readability_pts = 0
    # Sentence length scoring (Max 25 pts)
    if 0 < avg_sentence_len <= 65:
        readability_pts += 25
        s_status = "PASS"
        s_msg = f"문장의 평균 길이({int(avg_sentence_len)}자)가 간결하여 AI 언어모델이 맥락을 쉽게 구조화할 수 있습니다."
    elif 65 < avg_sentence_len <= 90:
        readability_pts += 15
        s_status = "WARN"
        s_msg = f"문장 평균 길이({int(avg_sentence_len)}자)가 약간 긴 편입니다. 조금 더 문장을 간소화하여 명확성을 높이세요."
    else:
        readability_pts += 5
        s_status = "FAIL"
        s_msg = f"평균 문장이 너무 깁니다({int(avg_sentence_len)}자). 문장이 장황할 시 생성형 요약 엔진이 오독하거나 핵심 추출을 놓칠 수 있습니다."
        
    geo_checks.append({
        "category": "가독성",
        "item": "평균 문장 길이 구조",
        "status": s_status,
        "msg": s_msg,
        "value": f"평균 {int(avg_sentence_len)}자"
    })
    
    # Paragraph scoring (Max 25 pts)
    if para_count >= 5:
        readability_pts += 25
        p_status = "PASS"
        p_msg = f"본문이 {para_count}개의 단락으로 구조적으로 조각나 있어 정보의 위계(Information Hierarchy)가 명확합니다."
    elif 2 <= para_count < 5:
        readability_pts += 12
        p_status = "WARN"
        p_msg = "단락 분리({para_count}개)가 적어 콘텐츠가 다소 뭉쳐 보입니다. 소제목(H2, H3)과 단락 구분을 확대하면 좋습니다."
    else:
        readability_pts += 5
        p_status = "FAIL"
        p_msg = "본문 텍스트가 거대하게 덩어리져 있어(1개 단락) 의미 단위를 분류하기 어렵습니다. 단락을 잘게 분해하고 소주제 헤더를 구성하세요."
        
    geo_checks.append({
        "category": "가독성",
        "item": "단락(Paragraph) 분할성",
        "status": p_status,
        "msg": p_msg,
        "value": f"{para_count}개 단락"
    })
    
    geo_score += readability_pts

    # ----------------- 4-Dimension Radar Chart Mapping -----------------
    # Compute scores for 4 areas mapped to 0-100 each:
    # 1. Metadata: Title (30) + Meta Desc (30) = 60 pts max. Map to 100
    dim_metadata = int((title_pts + desc_pts) * (100 / 60))
    
    # 2. Content Structure: H1 (20 pts). Plus H2-H6 diversity
    # Let's count diversity. Do we have at least one H2 and one H3?
    h2_exists = len(data["headers"]["h2"]) > 0
    h3_exists = len(data["headers"]["h3"]) > 0
    struct_extra = 0
    if h2_exists: struct_extra += 15
    if h3_exists: struct_extra += 15
    dim_structure = min(100, int((h1_pts * (70 / 20)) + struct_extra))
    
    # 3. Image Alt: img_pts (20) mapped to 100
    dim_images = int(img_pts * 5)
    
    # 4. Authority & Citation Density + Readability
    # Citations (50) + Readability (50) = 100 max.
    dim_trust_readability = int(citations_pts + readability_pts)

    radar_scores = {
        "metadata": dim_metadata,
        "structure": dim_structure,
        "images": dim_images,
        "trust_readability": dim_trust_readability
    }

    return {
        "seo_score": min(100, seo_score),
        "geo_score": min(100, geo_score),
        "seo_checks": seo_checks,
        "geo_checks": geo_checks,
        "radar_scores": radar_scores
    }

# ----------------- 3. Plotly Chart Generator -----------------

def generate_radar_chart(radar_scores: dict):
    """
    Renders an eye-catching, responsive Radar Chart using Plotly to show
    4 key dimensions of optimization.
    """
    categories = [
        '메타데이터 최적화', 
        '콘텐츠 위계 구조', 
        '이미지 웹 접근성', 
        '정보 신뢰도 & 가독성'
    ]
    
    values = [
        radar_scores["metadata"],
        radar_scores["structure"],
        radar_scores["images"],
        radar_scores["trust_readability"]
    ]
    
    # Radar chart expects the first point to be repeated at the end to close the polygon
    categories_closed = categories + [categories[0]]
    values_closed = values + [values[0]]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values_closed,
        theta=categories_closed,
        fill='toself',
        name='성숙도 점수',
        line=dict(color='#66fcf1', width=3),
        fillcolor='rgba(102, 252, 241, 0.25)',
        marker=dict(size=8, color='#45b3e0')
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                gridcolor='rgba(255, 255, 255, 0.1)',
                color='#8b9bb4',
                tickfont=dict(size=10, family='Outfit'),
                angle=0,
                tickangle=0
            ),
            angularaxis=dict(
                gridcolor='rgba(255, 255, 255, 0.1)',
                color='#e0e6ed',
                tickfont=dict(size=12, family='Outfit', weight='bold')
            ),
            bgcolor='rgba(31, 40, 51, 0.35)'
        ),
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=80, r=80, t=40, b=40),
        height=380
    )
    
    return fig

# ----------------- 4. Streamlit Application UI Layout -----------------

# Header Section
st.markdown('<div class="main-title">🔍 AI-SEO & GEO Insight Studio</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">웹사이트의 전통적 검색엔진 최적화(SEO) 및 차세대 생성형 AI 엔진 최적화(GEO) 동시 정밀 측정 플랫폼</div>', unsafe_allow_html=True)

# Initialize Session States
if "scraped_data" not in st.session_state:
    st.session_state.scraped_data = None
if "scores" not in st.session_state:
    st.session_state.scores = None
if "show_403_guide" not in st.session_state:
    st.session_state.show_403_guide = False

# Input Method Tabs
input_tab_url, input_tab_html = st.tabs(["🔗 URL 즉시 분석", "📄 HTML 소스 직접 붙여넣기 (보안 우회용)"])

with input_tab_url:
    st.markdown("<p style='color: #cbd5e1; font-size: 0.95rem; margin-bottom: 10px;'>웹사이트 주소(URL)를 입력하면 즉시 크롤링을 시도하여 실시간으로 정밀 측정합니다.</p>", unsafe_allow_html=True)
    col1, col2 = st.columns([4, 1])
    with col1:
        url_input = st.text_input(
            "분석할 웹사이트 URL 입력",
            placeholder="https://example.com 또는 blog.naver.com/post",
            label_visibility="collapsed",
            key="url_input_key"
        )
    with col2:
        start_btn = st.button("📈 분석 시작", use_container_width=True, key="start_btn_key")

    if start_btn:
        if not url_input:
            st.error("⚠️ 분석할 URL 주소를 명확히 입력해 주십시오.")
        else:
            st.session_state.show_403_guide = False
            with st.spinner("⚡ 타겟 사이트의 HTML 코드를 분석하고 위계를 구조화하고 있습니다..."):
                try:
                    data = scrape_url(url_input)
                    scores = calculate_scores(data)
                    st.session_state.scraped_data = data
                    st.session_state.scores = scores
                    st.success("✅ 사이트 구조 분석 및 점수 측정이 성공적으로 완료되었습니다!")
                except Exception as e:
                    err_msg = str(e)
                    st.error(f"❌ 분석 실패: {err_msg}")
                    if "403" in err_msg or "Forbidden" in err_msg:
                        st.session_state.show_403_guide = True

    # 403 Forbidden Friendly Help Guide Card
    if st.session_state.show_403_guide:
        st.markdown("""
        <div style="background: rgba(231, 76, 60, 0.08); border: 2px solid rgba(231, 76, 60, 0.4); border-radius: 12px; padding: 22px; margin-top: 15px; margin-bottom: 15px;">
            <h4 style="color: #e74c3c; margin-top: 0; margin-bottom: 12px; font-weight: 700; display: flex; align-items: center; gap: 8px;">
                🛑 HTTP 403 Forbidden 에러 대처 가이드
            </h4>
            <p style="color: #cbd5e1; font-size: 0.93rem; line-height: 1.6; margin-bottom: 15px;">
                분석을 요청하신 사이트는 <strong>Cloudflare, Akamai, AWS WAF</strong> 등 세계 최고 수준의 디도스 방어 및 무단 크롤링 방지 방화벽으로 강력히 보호되어 있습니다. 
                이러한 보안 시스템은 사람이 브라우저로 접근하는 것과 프로그램이 접속하는 것을 정교하게 가려내어 자동 스크래핑을 즉시 차단(HTTP 403 거부)합니다.
            </p>
            <h5 style="color: #ffffff; font-weight: 600; margin-bottom: 8px;">💡 어떻게 100% 우회하여 완벽히 분석할 수 있나요?</h5>
            <ol style="color: #cbd5e1; font-size: 0.9rem; line-height: 1.6; margin-left: 20px; padding-left: 0;">
                <li>크롬 등 브라우저를 열고 분석하고자 하던 타겟 페이지 주소로 정상 접속합니다.</li>
                <li>웹페이지 화면 빈 곳에서 <strong>마우스 우클릭 -> 페이지 소스 보기</strong>를 클릭하거나 <strong>Ctrl + U</strong> 키를 누릅니다.</li>
                <li>새 창에 나타나는 전체 소스 코드를 모두 선택(<strong>Ctrl + A</strong>)하여 복사(<strong>Ctrl + C</strong>)합니다.</li>
                <li>상단의 <strong>'📄 HTML 소스 직접 붙여넣기'</strong> 탭을 클릭하여 복사한 HTML 소스를 입력창에 붙여 넣고 분석 버튼을 누릅니다!</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)

with input_tab_html:
    st.markdown("<p style='color: #cbd5e1; font-size: 0.95rem; margin-bottom: 10px;'>보안 방화벽으로 자동 크롤링이 차단된 페이지의 소스 코드를 복사해서 붙여넣으시면, 보안 제약 없이 동일한 정밀 분석이 가능합니다.</p>", unsafe_allow_html=True)
    
    virtual_url = st.text_input(
        "대상 주소(URL) 입력 (선택사항)",
        placeholder="https://example.com (분석 시 링크 매핑 및 문맥 제공용)",
        key="virtual_url_key"
    )
    
    html_input = st.text_area(
        "HTML 소스 코드 붙여넣기",
        placeholder="<!DOCTYPE html> ... 으로 시작하는 웹페이지 전체 소스코드를 복사해서 넣어주세요.",
        height=220,
        key="html_input_key"
    )
    
    html_start_btn = st.button("📄 붙여넣은 HTML 소스 분석 시작", use_container_width=True, key="html_start_btn_key")
    
    if html_start_btn:
        if not html_input.strip():
            st.error("⚠️ 분석할 HTML 소스 코드를 입력창에 채워주십시오.")
        else:
            st.session_state.show_403_guide = False
            with st.spinner("⚡ 직접 입력된 HTML 코드를 구문 분석하고 위계를 구조화하고 있습니다..."):
                try:
                    ref_url = virtual_url.strip() if virtual_url.strip() else "https://direct-html-input.local"
                    data = parse_html_content(html_input, ref_url)
                    scores = calculate_scores(data)
                    st.session_state.scraped_data = data
                    st.session_state.scores = scores
                    st.success("✅ 수동 입력된 HTML 구조 분석 및 점수 측정이 성공적으로 완료되었습니다!")
                except Exception as e:
                    st.error(f"❌ HTML 파싱 중 에러 발생: {str(e)}")

# ----------------- Sidebar Configuration -----------------
st.sidebar.image("https://img.icons8.com/nolan/128/artificial-intelligence.png", width=70)

# Wrap API settings title and description in a beautiful, premium visual card with high visibility
# API Key Configuration via Streamlit Secrets (Security Guardrail)
#
# 로컬 개발 및 테스트를 위한 `.streamlit/secrets.toml` 파일 예시 구조:
# ==========================================================
# # .streamlit/secrets.toml
# GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
# ==========================================================

st.sidebar.markdown("""
<div style="background: rgba(102, 252, 241, 0.08); border: 2px solid rgba(102, 252, 241, 0.4); border-radius: 12px; padding: 15px; margin-bottom: 20px;">
    <h3 style="color: #66fcf1; margin-top: 0; margin-bottom: 10px; font-size: 1.15rem; font-weight: 700; display: flex; align-items: center; gap: 8px;">
        🛠️ Gemini API 설정
    </h3>
    <p style="color: #cbd5e1; font-size: 0.88rem; line-height: 1.5; margin: 0;">
        안전한 API 관리를 위해 Streamlit Secrets를 통해 <strong>GEMINI_API_KEY</strong>를 로드합니다.
    </p>
</div>
""", unsafe_allow_html=True)

# API Key Configuration via Streamlit Sidebar / OS Environment Variables
import os

# 1. Sidebar input field for API key (masked as password for security)
user_api_key = st.sidebar.text_input(
    "🔑 Gemini API Key 직접 입력",
    type="password",
    help="보안을 위해 API 키를 소스 코드나 설정 파일에 저장하지 않고 웹 브라우저에서 직접 입력하여 사용할 수 있습니다. 입력한 키는 시스템 환경 변수 설정보다 우선 적용됩니다.",
    placeholder="AIzaSy..."
)

def get_gemini_api_key(user_key):
    # Priority 1: Direct user input from sidebar
    if user_key and user_key.strip():
        return user_key.strip()
    
    # Priority 2: System environment variables (os.environ)
    for key in ["GEMINI_API_KEY", "gemini_api_key"]:
        val = os.environ.get(key)
        if val and val.strip():
            return val.strip()
    return None

gemini_api_key = get_gemini_api_key(user_api_key)
api_key_configured = gemini_api_key is not None

if api_key_configured:
    st.sidebar.success("🔑 Gemini API 인증 완료")
else:
    st.sidebar.error("❌ Gemini API Key 미설정")
    st.sidebar.markdown(
        """
        <div style="font-size: 0.85rem; color: #cbd5e1; line-height: 1.5;">
            위의 <strong>'Gemini API Key 직접 입력'</strong> 란에 API 키를 붙여넣거나, 시스템 환경 변수에 <code>GEMINI_API_KEY</code>를 등록해 주세요.
        </div>
        """,
        unsafe_allow_html=True
    )

selected_model = st.sidebar.selectbox(
    "⚙️ Gemini 모델 선택",
    ["gemini-2.5-flash", "gemini-2.5-pro", "gemini-1.5-flash", "gemini-1.5-pro"],
    index=0,
    help="특정 모델의 트래픽 폭주로 503 에러가 발생할 시 다른 버전의 모델을 선택해 보실 수 있습니다."
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 GEO (Generative Engine Optimization) 란?")
st.sidebar.markdown(
    """
    인공지능 검색 엔진이 정보 출처를 채택하고 답변을 생성할 때, 특정 사이트가 **가장 신뢰성 높고 명확한 출처**로 선정되게끔 콘텐츠 정보 구조와 텍스트 위계를 AI 모델 선호에 맞게 가공하는 최신 최적화 패러다임입니다.
    """
)

# Display results if available in session state
if st.session_state.scraped_data and st.session_state.scores:
    data = st.session_state.scraped_data
    scores = st.session_state.scores

    st.markdown("---")
    
    # ---------------- Dashboard Layout: Core Score visualization ----------------
    row1_col1, row1_col2 = st.columns([1, 1], gap="large")

    with row1_col1:
        st.markdown('<h3 style="margin-bottom: 20px;">📊 최적화 성숙도 다이어그램</h3>', unsafe_allow_html=True)
        # Radar Chart
        fig = generate_radar_chart(scores["radar_scores"])
        st.plotly_chart(fig, use_container_width=True)

    with row1_col2:
        st.markdown('<h3 style="margin-bottom: 20px;">🏆 종합 최적화 점수</h3>', unsafe_allow_html=True)
        
        # SEO Score Card
        seo_color = "#2ecc71" if scores["seo_score"] >= 80 else ("#f1c40f" if scores["seo_score"] >= 50 else "#e74c3c")
        st.markdown(f"""
        <div class="custom-card">
            <div class="metric-container">
                <div class="metric-lbl">SEO (검색엔진 최적화) 점수</div>
                <div class="metric-val" style="color: {seo_color};">{scores["seo_score"]}<span style="font-size: 1.5rem; font-weight: normal; color: #cbd5e1;">/100</span></div>
            </div>
            <p style="margin: 0; font-size: 0.95rem; color: #ffffff; line-height: 1.6;">
                구글, 네이버 등 크롤러 기반의 기존 검색봇이 정보를 완벽히 인덱싱하고 크롤링할 수 있도록 돕는 HTML 구조적 정합성 점수입니다.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # GEO Score Card
        geo_color = "#2ecc71" if scores["geo_score"] >= 80 else ("#f1c40f" if scores["geo_score"] >= 50 else "#e74c3c")
        st.markdown(f"""
        <div class="custom-card" style="margin-top: 15px;">
            <div class="metric-container">
                <div class="metric-lbl">GEO (생성형엔진 최적화) 점수</div>
                <div class="metric-val" style="color: {geo_color};">{scores["geo_score"]}<span style="font-size: 1.5rem; font-weight: normal; color: #cbd5e1;">/100</span></div>
            </div>
            <p style="margin: 0; font-size: 0.95rem; color: #ffffff; line-height: 1.6;">
                LLM 및 생성형 답변 생성봇이 본문 텍스트 내에서 객관적 근거를 인식하고 구조화된 Schema(JSON-LD)를 통해 엔티티로 매핑하여 답변 출처로 채택할 수 있는 AI 선호도 점수입니다.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # ----------------- 5. Gemini AI Consultant Integration -----------------
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<h3>🤖 AI 검색엔진 추천을 위한 전문가 GEO 심층 컨설팅</h3>', unsafe_allow_html=True)

    if not api_key_configured:
        st.info("💡 **Gemini API Key**가 설정되지 않았습니다. 사이드바에서 직접 입력하거나 시스템 환경 변수에 GEMINI_API_KEY를 설정해 주세요.")
        consult_btn = st.button("🩺 전문가 GEO 심층 컨설팅 시작", disabled=True)
    else:
        consult_btn = st.button("🩺 전문가 GEO 심층 컨설팅 시작", disabled=False)
        
        if consult_btn:
            with st.spinner("🤖 세계 최고의 GEO 컨설턴트 페르소나를 장착하고 사이트 텍스트 구조 분석 및 개선 제안서를 작성 중입니다..."):
                try:
                    # Initialize the google-genai client using gemini_api_key
                    client = genai.Client(api_key=gemini_api_key)
                    
                    # Prepare input text (safely truncated to fit prompt cleanly)
                    preview_text = data["body_text"][:4000]
                    headers_summary = {k: v[:5] for k, v in data["headers"].items() if v}
                    
                    prompt = f"""
                    너는 AI 검색 엔진(구글 SGE, Perplexity, ChatGPT Search, Gemini 등)에서 이 사이트의 콘텐츠가 최우선으로 인용되고 추천되도록 돕는 세계 최고의 SEO 및 GEO(생성형 엔진 최적화) 컨설턴트야.
                    아래 제공되는 웹사이트 데이터를 바탕으로 가장 중요하고 시급히 개선해야 할 핵심 문제점과 구체적인 액션 플랜을 도출해줘.

                    반드시 아래 제공된 JSON 형식(JSON schema)에 정확히 맞추어 응답을 작성해 줘. 다른 서론이나 설명은 배제하고 오직 순수 JSON 데이터만 출력해야 해.

                    [대상 URL]
                    {data["url"]}

                    [분석 점수 결과]
                    - SEO 점수: {scores["seo_score"]}/100
                    - GEO 점수: {scores["geo_score"]}/100
                    - 4차원 다이어그램 점수:
                      * 메타데이터: {scores["radar_scores"]["metadata"]}점
                      * 콘텐츠 구조: {scores["radar_scores"]["structure"]}점
                      * 이미지 최적화: {scores["radar_scores"]["images"]}점
                      * 정보 신뢰도 & 가독성: {scores["radar_scores"]["trust_readability"]}점

                    [추출된 헤딩 구조 (최대 5개씩)]
                    {json.dumps(headers_summary, ensure_ascii=False, indent=2)}

                    [사이트 본문 텍스트 (최대 4000자 발췌)]
                    {preview_text}

                    [JSON 출력 형식 (Schema)]
                    {{
                      "seo_problems": [
                        {{
                          "num": 1,
                          "text": "SEO 핵심 문제점 내용 설명 (구체적이고 통계적인 분석 반영)"
                        }},
                        {{
                          "num": 2,
                          "text": "SEO 핵심 문제점 내용 설명"
                        }},
                        {{
                          "num": 3,
                          "text": "SEO 핵심 문제점 내용 설명"
                        }}
                      ],
                      "geo_problems": [
                        {{
                          "num": 1,
                          "text": "GEO 핵심 문제점 내용 설명 (LLM 및 생성형 AI 관점에서 구체적인 문제 요인 분석)"
                        }},
                        {{
                          "num": 2,
                          "text": "GEO 핵심 문제점 내용 설명"
                        }},
                        {{
                          "num": 3,
                          "text": "GEO 핵심 문제점 내용 설명"
                        }}
                      ],
                      "seo_action_plans": [
                        {{
                          "num": 1,
                          "title": "SEO 액션 플랜 제목",
                          "priority": "높음" 또는 "중간" 또는 "낮음",
                          "text": "구체적인 실무 적용 해결 방안 설명. **반드시 직접 사용할 수 있는 구체적인 HTML 태그 수정 예시나 스크립트 코드 조각을 마크다운 코드 블록(예: ```html ... ```)으로 정교하게 구성해서 포함시켜줘.**"
                        }},
                        {{
                          "num": 2,
                          "title": "SEO 액션 플랜 제목",
                          "priority": "높음" 또는 "중간" 또는 "낮음",
                          "text": "해결 방안 설명 및 스크립트 수정 제안 코드 블록"
                        }},
                        {{
                          "num": 3,
                          "title": "SEO 액션 플랜 제목",
                          "priority": "높음" 또는 "중간" 또는 "낮음",
                          "text": "해결 방안 설명 및 스크립트 수정 제안 코드 블록"
                        }}
                      ],
                      "geo_action_plans": [
                        {{
                          "num": 1,
                          "title": "GEO 액션 플랜 제목",
                          "priority": "높음" 또는 "중간" 또는 "낮음",
                          "text": "생성형 AI 검색 랭킹 상승을 위한 구체적인 텍스트 수정 및 구조 배치 팁. **실제 서비스에 즉시 삽입할 수 있는 최적화된 문맥 및 문구 수정 예시를 마크다운 코드 블록(예: ```html ... ``` 또는 ```text ... ```)으로 상세히 작성해서 포함시켜줘.**"
                        }},
                        {{
                          "num": 2,
                          "title": "GEO 액션 플랜 제목",
                          "priority": "높음" 또는 "중간" 또는 "낮음",
                          "text": "해결 방안 및 구체적 문구 예시 코드 블록"
                        }},
                        {{
                          "num": 3,
                          "title": "GEO 액션 플랜 제목",
                          "priority": "높음" 또는 "중간" 또는 "낮음",
                          "text": "해결 방안 및 구체적 문구 예시 코드 블록"
                        }}
                      ]
                    }}
                    """
                    
                    # Try executing the selected model, with automatic backup models if rate limited or overloaded
                    models_to_try = [selected_model]
                    for backup in ["gemini-2.5-pro", "gemini-1.5-flash", "gemini-1.5-pro"]:
                        if backup not in models_to_try:
                            models_to_try.append(backup)
                    
                    response = None
                    last_err = None
                    used_model = None
                    
                    for model_name in models_to_try:
                        try:
                            response = client.models.generate_content(
                                model=model_name,
                                contents=prompt,
                                config=types.GenerateContentConfig(
                                    response_mime_type="application/json"
                                )
                            )
                            used_model = model_name
                            break
                        except Exception as e:
                            last_err = e
                            st.warning(f"⚠️ {model_name} 모델 호출에 실패하여 다음 대체 모델로 전환합니다.")
                            continue
                    
                    if response is None:
                        raise last_err
                    
                    try:
                        # Attempt to parse output as JSON
                        raw_text = response.text.strip()
                        if raw_text.startswith("```"):
                            match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", raw_text)
                            if match:
                                raw_text = match.group(1).strip()
                        report_data = json.loads(raw_text)
                        
                        # Beautiful Premium Dashboard Layout Renderer
                        st.markdown(f"""
                        <div style="background: rgba(102, 252, 241, 0.05); border: 1px solid rgba(102, 252, 241, 0.3); border-radius: 16px; padding: 20px; margin-top: 25px; margin-bottom: 25px;">
                            <h4 style="color: #66fcf1; margin: 0; font-size: 1.3rem; font-weight: 700; display: flex; justify-content: space-between; align-items: center;">
                                <span>📋 Gemini SEO & GEO 전문 심층 분석 보고서</span>
                                <span style="font-size: 0.85rem; font-weight: normal; color: #8b9bb4;">사용된 AI 모델: {used_model}</span>
                            </h4>
                        </div>
                        """, unsafe_allow_html=True)

                        # Create two columns for SEO/GEO key problems
                        p_col1, p_col2 = st.columns(2, gap="medium")
                        
                        with p_col1:
                            st.markdown('<h4 style="color: #66fcf1; margin-bottom: 15px; font-weight: 700; display: flex; align-items: center; gap: 8px;">🔒 SEO 핵심 문제점</h4>', unsafe_allow_html=True)
                            for prob in report_data.get("seo_problems", []):
                                st.markdown(f"""
                                <div class="problem-card">
                                    <div class="problem-badge seo-badge">#{prob.get('num', 1)}</div>
                                    <div class="problem-text">{prob.get('text', '')}</div>
                                </div>
                                """, unsafe_allow_html=True)
                                
                        with p_col2:
                            st.markdown('<h4 style="color: #c084fc; margin-bottom: 15px; font-weight: 700; display: flex; align-items: center; gap: 8px;">🌐 GEO 핵심 문제점</h4>', unsafe_allow_html=True)
                            for prob in report_data.get("geo_problems", []):
                                st.markdown(f"""
                                <div class="problem-card">
                                    <div class="problem-badge geo-badge">#{prob.get('num', 1)}</div>
                                    <div class="problem-text">{prob.get('text', '')}</div>
                                </div>
                                """, unsafe_allow_html=True)

                        st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)

                        # Action Plans section with tabs
                        st.markdown('<h4 style="color: #ffffff; margin-bottom: 15px; font-weight: 700;">🚀 최적화 액션 플랜</h4>', unsafe_allow_html=True)
                        
                        act_tab_seo, act_tab_geo = st.tabs(["🔒 SEO 액션 플랜", "🌐 GEO 액션 플랜"])
                        
                        with act_tab_seo:
                            st.markdown("<p style='color: #cbd5e1; font-size: 0.95rem; margin-bottom: 15px;'>전통적 검색 엔진 최적화 및 봇 크롤링 효율을 높이기 위한 실행 플랜입니다.</p>", unsafe_allow_html=True)
                            for plan in report_data.get("seo_action_plans", []):
                                prio = plan.get('priority', '중간')
                                prio_class = "priority-high" if prio == "높음" else ("priority-medium" if prio == "중간" else "priority-low")
                                
                                st.markdown(f"""
                                <div style="margin-top: 22px; display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
                                    <div class="action-num-badge" style="background: #45b3e0; margin-right: 0; display: flex; align-items: center; justify-content: center; width: 26px; height: 26px; border-radius: 50%; color: white; font-weight: bold; font-size: 0.9rem;">{plan.get('num', 1)}</div>
                                    <strong style="color: #ffffff; font-size: 1.05rem;">{plan.get('title', '')}</strong>
                                    <span class="priority-badge {prio_class}">우선순위: {prio}</span>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                # Render body as rich markdown (to properly support code blocks, bold strings, and script examples)
                                st.markdown(plan.get('text', ''))
                                st.markdown("<hr style='margin: 1.5rem 0; opacity: 0.35;' />", unsafe_allow_html=True)
                                
                        with act_tab_geo:
                            st.markdown("<p style='color: #cbd5e1; font-size: 0.95rem; margin-bottom: 15px;'>생성형 AI 검색 엔진(LLM)에 의해 정보 출처로 적극 추천/인용되기 위한 액션 플랜입니다.</p>", unsafe_allow_html=True)
                            for plan in report_data.get("geo_action_plans", []):
                                prio = plan.get('priority', '중간')
                                prio_class = "priority-high" if prio == "높음" else ("priority-medium" if prio == "중간" else "priority-low")
                                
                                st.markdown(f"""
                                <div style="margin-top: 22px; display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
                                    <div class="action-num-badge" style="background: #8b5cf6; margin-right: 0; display: flex; align-items: center; justify-content: center; width: 26px; height: 26px; border-radius: 50%; color: white; font-weight: bold; font-size: 0.9rem;">{plan.get('num', 1)}</div>
                                    <strong style="color: #ffffff; font-size: 1.05rem;">{plan.get('title', '')}</strong>
                                    <span class="priority-badge {prio_class}">우선순위: {prio}</span>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                # Render body as rich markdown (to properly support code blocks, bold strings, and JSON-LD script examples)
                                st.markdown(plan.get('text', ''))
                                st.markdown("<hr style='margin: 1.5rem 0; opacity: 0.35;' />", unsafe_allow_html=True)
                                
                    except Exception as parse_err:
                        # Resilient Fallback to raw text representation
                        st.warning("⚠️ 심층 분석 보고서를 구조화된 레이아웃으로 파싱하지 못했습니다. 대신 원본 마크다운 텍스트를 출력합니다.")
                        st.markdown(response.text)
                    
                except Exception as e:
                    st.error(f"❌ Gemini 컨설팅 리포트 생성 도중 에러가 발생했습니다: {str(e)}")

    # ------------------ Detail Scorecard Tabs ------------------
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<h3>🔍 상세 진단 체크리스트</h3>', unsafe_allow_html=True)

    tab_seo, tab_geo, tab_raw = st.tabs(["🔒 SEO (검색엔진 최적화) 체크리스트", "🌐 GEO (생성형 AI 최적화) 체크리스트", "📝 파싱된 원시 데이터 및 태그"])

    # 1. Tab SEO Display
    with tab_seo:
        st.markdown("<p style='color: #cbd5e1; font-size: 1rem; margin-bottom: 15px;'>크롤러 기반의 일반 검색 봇에 노출되는 기준들을 정밀 검진합니다.</p>", unsafe_allow_html=True)
        
        for item in scores["seo_checks"]:
            badge_class = "status-pass" if item["status"] == "PASS" else ("status-warn" if item["status"] == "WARN" else "status-fail")
            st.markdown(f"""
            <div style="background: #161a23; border-left: 4px solid { '#2ecc71' if item['status'] == 'PASS' else ('#f1c40f' if item['status'] == 'WARN' else '#e74c3c') }; padding: 15px; border-radius: 8px; margin-bottom: 12px; border-top: 1px solid rgba(255,255,255,0.03); border-right: 1px solid rgba(255,255,255,0.03); border-bottom: 1px solid rgba(255,255,255,0.03);">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <strong style="color: #ffffff; font-size: 1.05rem;">{item["item"]}</strong>
                    <span class="status-badge {badge_class}">{item["status"]} ({item["value"]})</span>
                </div>
                <div style="font-size: 0.92rem; color: #f1f5f9; margin-top: 6px; line-height: 1.5;">{item["msg"]}</div>
            </div>
            """, unsafe_allow_html=True)

    # 2. Tab GEO Display
    with tab_geo:
        st.markdown("<p style='color: #cbd5e1; font-size: 1rem; margin-bottom: 15px;'>LLM 엔진이 본문을 출처로 인용할 때 우선 고려하는 수치/통계 신뢰성, JSON-LD, 문장 가독성을 점검합니다.</p>", unsafe_allow_html=True)
        
        for item in scores["geo_checks"]:
            badge_class = "status-pass" if item["status"] == "PASS" else ("status-warn" if item["status"] == "WARN" else "status-fail")
            st.markdown(f"""
            <div style="background: #161a23; border-left: 4px solid { '#2ecc71' if item['status'] == 'PASS' else ('#f1c40f' if item['status'] == 'WARN' else '#e74c3c') }; padding: 15px; border-radius: 8px; margin-bottom: 12px; border-top: 1px solid rgba(255,255,255,0.03); border-right: 1px solid rgba(255,255,255,0.03); border-bottom: 1px solid rgba(255,255,255,0.03);">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <strong style="color: #ffffff; font-size: 1.05rem;">{item["item"]}</strong>
                    <span class="status-badge {badge_class}">{item["status"]} ({item["value"]})</span>
                </div>
                <div style="font-size: 0.92rem; color: #f1f5f9; margin-top: 6px; line-height: 1.5;">{item["msg"]}</div>
            </div>
            """, unsafe_allow_html=True)

    # 3. Tab Raw Parsed HTML Data Display
    with tab_raw:
        st.markdown("<h4>📋 기본 추출된 주요 요소</h4>", unsafe_allow_html=True)
        st.markdown(f"**타겟 URL:** `{data['url']}`")
        st.markdown(f"**추출된 Title:** `{data['title']}`")
        st.markdown(f"**추출된 Meta Description:** `\"{data['meta_description']}\"`")
        
        st.markdown("---")
        st.markdown("<h4>🔗 OpenGraph 메타 데이터</h4>", unsafe_allow_html=True)
        if data["og_tags"]:
            st.json(data["og_tags"])
        else:
            st.info("페이지 내 OpenGraph 메타태그가 존재하지 않습니다.")

        st.markdown("---")
        st.markdown("<h4>🧱 H1~H6 제목 구조 (Headers Structure)</h4>", unsafe_allow_html=True)
        has_headers = any(len(v) > 0 for v in data["headers"].values())
        if has_headers:
            for level, items in data["headers"].items():
                if items:
                    st.markdown(f"**{level.upper()} 태그 ({len(items)}개)**")
                    st.code("\n".join(items), language="text")
        else:
            st.info("제목 태그(Heading tags)가 식별되지 않습니다.")

        # Removed Schema.org JSON-LD structured data section from tab_raw

        st.markdown("---")
        st.markdown("<h4>📝 추출된 순수 본문 텍스트 (앞부분 1500자 요약)</h4>", unsafe_allow_html=True)
        if data["body_text"]:
            st.text_area("순수 추출 텍스트", data["body_text"][:1500] + ("..." if len(data["body_text"]) > 1500 else ""), height=250)
        else:
            st.warning("본문 텍스트를 가져오지 못했습니다. 빈 페이지거나 봇 접속이 차단되었을 수 있습니다.")
else:
    st.info("💻 위의 텍스트 창에 분석할 사이트 URL을 입력하고 **'분석 시작'** 버튼을 클릭해 주십시오.")

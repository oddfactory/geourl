# AI-SEO & GEO Insight Studio 🔍📈

> **전통적인 검색엔진 최적화(SEO)와 차세대 AI 생성형 엔진 최적화(GEO)를 동시에 진단하고 개선을 돕는 통합 대시보드 플랫폼**

이 플랫폼은 사용자가 입력한 웹사이트 URL의 HTML 구조를 실시간으로 크롤링하고 분석하여 정밀한 SEO 및 GEO 성숙도 점수를 산출합니다. 또한, **Plotly 방사형 그래프(Radar Chart)**를 통한 시각화와 더불어 **Google Gemini API**를 연동한 자가 치유형 전문 GEO 심층 컨설팅 리포트를 제공합니다.

---

## 주요 핵심 기능 (Key Features)

1. **실시간 웹 스크래핑 & 위계 분석**:
   - `requests` 및 `BeautifulSoup4`를 활용한 정적 HTML 파싱 (Desktop User-Agent 우회 적용).
   - 메타데이터(Title, Meta Description), 제목 위계 구조(H1~H6), 이미지 alt 속성 누락 검사, JSON-LD Schema.org 구조화 데이터 추출.

2. **SEO & GEO 하이브리드 진단 엔진**:
   - **SEO 스코어 (0-100점)**: 검색 엔진 노출을 위한 가이드라인 준수 여부 정량 평가.
   - **GEO 스코어 (0-100점)**: AI 언어 모델이 본문을 신뢰성 높은 출처로 인식하고 인용(Citation)을 채택할 수 있는 AI 검색 맞춤도(인용 밀도, 단락 구조, 수치/통계 자료 등) 분석.

3. **Plotly 방사형 그래프 (Radar Chart) 시각화**:
   - 5대 최적화 도메인(메타데이터, 콘텐츠 구조, 이미지 접근성, Semantic 구조화 데이터, 정보 신뢰도 & 가독성)별 다이어그램 제공.

4. **Gemini 연동 정밀 GEO 컨설팅 (Self-Healing Fallback 탑재)**:
   - AI 검색 엔진(Perplexity, ChatGPT Search, Gemini 등)의 추천 출처 선정을 위한 전문가 보고서 생성.
   - **자가 치유 백업 아키텍처**: 요청하신 모델이 트래픽 폭주(503 Unavailable)로 실패할 경우, 2.5-pro, 1.5-flash 등의 백업 모델군으로 순차 자동 전환 호출을 시도하여 항상 안정적으로 보고서를 작성해 냅니다.

---

## 기술 스택 (Tech Stack)

- **Language**: Python 3.12+
- **Web UI Framework**: Streamlit
- **Visualization**: Plotly
- **Crawling/Parsing**: Requests, BeautifulSoup4
- **LLM SDK**: google-genai (Gemini 2.5 & 1.5 Series)

---

## 실행 및 배포 방법 (How to Run)

### 1. 패키지 설치
필요한 외부 종속성 라이브러리를 먼저 설치해 줍니다.
```bash
pip install streamlit requests beautifulsoup4 plotly google-genai
```

### 2. Streamlit 대시보드 기동
```bash
streamlit run app.py
```
브라우저에서 자동으로 `http://localhost:8501`이 열리며 대시보드를 즉시 사용하실 수 있습니다.

# TRENDIE
> 여행 유튜버(인플루언서)를 위한 틱톡, 유튜브의 트렌드를 분석하여 현재 여행 트렌드를 제공하고, 사용자가 업로드 할 영상을 분석하여 (맞춤형) 해시태그와 제목을 제공하는 모바일 어플리케이션

## 🔍 프로젝트 개요

**TRENDIE**는

✔ 최신 여행 트렌드를 시각화한 대시보드  
✔ 사용자 영상의 트렌드 일치도 피드백 보고서  

를 제공하는 **여행 유튜버 대상 피드백 제공 서비스**입니다.

---

## 🖼️ 프로젝트 구성

- **whisper-keyword-generator**
  </br>Whisper API와 OpenAI를 사용해 동영상 속 음성을 텍스트로 변환하고 해시태그로 사용할 만한 키워드를 추출합니다.

- **TikTok Crawler**
  </br>TikTok Creative Center에서 제공하는 인기 순위 목록을 수집합니다. 인기 있는 음악 정보와 여행 관련 인기 해시태그를 크롤링하여 음악과 여행 트렌드를 분석합니다.

- **YouTube Travel Analyzer** (텍스트 분석 모듈)  
  유튜브 API를 사용해 여행 관련 영상을 수집하고, 텍스트 분석으로 여행 키워드를 추출합니다. 추출한 키워드를 기반으로 영상의 여행 관련도를 계산하여 최종적으로 여행 관련 영상 제목 목록을 제공합니다.

    ### 📁 주요 파일 구조

    ```
    whisper-keyword-generator.ipynb    # ASR(Automatic Speech Recognition) & 키워드 추출
    ```

    ```
    TikTok_Crawler/
    │
    ├── hashtag_crawler.py         # 틱톡 해시태그 순위 크롤링                 
    ├── music_crawler.py           # 틱톡 음악 순위 크롤링
    ├── save_cookies.py            # 로그인 세션 쿠키 저장
    ├── requirements.txt           # 필요한 패키지 목록
    ```
    
    ```
    youtube_travel_analyzer/
    │
    ├── main.py                  # 실행 스크립트
    ├── youtube_api.py           # 유튜브 API 호출
    ├── text_processing.py       # 텍스트 전처리 및 키워드 분석
    ├── config.py                # 환경변수 및 설정값 로딩
    ├── stopwords-ko.txt         # 한국어 불용어 리스트
    ├── requirements.txt         # 필요한 패키지 목록
    ├── utils.py                 # 결과 출력 및 저장
    ├── .env                     # 환경변수 파일 (로컬 전용)
    ```

    ### ⚙️ 설치 및 실행
  
    **TikTok_Crawler**
    1. Python(최소 3.8 필요) 설치
    2. `pip install -r requirements.txt`
        </br>playwright 최초 설치일 경우 아래 명령어로 브라우저 드라이버 설치:
          </br>`playwright install`
    3. 틱톡 크리에이티브 센터 로그인 쿠키 저장:
        </br>`python save_tiktok_cookies.py` 실행
       </br>자동 실행된 브라우저(틱톡 크리에이티브 센터)에 직접 로그인 후 터미널에 Enter 입력
    4. 인기 해시태그 순위 크롤링 및 클러스터링:
        </br>`python tiktok_hashtag_crawler.py` 실행
    5. 인기 음악 순위 크롤링:
        </br>`python tiktok_music_crawler.py` 실행
  
    **youtube_travel_analyzer/**
    1. 가상환경 생성 및 활성화  
    2. `pip install -r requirements.txt`  
    3. `.env` 파일 생성 후 아래 변수 설정:

    ```env
    YOUTUBE_API_KEY="여기에_API_키"
    STOPWORDS_PATH="stopwords-ko.txt"
    REGION_CODE="KR"
    MAX_RESULTS=50
    TOP_KEYWORDS=3
    TRAVEL_SCORE_THRESHOLD=3
    ```

    4. `python main.py` 실행

    ### ⚠️ 주의사항

    **TikTok_Crawler/**
    - 크롤링 실패/페이지 구조 변경 시:
      1. playwright 브라우저 최신화
      2. 브라우저 창 크기에 맞추어 스크롤 조정
      3. 코드 내 셀렉터(버튼/텍스트 등) 점검
    - 쿠키 저장 파일명 tiktok_cookies.json
    - 쿠키 만료/로그아웃 시:
      </br>`tiktok_cookies.json` 삭제 후 쿠키 저장 재진행

    **youtube_travel_analyzer/**
    - `.env` 파일에 API 키 등 민감 정보 포함, 깃허브 업로드 금지  
    - API 키는 Google Cloud Console에서 발급받을 것

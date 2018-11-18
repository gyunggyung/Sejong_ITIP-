 <h1 align="left">crawling.py</h1>
 
 ## Intro
 [구글 지도 웹사이트](https://www.google.com/maps)를 실행하여 미리 입력한 키워드를 기반으로 키워드 당 최대 20개 검색,
  DB를 생성하여 저장합니다.
 
 ## Dependency to use
 크롤러 모듈을 실행하기 위해서는 아래와 같은 라이브러리/프로그램이 필요합니다.
 > BeautifulSoup4\
 > Selenium\
 > [ChromeDriver](http://chromedriver.chromium.org/downloads)
 
 ## How to use
 [place_list.txt](/place_list.txt) 파일의 각 행에 검색하고자 하는 키워드를 입력한 뒤 push_to_db 함수 를 실행합니다.
 ```python
push_to_db()
```
 push_to_db 함수는 키워드에 해당하는 검색 결과를 불러와 하기 Output 목록에 해당하는 값을 추출하여 Seoul_Place.csv 파일에 저장합니다.
  
 이와 별개로, get_location 함수를 실행해 현재 위치와 구 단위 주소를 받아올 수 있습니다.
 ```python
 get_location()
```
예를 들어 현재 위치가 세종대 광개토관일 경우, 반환값은 `[127.0731761, 37.5500612, 광진구]` 입니다.
 
 
 ##Notice
 자바스크립트를 실행하여 크롤링하기 때문에 로딩 지연 등으로 크롤링 과정이 불안정할 수 있습니다.\
 또한 크롬드라이버가 최소화 상태로 있으면 크롤링 중 오류가 발생할 수 있습니다. 
 
 ## Output
 - Name : 이름
 - Function : 범주
 - Details : 상세설명
 - (Date - Saturday, Sunday 등) : 날짜 별 영업 시간
 - Score : 구글 지도 상의 평점
 - Indoor/Outdoors : 실내/외 위치 여부
 - Longitude : 경도
 - Latitude : 위도
 - Image : 구글 지도 상의 가장 처음 사진
 

![](image/crawling_output.png)
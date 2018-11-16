 <h1 align="left">weather.py</h1>
 
 ## Intro
 [동네예보정보조회서비스](https://www.data.go.kr/dataset/15000099/openapi.do) API를 호출해 현재 위치의 실시간 기상정보를 불러옵니다.
 
 ##Dependency to use
 실시간 기상정보 모듈을 사용하기 위해선 아래의 라이브러리/API 키가 필요합니다
 >pytz\
 >[동네예보정보조회서비스](https://www.data.go.kr/dataset/15000099/openapi.do) API 키
 
 ## How to use
 현재 위치의 경도와 위도, API 키를 인자로 하여 get_weather_data 함수를 실행합니다.
 ```python
get_weather_data(126.976695, 37.57737, API key)
```
예를 들어, 경복궁의 실시간 기상정보를 불러오기 위해서 위와 같이 입력합니다.\
2018년 11월 16시 5시 기준 출력값은\
`{'T1H': '9', 'RN1': '0', 'PTY': '0', 'SKY': '1', 'LGT': '0', 'WSD': 'None'}`입니다.

## Output
    data_parsed 에는 T1H, RN1, PTY, SKY, LGT, WSD 가 존재
    T1H : 기온
    RN1 : 1시간 강수량
          (0 - 0mm 또는 없음)
          (1 - 1mm 미만)
          (5 - 1~4mm)
          (10 - 5~9mm)
          (20 - 10~19mm)
          (40 - 20~39mm)
          (70 - 40~69mm)
          (100 - 70mm 이상)
    PTY : 강수형태 -- 0 - 없음 , 1 - 비 , 2 - 진눈깨비 , 3 - 눈
    SKY : 하늘상태 -- 1 - 맑음 , 2 - 구름조금 , 3 - 구름많음 , 4 - 흐림
    LGT : 낙뢰 -- 0 - 없음 , 1 - 있음
             또는 0 - 없음 , 1 - 낮음 , 2 - 보통 , 3 - 높음
    WSD : 풍속
    
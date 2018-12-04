 <h1 align="left">weather.py</h1>
 
 ## Intro
 [대기오염정보 조회 서비스](https://www.data.go.kr/dataset/15000581/openapi.do) API를 호출해 현재 위치의 미세먼지 현황을 불러옵니다.
 
 ## Dependency to use
 대기오염정보를 조회하기 위해선 아래의 라이브러리/API 키가 필요합니다
 >pytz\
 >[대기오염정보 조회 서비스](https://www.data.go.kr/dataset/15000581/openapi.do) API 키
 
 ## How to use
 현재 위치의 구, API 키를 인자로 하여 get_fine_dict_data 함수를 실행합니다.
 ```python
get_fine_dict_data(service_key, '광진구')
```
예를 들어, 광진구의 실시간 기상정보를 불러오기 위해서 위와 같이 입력합니다.\
2018년 11월 17시 3시 기준 출력값은\
`fine_dust = 2, Ultrafine_dust = 2, dataTime = 2018-11-17 03:00`입니다.

## Output
    fine_dust : 미세먼지
    Ultrafine_dust : 초미세먼지
          (좋음 : 1, 보통 : 2, 나쁨 : 3, 매우나쁨 : 4)
    dataTime : 미세먼지 추출 시간
    
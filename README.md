<h1 align="center">Sejong_ITIP</h1>
날씨와 거리를 기반으로 서울에서 갈만한 장소를 추천해줍니다.

## API
- 아래 API들을 받아야 프로그램을 실행할 수 있습니다.
- 날씨 : https://www.data.go.kr/dataset/15000099/openapi.do
- 미세먼지 : https://www.data.go.kr/dataset/15000581/openapi.do
- 구글맵 : https://cloud.google.com/maps-platform/?hl=ko

## Data
서울에 갈만한 장소를 정리합니다. 아래는 해당 데이터들의 Attribute value입니다.

### Name
- 장소의 이름을 기제합니다.

### Function
- 장소의 대분류를 기제합니다.

### Details
- 장소의 상세설명을 기제합니다.

### Day
- 장소의 이용가능 시간을 기제합니다.

### Score
- 장소에 대한 Google의 Score 기제합니다.
- 추천을 할 때에는 거리, 날씨 등에 맞게 점수를 갱신합니다.

### Indoor/Outdoors
- 장소가 내부에 있는지 외부에 있는지 기제합니다.

### Longitude
- 장소의 경도를 기제합니다.

### Latitude
- 장소의 위도를 기제합니다.

### Show density of Data  
![](map.PNG)


## 개발 방법
1. 사용자의 현재 위치 및 날씨정보 받기

2. 이용시간에 따라 장소 필터링

3. 날씨 정보에 따라 장소 필터링

4. 사용자 주변위치 위주로 필터링

5. 과정3에서 필터링한 정보가 적으면 주변으로 확대

6. 날씨, 거리 정보로 스코어 추가

7. 스코어를 기준으로 Random-roulette을 돌려서 추천 장소 선택

8. 다양한 장소 추천 크롤링한 정보들과 사진등을 표시하며 몇 가지 장소를 추천

![](result.PNG)

## 예제

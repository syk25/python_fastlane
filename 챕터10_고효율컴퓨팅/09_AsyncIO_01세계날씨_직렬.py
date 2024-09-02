"""
1. concurrent_work()를 동시성으로 수행해서 더 빠르게 만들기
2. 전역 변수 city_temperature 제거
3. run_in_executor() 사용
"""

import requests
import time


class Timer:
    def __init__(self):
        self.start = time.perf_counter()

    def __enter__(self):
        return self  # as로 사용할 수 있도록 self 반환

    def __exit__(self, *args):
        print("Elapsed time = ", time.perf_counter() - self.start)


cities = [
    "Seoul",
    "Pusan",
    "Paris",
    "London",
    "Cairo",
    "Lagos",
    "Giza",
    "Los Angeles",
    "San Francisco",
    "New York",
]

API_KEY = "YOUR_KEY_HERE"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
LANGUAGE = "kr"  # 출력 중 Weather에 한국어로 받을 수 있음. 영어를 원하면 "en"이나 생략

# 날씨 가져오기를 동시성으로 수정
def concurrent_work(city):

    global city_temperature

    request_url = f"{BASE_URL}?appid={API_KEY}&q={city}&lang={LANGUAGE}"
    response = requests.get(request_url)
    if response.status_code == 200:
        data = response.json()
        city_name = data["name"]
        temperature = round(data["main"]["temp"] - 273.15, 2)

        print(city_name, temperature)
        city_temperature[city_name] = temperature

    else:
        print("An error occurred.", response.status_code)


# 전역변수 제거
city_temperature = {}  # empty dict

with Timer():
    for city in cities:
        concurrent_work(city)

city_sorted = dict(
    sorted(city_temperature.items(), key=lambda item: item[1], reverse=True)
)

print("가장 더운 도시:", next(iter(city_sorted)))
print(city_sorted)

# Elapsed time =  1.9664716000006592

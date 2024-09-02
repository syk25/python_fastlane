# [실습] 온도가 가장 높은 도시 찾기 (AsyncIO)

# import requests
import aiohttp  # pip install aiohttp
import asyncio
import time


class Timer:
    def __init__(self):
        self.start = time.time()

    def __enter__(self):
        return self  # as로 사용할 수 있도록 self 반환

    def __exit__(self, *args):
        print("Elapsed time = ", time.time() - self.start)


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
LANGUAGE = "kr"


async def concurrent_work(city):

    request_url = f"{BASE_URL}?appid={API_KEY}&q={city}&lang={LANGUAGE}"

    async with aiohttp.ClientSession() as session:
        response = await session.get(request_url)
        if response.status == 200:
            data = await response.json()
            city_name = data["name"]
            temperature = round(data["main"]["temp"] - 273.15, 2)
            return {city_name: temperature}
        else:
            print("An error occurred.", response.status_code)
            return {}  # 정보를 받지 못한 도시는 제외


async def main():
    return await asyncio.gather(*(concurrent_work(city) for city in cities))


if __name__ == "__main__":
    with Timer():
        result = asyncio.run(main())  # return을 사용하도록 수정
        result = {k: v for i in result for k, v in i.items()}

    city_sorted = dict(sorted(result.items(), key=lambda item: item[1], reverse=True))

    print(city_sorted)

# RealPython 참고: https://realpython.com/async-io-python/

# Elapsed time =  0.18180084228515625

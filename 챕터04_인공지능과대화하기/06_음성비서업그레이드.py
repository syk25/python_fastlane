import speech_recognition as sr
from datetime import datetime
from pytz import timezone
from io import BytesIO
from navertts import NaverTTS
from pydub import AudioSegment
from pydub.playback import play
import requests
from collections.abc import Callable


def speech_to_text() -> str:
    """음성 인식

    마이크로 사용자의 음성을 듣고 결과를 문자열로 반환

    Args:
        마이크와 음성인식기를 함수 안에서 초기화하기 때문에 인수 없음

    Returns:
        str: 음성 인식 결과 문자열. 실패시 빈 문자열 반환.
    """


def text_to_speech(text: str) -> None:
    """음성 합성

    입력받은 문자열을 print()로 출력하고 TTS로 스피커로 출력

    Args:
        text (str): 음성 합성할 문자열
    """


def report_daytime(user_command: str) -> None:
    """시간과 날짜 안내

    user_command에 "시간"이 포함되어 있으면 현재 시간 안내
    user_command에 "날짜"가 포함되어 있으면 현재 날짜 안내
    user_command에 도시 이름이 포함되어 있을 경우에는 그 도시 기준, 그렇지 않으면 기본 도시(예: "서울") 기준

    Args:
        user_command (str): 도시 이름을 찾아볼 사용자 명령문
    """

    cities_dict = {
        "서울": "Asia/Seoul",
        "뉴욕": "America/New_York",
        "로스앤젤레스": "America/Los_Angeles",
        "파리": "Europe/Paris",
        "런던": "Europe/London",
    }


def report_weather(user_command: str) -> None:
    """날씨 안내

    현재 날씨를 text_to_speech()를 사용해서 안내
    user_command에 도시 이름이 포함되어 있을 경우에는 그 도시의 날씨를 안내하고
    그렇지 않을 경우 기본 도시(예: "서울")의 날씨를 안내

    Args:
        user_command (str): 도시 이름을 찾아볼 사용자 명령문
    """

    API_KEY = "YOUR_KEY_HERE"
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
    LANGUAGE = "kr"

    cities_dict = {
        "서울": "seoul",
        "뉴욕": "new york",
        "로스앤젤레스": "los angeles",
        "파리": "paris",
        "런던": "london",
    }


def find_keyword(keywords: list[str], sentence: str, default: str = "") -> str:
    """주어진 문장에서 가장 처음 발견되는 keyword 반환

    Args:
        keywords (list[str]): 찾고자 하는 키워드의 리스트 예) ["날씨", "시간"]
        sentence (str): 키워드를 찾아볼 문장 예) "날씨를 알려주세요"
        default (str): 키워드가 하나도 없을 경우 반환할 문자열

    Returns:
        str: 문장 안에서 처음 발견한 키워드. 없을 경우 default 반환.
    """

    for k in keywords:
        if k in sentence:
            return k

    return default


# [보충] 여기서 Callable[[str], None]은 str을 입력으로 받고 None을 반환하는 함수의 타입힌트입니다.
def listen_and_report(command_callbacks: dict[str, Callable[[str], None]]) -> bool:
    """마이크를 통해 음성을 입력받고 명령을 수행

    1. speech_to_text() 함수로 사용자 음성으로부터 명령문 인식
    2. 인식된 명령문에 "종료"가 포함되어 있을 경우 "종료합니다." 음성 안내 후 False 반환
    3. 인식된 명령문에 command_callbacks의 key에 해당하는 단어가 포함되어 있을 경우 함수 객체 실행

    Args:
        command_callbacks (dict[str, function]): 명령문에 key가 포함되었을 경우 value 함수 실행

    Returns:
        bool: 프로그램을 계속 진행할 경우 True, 종료할 경우 False
    """


command_callbacks = {
    "시간": report_daytime,
    "날씨": report_weather,
}

while listen_and_report(command_callbacks):
    continue

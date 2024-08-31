import speech_recognition as sr
import datetime
from io import BytesIO
from navertts import NaverTTS
from pydub import AudioSegment
from pydub.playback import play
import requests

r = sr.Recognizer()
microphone = sr.Microphone(device_index=1)  # 대부분의 경우 device_index 생략 가능


API_KEY = "d442bd5f7833de15009628bf72c19e74"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
LANGUAGE = "kr"  # 출력 중 Weather에 한국어로 받을 수 있음. 영어를 원하면 "en"이나 생략


r = sr.Recognizer()
microphone = sr.Microphone(device_index=1)

print("날짜와 시간을 알려주는 프로그램!")


while True:
    # 음성인식
    with microphone as source:
        r.adjust_for_ambient_noise(source)
        print("음성 인식 대기중")
        audio = r.listen(source)

    speech = None
    finished = False
    try:
        text = r.recognize_google(audio, language="ko")
    except:
        speech = "이해할 수 없는 명령입니다."
    else:
        if "날짜" in text:
            speech = f"오늘 날짜는 {datetime.date.today().year}년 {datetime.date.today().month}월 {datetime.date.today().day}일 입니다."
            print(speech)
        elif "시간" in text:
            speech = f"현재 시간은 {datetime.datetime.now().hour}시 {datetime.datetime.now().minute}분 {datetime.datetime.now().second}초 입니다."
        elif "날씨" in text:
            city = "seoul"
            request_url = f"{BASE_URL}?appid={API_KEY}&q={city}&lang={LANGUAGE}"

            response = requests.get(request_url)  # 웹브라우저에 똑같이 사용

            if response.status_code == 200:  # HTTP status 200은 성공을 의미합니다.

                data = response.json()
                city_name = data["name"]
                weather = data["weather"][0]["description"]
                temperature = round(data["main"]["temp"] - 273.15, 2)  # 켈빈 온도 사용
                
                speech = f"현재 {city_name}의 날씨는 {weather}입니다. 온도는 {temperature}도 입니다."

            else:
                print("An error occurred.", response.status_code)

        elif "종료" in text:
            speech = "종료합니다."
            finished = True
        else:
            speech = "실행할 수 없는 명령입니다."

        tts = NaverTTS(speech, lang="ko")
        fp = BytesIO()
        tts.write_to_fp(fp)
        fp = BytesIO(fp.getvalue())
        my_sound = AudioSegment.from_file(fp, format="mp3")
        play(my_sound)
        if finished:
            break
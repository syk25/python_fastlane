import speech_recognition as sr
import gtts
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play
import datetime

r = sr.Recognizer()

microphone = sr.Microphone()


while True:

    # 음성합성
    print("음성명령을 기다리는 중입니다.")
    tts = gtts.gTTS("음성명령을 기다리는 중입니다.", lang="ko")

    fp = BytesIO()
    tts.write_to_fp(fp)
    fp = BytesIO(fp.getvalue())

    my_sound = AudioSegment.from_file(fp, format="mp3")
    play(my_sound)

    # 음성인식
    with microphone as source:
        r.adjust_for_ambient_noise(source)  # 배경 소음을 측정합니다.
        audio = r.listen(source)  # 일정 크기 이상의 소리가 들리면 녹음합니다.
    text = r.recognize_google(audio, language="ko")

    if "날씨" in text:
        print(f"음성 인식 결과: {text}")
    elif "시간" in text:
        print(f"음성 인식 결과: {text}")
        hour = datetime.datetime.now().hour
        minute = datetime.datetime.now().minute

        print(f"지금은 {hour}시 {minute}분 입니다.")
        tts = gtts.gTTS(f"지금은 {hour}시 {minute}분 입니다.", lang="ko")
        fp = BytesIO()
        tts.write_to_fp(fp)
        fp = BytesIO(fp.getvalue())
        my_sound = AudioSegment.from_file(fp, format="mp3")
        play(my_sound)
    elif "날짜" in text:
        print(f"음성 인식 결과: {text}")

        today_date = f"오늘은 {datetime.date.today().year}년 {datetime.date.today().month}월 {datetime.date.today().day}일 입니다."
        print(today_date)

        tts = gtts.gTTS(today_date, lang="ko")
        fp = BytesIO()
        tts.write_to_fp(fp)
        fp = BytesIO(fp.getvalue())
        my_sound = AudioSegment.from_file(fp, format="mp3")
        play(my_sound)

    elif "종료" in text:
        print("종료합니다.")
        break
    else:
        print(f"음성 인식 결과: {text}")
        print("알 수 없는 명령입니다.")
        tts = gtts.gTTS("알 수 없는 명령입니다.", lang="ko")

        fp = BytesIO()
        tts.write_to_fp(fp)
        fp = BytesIO(fp.getvalue())

        my_sound = AudioSegment.from_file(fp, format="mp3")
        play(my_sound)

""" TODO: 코드의 중복: 눈에 잘 들어오지도 않고 고치기도 어렵고 힘들다 -> 중복 제거하자! """

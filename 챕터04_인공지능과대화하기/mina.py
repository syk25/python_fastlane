import speech_recognition as sr

from io import BytesIO

from navertts import NaverTTS

from pydub import AudioSegment
from pydub.playback import play

import datetime



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

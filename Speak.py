import speech_recognition as sr
import keyboard
import pyttsx3
import os
import re
import g4f
g4f.debug.logging = True  # Enable logging
g4f.check_version = False  # Disable automatic version checking
print(g4f.version)  # Check version
print(g4f.Provider.Ails.params)  # Supported args


from g4f.Provider import (
    AItianhu,
    Aichat,
    Bard,
    Bing,
    ChatBase,
    ChatgptAi,
    OpenaiChat,
    Vercel,
    You,
    Yqcloud,
)

# cam switch if you want
_providers = [
    g4f.Provider.Aichat,
    g4f.Provider.ChatBase,
    g4f.Provider.Bing,
    g4f.Provider.GptGo,
    g4f.Provider.You,
    g4f.Provider.Yqcloud,
]

# TTS 엔진 초기화
engine = pyttsx3.init()
voices = engine.getProperty('voices')
# 여성 목소리 선택 (Windows에는 여러 여성 음성이 있을 수 있음)
# engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\SPEECH_OneCore\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0')  
engine.setProperty('voice', voices[2].id)
engine.setProperty('voice', 'en-US')

# 설정 변경
engine.setProperty('volume', 1.0)  # 볼륨 설정 (0.0부터 1.0까지)
engine.setProperty('rate', 200)  # 읽는 속도 설정 (기본 값: 200, 더 느리게 하려면 값 낮춤)

# 음성 인식 객체 생성
recognizer = sr.Recognizer()

# 'esc' 키를 누를 때까지 반복
while not keyboard.is_pressed('esc'):
    # 's' 키를 눌렀을 때 음성 인식 시작
    if keyboard.is_pressed('s'):
        with sr.Microphone() as source:
            print("Recording...")
            audio = recognizer.listen(source, phrase_time_limit=10)
        try:
            recognized_text = recognizer.recognize_google(audio, language="en-US")
            print("User Say: " + recognized_text)

            # Normal response
            response = g4f.ChatCompletion.create(
                model=g4f.models.gpt_4,
                provider=g4f.Provider.Bing,
                messages=[{"role": "user", "content": f"{recognized_text}"}],
            )  # Alternative model setting
            
            pattern1 = re.compile(r'\[.*?\]: https?://\S+ ""')
            pattern2 = re.compile(r'\[\^\d\^\]\[\d\]')
            cleaned_sentence = re.sub(pattern1, '', response)
            cleaned_sentence = re.sub(pattern2, '', cleaned_sentence)
            print("GPT response : ", response)
            print("Normalize : ",cleaned_sentence.strip())
            
            if response:
                engine.say(f"{cleaned_sentence.strip()}")

            # 음성 재생
            engine.runAndWait()

        except sr.UnknownValueError:
            print("Can't Recognize.")
        except sr.RequestError as e:
            print("Error: {0}".format(e))
        





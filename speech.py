import speech_recognition as sr

# Initialize recognizer class (for recognizing the speech)
r = sr.Recognizer()
m = sr.Microphone()

# A list
sentences = []

try:
    print("A moment of silence, please...")
    with m as source: r.adjust_for_ambient_noise(source) # we only need to calibrate once, before we start listening
    print("Set minimum energy threshold to {}".format(r.energy_threshold))
    
    while True:
        print("Say something!")
        with m as source: audio = r.listen(source, phrase_time_limit=10) # wait for 10 secs to detect speech
        print("Got it! Now to recognize it...")
        
        try:
            # recognize speech using Google Speech Recognition
            value = r.recognize_google(audio)
            sentences.append(value)
            print("You said {}".format(value))
        except sr.UnknownValueError:
            print("Oops! Didn't catch that")
        except sr.RequestError as e:
            print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
except KeyboardInterrupt:
    pass
import speech_recognition as sr
import urllib.request

# Initialize recognizer class (for recognizing the speech)
r = sr.Recognizer()
m = sr.Microphone()

# A list
sentences = []

# try:
#     print("A moment of silence, please...")
#     with m as source: r.adjust_for_ambient_noise(source) # we only need to calibrate once, before we start listening
#     print("Set minimum energy threshold to {}".format(r.energy_threshold))
#     # Blink twice when ready
#     url = 'https://maker.ifttt.com/trigger/{}/with/key/NzX9u8NuVPaFWZyqQRhlv'.format('system_ready')
#     urllib.request.urlopen(url) 
    
#     while True:
#         print("Say something!")
#         with m as source: audio = r.listen(source, phrase_time_limit=10) # wait for 10 secs to detect speech
#         print("Got it! Now to recognize it...")
        
#         try:
#             # recognize speech using Google Speech Recognition
#             value = r.recognize_google(audio)
#             sentences.append(value)
#             print("You said {}".format(value))
#         except sr.UnknownValueError:
#             print("Oops! Didn't catch that")
#         except sr.RequestError as e:
#             print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
# except KeyboardInterrupt:
#     pass

def listen(): 
    sentences = []
    with sr.Microphone() as source:
        print("Talk")
        audio_text = r.listen(source)
        print("Time over, thanks")
    
    # recoginize_() method will throw a request error if the API is unreachable, hence using exception handling    
        try:
            # using google speech recognition
            value = r.recognize_google(audio_text)
            sentences.append(value)
            print("Text:" + value)
            return sentences
        except:
            print("Sorry, I did not get that")

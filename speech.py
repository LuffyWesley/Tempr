#import library
import speech_recognition as sr

# Initialize recognizer class (for recognizing the speech)
r = sr.Recognizer()

# A list
sentences = []

# Reading Microphone as source
# listening the speech and store in audio_text variable
with sr.Microphone() as source:
    print("Talk")
    audio_text = r.listen(source)
    print("Time over, thanks")

# recoginize_() method will throw a request error if the API is unreachable, hence using exception handling    
    try:
        # using google speech recognition
        capture = r.recognize_google(audio_text)
        sentences.append(capture)
        print("Text:" + capture)
    except:
        print("Sorry, I did not get that")  
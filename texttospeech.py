import pyttsx3

speechengine=pyttsx3.init()

voices = speechengine.getProperty('voices')
speechengine.setProperty('voice', voices[2].id)

#enter the string here
string="Today is a beautiful day and i want everything i can have in my life"
speechengine.setProperty("rate",125)
speechengine.setProperty("gender","female")
speechengine.save_to_file(string,"string.wav")
speechengine.runAndWait()
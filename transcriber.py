from pydoc import TextDoc
from xml.etree.ElementTree import tostring
from flask import Flask, render_template, request, Response
import arabic_reshaper
from bidi.algorithm import get_display

app = Flask("transcription_app") #making an app

@app.route("/")    #@ makes it a 'decorator'. line tells peple where to look inside flask framework. Decorators always followed by function.
def landing_page():
    return render_template("transcriber_page.html")

@app.route("/transcribed", methods=['POST'])
def transcribe():
    
    form_data = request.form[inputText]
    string_of_text = tostring(form_data)
    TextToTranscribe = list(string_of_text)

    #mapping
    characters = {
    " " : " ",
    "ʾ" : "ء",
    "b" :"ب",
    "t" : "ت",
    "th" : "ث",
    "T" : "ط",
    "Th" : "ظ",
    "ẓ" : "ظ",
    "j" : "ج",
    "H" : "ح",
    "ḥ" : "ح",
    "ch": "خ",
    "kh": "خ",
    "d" : "د",
    "dh" : "ذ",
    "r" : "ر",
    "z" : "ز",
    "s" : "س",
    "sh" : "ش",
    "ṣ" : "ص",
    "S" : "ص",
    "ḍ" : "ض",
    "D" : "ض",
    "ʿ" : "ع",
    "gh" : "غ",
    "q" : "ق",
    "f" : "ف",
    "k" : "ك",
    "l" : "ل",
    "m" : "م",
    "n" : "ن",
    "h" : "ه",
    "w": "و",
    "'" : "", #needs rule
    "a" : "َ" , #needs rule
    "a" : "ة", #needs rule
    "at" : "ة", #needs rule
    "ā" : "ا", #needs rule
    "ā" : "ی", #needs rule
    "ū" : "و" , #needs rule
    "ī" : "ي" , #needs rule
    "aa" : "ا" , #needs rule
    "u" : "ُ" , #needs rule
    "o" : "ُ" , #needs rule
    "uu" : "و" , #needs rule
    "oo" : "و" , #needs rule
    "i" : "ِ" , #needs rule
    "ii" : "ي" , #needs rule
    "iyy" : "ّي ِ", #needs rule
    "uww" : "ّو ُ", #needs rule
    "ee" : "ي" , #needs rule
    "y": "ي" #needs rule
    }

    transcriber_result = ' '.join(characters[character] for character in TextToTranscribe)
    reshaped_text = arabic_reshaper.reshape(transcriber_result)
    print(reshaped_text)
    bidi_text = get_display(reshaped_text)
    print(bidi_text)
    transcribed_text = bidi_text
    print (transcribed_text)
    return render_template("transcriber_page.html")

#transliteration source https://www.cambridge.org/core/services/aop-file-manager/file/57d83390f6ea5a022234b400/TransChart.pdf

app.run(debug=True) #runs the app. the debug part - unlocks debugging feature.

#e.g. bidi for ref
#print("إسمي ماجي"); #translation: 'my name is Maggie' - prints backwards and disjointed
#print ("يجام يمسإ"); #'my name is Maggie', typed bacwards so prints right way, still disjointed
# #my_text = "إسمي ماجي";
#reshaped_text = arabic_reshaper.reshape(my_text);    # correct its shape - links the letters
#print(reshaped_text); #joined up forms of the letters, but still going in the wrong direction
#bidi_text = get_display(reshaped_text);           # correct its direction - right to left
#print(bidi_text);
from encodings.utf_8 import encode
from pickle import OBJ
from pydoc import TextDoc
from xml.etree.ElementTree import tostring
from flask import Flask, render_template, request, Response
import arabic_reshaper
from bidi.algorithm import get_display
import base64
import io

app = Flask("transcription_app") #making an app

@app.route("/")    #@ makes it a 'decorator'. line tells peple where to look inside flask framework. Decorators always followed by function.
def landing_page():
    return render_template("transcriber_page.html")

@app.route("/transcribed", methods=["POST", "GET"]) 
def transcribe():

    inputTextFromForm = str(request.form['inputText'])
    print(inputTextFromForm)
    TextToTranscribe = list(inputTextFromForm)
    print(TextToTranscribe)

    #mapping - Eng to Arabic
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
    "ch": "خ", #needs rule
    "kh": "خ", #needs rule
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
    "ii" : "ي" , #needs rule
    "i" : "ِ" , #needs rule
    "iyy" : "ّي ِ", #needs rule
    "uww" : "ّو ُ", #needs rule
    "ee" : "ي" , #needs rule
    "y": "ي", #needs rule
    #other letters which may come up
    "e": "", #needs rule
    "c": "", #needs rule
    "x": "", #needs rule
    "d": "", #needs rule
    "g": "", #needs rule
    "p": "", #needs rule
    "v": "", #needs rule
    "w": "", #needs rule
    '\n':'\n',
    '\r': '\r',
    " " : " "
    }

    transcriber_result = ''.join(characters[character] for character in TextToTranscribe)
    reshaped_text = arabic_reshaper.reshape(transcriber_result)
    print(reshaped_text)
    bidi_text = get_display(reshaped_text, upper_is_rtl=True)
    print(bidi_text)
    transcribed_text = str(bidi_text)
    print (transcribed_text)

    file = open('transliteration.txt', 'w')
    with open('transliteration.txt', 'w') as file:
        file.write(transcribed_text)
    with open('transliteration.txt', 'r') as file:
        file.seek(0)
        bytesfile = (encode(str(file)))
        print(bytesfile)
        doc_url = base64.b64encode(dict(bytesfile))
        print (doc_url)



    return render_template("transcriber_page.html", transcribed_text=transcribed_text, doc_url=doc_url)

#isn't printing on html the right way
#transliteration source https://www.cambridge.org/core/services/aop-file-manager/file/57d83390f6ea5a022234b400/TransChart.pdf

app.run(debug=True) #runs the app. the debug part - unlocks debugging feature.
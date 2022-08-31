from encodings.utf_8 import encode
from pickle import OBJ
from pydoc import TextDoc
from xml.etree.ElementTree import tostring
from flask import Flask, render_template, request, Response
import arabic_reshaper
from bidi.algorithm import get_display
import base64
import io
import os

app = Flask("Transliterator_app") #making an app

@app.route("/")    #@ makes it a 'decorator'. line tells peple where to look inside flask framework. Decorators always followed by function.
def landing_page():
    return render_template("index.html")

@app.route("/transliterator", methods=["POST", "GET"]) 
def transliterate():

    inputTextFromForm = str(request.form['inputText'])
    print(inputTextFromForm)
    TextTotransliterate = list(inputTextFromForm)
    print(TextTotransliterate)

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
    "w": "و", #needs rule
    "'" : "", #needs rule
    "a" : "َ" , #needs rule
    "a" : "ة", #needs rule
    "at" : "ة", #needs rule
    "A" : "ا", #needs rule
    "ā" : "ی", #needs rule
    "ā" : "ا", #needs rule
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
    "?" : "؟"
    }
    #need to look for combinations of letters
    # transliterator_result = ''.join(characters[character] for character in TextTotransliterate)
    transliterator_result = ""
    for character in TextTotransliterate:
        if character in characters:
            X = characters[character]
        else:
            X = character
        transliterator_result = transliterator_result+X
        
    transliterator_text = arabic_reshaper.reshape(transliterator_result)
    print(transliterator_text)
    #necessary for future text and downloads but not html display
    bidi_text = get_display(transliterator_text, upper_is_rtl=True)
    print (bidi_text)



    return render_template("index.html", transliterator_text=transliterator_text)

#isn't printing on html the right way
#transliteration source https://www.cambridge.org/core/services/aop-file-manager/file/57d83390f6ea5a022234b400/TransChart.pdf

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
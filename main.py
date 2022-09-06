from curses import keyname
from encodings.utf_8 import encode
from importlib.machinery import all_suffixes
from pickle import FALSE, OBJ, TRUE
from pydoc import TextDoc
from wave import Wave_write
from xml.etree.ElementTree import tostring
from flask import Flask, render_template, request, Response
import arabic_reshaper
from bidi.algorithm import get_display
import base64
import io
import os
# from bidict import bidict

app = Flask("Transliterator_app") #making an app

@app.route("/")    #@ makes it a 'decorator'. line tells peple where to look inside flask framework. Decorators always followed by function.
def landing_page():
    return render_template("index.html")

@app.route("/transliterator", methods=["POST", "GET"]) 
def transliterate():

    unhandled_letters = []
    inputTextFromForm = str(request.form['inputText'])
    print("input = "+ inputTextFromForm)

    lower_inputTextFromForm = inputTextFromForm.lower()+" "
    print("lower case = " + lower_inputTextFromForm)

    #replacing character combinations on official transliteration to enable accurate transcription
    lower_inputTextFromForm1 = lower_inputTextFromForm.replace("th", "V")
    lower_inputTextFromForm2 = lower_inputTextFromForm1.replace("gh", "G")
    lower_inputTextFromForm3 = lower_inputTextFromForm2.replace("kh", "K")
    lower_inputTextFromForm4 = lower_inputTextFromForm3.replace("dh", "D")
    lower_inputTextFromForm5 = lower_inputTextFromForm4.replace("sh", "S")
    lower_inputTextFromForm6 = lower_inputTextFromForm5.replace("iyy", "I")
    lower_inputTextFromForm7 = lower_inputTextFromForm6.replace("uww", "U")
    lower_inputTextFromForm8 = lower_inputTextFromForm7.replace("ā ", "A ")
    lower_inputTextFromForm9 = lower_inputTextFromForm8.replace("at ", "T ")
    lower_inputTextFromForm10 = lower_inputTextFromForm9.replace("a ", "T ")
    lower_inputTextFromForm11 = lower_inputTextFromForm10.replace("x", "ks")
    lower_inputTextFromForm12 = lower_inputTextFromForm11.replace("ya", "īa")
    lower_inputTextFromForm13 = lower_inputTextFromForm12.replace("wa", "ūa")
    lower_inputTextFromForm14 = lower_inputTextFromForm13.replace("yi", "īi")
    lower_inputTextFromForm15 = lower_inputTextFromForm14.replace("wi", "ūi")
    lower_inputTextFromForm16 = lower_inputTextFromForm15.replace("yu", "īu")
    lower_inputTextFromForm17 = lower_inputTextFromForm16.replace("wu", "ūu")
    lower_inputTextFromForm18 = lower_inputTextFromForm17.replace("ʾa", "X")
    lower_inputTextFromForm19 = lower_inputTextFromForm18.replace("ʾu", "W")
    lower_inputTextFromForm20 = lower_inputTextFromForm19.replace("ʾi", "Q")
    lower_inputTextFromForm21 = lower_inputTextFromForm20.replace("ʾā", "Z")
    lower_inputTextFromForm22 = lower_inputTextFromForm21.replace(" al", " āl")
    lower_inputTextFromForm23 = lower_inputTextFromForm22.replace("ﺃ", "ءا")
    lower_inputTextFromForm24 = lower_inputTextFromForm23.replace("ﺇ", "ءي")
    lower_inputTextFromForm25 = lower_inputTextFromForm24.replace("ؤ", "ءو")
    lower_inputTextFromForm26 = lower_inputTextFromForm25.replace("ﺉ", "ءﻯ")

    TextTotransliterate = list(lower_inputTextFromForm22)
    print("to transliterate "+ str(TextTotransliterate))

    #mapping
    characters = {
    "ʾ" : "ء",
    "b" :"ب",
    "t" : "ت",
    "V" : "ث",
    "ṭ" : "ط",
    "ẓ" : "ظ",
    "j" : "ج",
    "ḥ" : "ح",
    "K": "خ",
    "d" : "د",
    "D" : "ذ",
    "r" : "ر",
    "I" : "ّي ِ",
    "U" : " ّو ُ",
    "z" : "ز",
    "s" : "س",
    "S" : "ش",
    "ṣ" : "ص", 
    "ḍ" : "ض",
    "ʿ" : "ع",
    "gh" : "غ",
    "q" : "ق",
    "f" : "ف",
    "k" : "ك",
    "l" : "ل",
    "m" : "م",
    "n" : "ن",
    "h" : "ه",
    "a" : "َ" ,
    "T" : "ة",
    "ā" : "ا", 
    "A" : "ى", 
    "ū" : "و" , 
    "ī" : "ي" ,
    "u" : "ُ" , 
    "i" : "ِ" ,
    "?" : "؟",
    "ء" : "ʾ" ,
    "ب" : "b" ,
    "ت" : "t" ,
    "ث" : "V" ,
    "ط" : "ṭ" ,
    "ظ" : "ẓ" ,
    "ج" : "j" ,
    "ح" : "ḥ" ,
    "خ" : "K" ,
    "د" : "d" ,
    "ذ" : "D" ,
    "ر" : "r" ,
    " ِ" : "I" ,
    " ُ" : "U" ,
    "ز" : "z" ,
    "س" : "s" ,
    "ش" : "S" ,
    "ص"  : "ṣ" ,
    "ض" : "ḍ" ,
    "ع" : "ʿ" ,
    "غ" : "gh" ,
    "ق" : "q" ,
    "ف" : "f" ,
    "ك" : "k" ,
    "ل" : "l" ,
    "م" : "m" ,
    "ن" : "n" ,
    "ه" : "h" ,
    "َ"  : "a" ,
    "ة" : "T" ,
    "ا"  : "ā" ,
   "ى" : "A" ,
    "و" : "ū" ,
    "ي"  : "ī" ,
    "ُ"  : "u" ,
    "ِ" : "i" ,
    "؟" : "?",
    "X" : "أ",
    "W" : "ؤ",
    "Q" : "إ",
    "Z" : "ئ",
    "أ" : "X",
    "ؤ" : "W",
    "إ" : "Q",
    "ئ" : "Z",
    "،" : ",",
    "," : "،",
    "ﹼ" : "",
    "-" : ""}

    #todo add numbers
    #transliteration source https://www.cambridge.org/core/services/aop-file-manager/file/57d83390f6ea5a022234b400/TransChart.pdf

    #two-way dictionary
        # bidict_lookup_arabic_characters=bidict(characters)
        # bidict_lookup_western_characters = bidict_lookup_arabic_characters.inverse
        # print(bidict_lookup_western_characters)
        # transliterator_result = ''.join(characters[character] for character in TextTotransliterate)
    transliterator_result = ""
    input_lang_ar = False
    
    for character in TextTotransliterate:
        ar_char = arabic_reshaper.reshape(character)
        print(ar_char)
        if character in characters:
            print ("lookup")
            X = characters[character]
            if ('\u0600' <= character <= '\u06FF' or
                '\u0750' <= character <= '\u077F' or
                '\u08A0' <= character <= '\u08FF' or
                '\uFB50' <= character <= '\uFDFF' or
                '\uFE70' <= character <= '\uFEFF' or
                '\U00010E60' <= character <= '\U00010E7F' or
                '\U0001EE00' <= character <= '\U0001EEFF'):
                input_lang_ar =  True
            else:
                print("not ar")
        # elif ar_char in bidict_lookup_arabic_characters.inverse:
        #     print(character)
        #     print ("lookup western")
        #     print(ar_char)
        #     X = bidict_lookup_western_characters[character]
        #     X = bidict_lookup_arabic_characters.inverse[character]
        else:
            print ("no lookup")
            X = character
            unhandled_letters.append(X)
        transliterator_result = transliterator_result+X
    
    
    #replacing replacements' to match official transliteration with character combinations
    transliterator_result1 = transliterator_result.replace("V", "th")
    transliterator_result2 = transliterator_result1.replace("G", "gh")
    transliterator_result3 = transliterator_result2.replace("K", "kh")
    transliterator_result4 = transliterator_result3.replace("D", "dh")
    transliterator_result5 = transliterator_result4.replace("S", "sh")
    transliterator_result6 = transliterator_result5.replace("I", "iyy")
    transliterator_result7 = transliterator_result6.replace("U", "uww")
    transliterator_result8 = transliterator_result7.replace("A", "ā")
    transliterator_result9 = transliterator_result8.replace("T", "a(t)")
    transliterator_result10 = transliterator_result9.replace("īa", "ya")
    transliterator_result11 = transliterator_result10.replace("ūa", "wa")
    transliterator_result12 = transliterator_result11.replace("īi", "yi")
    transliterator_result13 = transliterator_result12.replace("ūi", "wi")
    transliterator_result14 = transliterator_result13.replace("īu", "yu")
    transliterator_result15 = transliterator_result14.replace("ūu", "wu")
    transliterator_result16 = transliterator_result15.replace(" āl", " al")
    transliterator_result17 = transliterator_result16.replace("aā", "ā")
    transliterator_result18 = transliterator_result17.replace("iī", "ī")
    transliterator_result19 = transliterator_result18.replace("uū", "ū")
    transliterator_result20 = transliterator_result19.replace("Q", "'i")
    transliterator_result21 = transliterator_result20.replace("Z","'ā")
    transliterator_result22 = transliterator_result21.replace(" al", " al-")
    transliterator_result23 = transliterator_result22.replace("W", "'u")
    transliterator_result24 = transliterator_result23.replace("X", "'a")
    transliterator_result25 = transliterator_result24.replace(" ū", " w-")
    transliterator_result26 = transliterator_result25.replace(" fal-", " f'al-")
   

    transliterator_reshaped = arabic_reshaper.reshape(transliterator_result26)

    if input_lang_ar == True:
        transliterator_text_qmark = '? '.join(x.capitalize() for x in transliterator_reshaped.split('? '))
        transliterator_text_emark = '! '.join(x.capitalize() for x in transliterator_text_qmark.split('! '))
        transliterator_text = '. '.join(x.capitalize() for x in  transliterator_text_emark.split('. '))

    else:
        #linking cursive up
        print("ok")
        transliterator_text = transliterator_reshaped
    
    
    

    print(transliterator_text)

    #adjusting direction - necessary for backend but not html display
    bidi_text = get_display(transliterator_text, upper_is_rtl=True)
    print (bidi_text)

    # if input_lang_ar:
    #     input_direction="<span dir=\"rtl\">"
    #     output_direction="<span dir=\"ltr\">"
    # else:
    #     input_direction="<span dir=\"ltr\">"
    #     output_direction="<span dir=\"rtl\">"

   
    

    print(input_lang_ar)
    print(set(unhandled_letters))
    return render_template("index.html", input_lang_ar=input_lang_ar, inputTextFromForm=inputTextFromForm, transliterator_text=transliterator_text)



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
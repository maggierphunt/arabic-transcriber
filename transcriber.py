from flask import Flask, render_template, request, Response
import arabic_reshaper
from bidi.algorithm import get_display

app = Flask("transcription_app") #making an app

@app.route("/")    #@ makes it a 'decorator'. line tells peple where to look inside flask framework. Decorators always followed by function.
def landing_page():
    return render_template("transcriber_page.html")

app.run(debug=True) #runs the app. the debug part - unlocks debugging feature.

#e.g. bidi for ref
#print("إسمي ماجي"); #translation: 'my name is Maggie' - prints backwards and disjointed
#print ("يجام يمسإ"); #'my name is Maggie', typed bacwards so prints right way, still disjointed
# #my_text = "إسمي ماجي";
#reshaped_text = arabic_reshaper.reshape(my_text);    # correct its shape - links the letters
#print(reshaped_text); #joined up forms of the letters, but still going in the wrong direction
#bidi_text = get_display(reshaped_text);           # correct its direction - right to left
#print(bidi_text);
from flask import Flask, render_template, request, redirect, session, jsonify
import speech_recognition as sr
from app import db

import wave



class AudioProceesing:
    def practice(self):
        transcript = ""
        count = 0
        stars = 0

        if request.method == "POST":
            print("FORM DATA RECEIVED")

            if "file" not in request.files:
                return redirect(request.url)

            file = request.files["file"]
            if file.filename == "":
                return redirect(request.url)

            if file:
                recognizer = sr.Recognizer()
                audioFile = sr.AudioFile(file)
                with audioFile as source:
                    data = recognizer.record(source)
                transcript = recognizer.recognize_google(
                    data, language="ta-IN")

                spoken_words = []
                for i in transcript.split():
                    spoken_words.append(i)
                print(spoken_words)

                kuralId = request.form.get("getKuralId")
                kural_data = db['kural_data']
                query = {"kural_id": int(kuralId)}

                kural = kural_data.find_one(query)
                kuralWords = kural['kural'][0][0] + kural['kural'][1][0]

                for word in spoken_words:
                    if(word in kuralWords):
                        count += 1

                if(count > 0 and count <= 3):
                    stars = 1
                elif(count > 3 and count <= 6):
                    stars = 2
                elif(count == 7):
                    stars = 3
                else:
                    stars = 0

                adhigaram_number = str(int(kuralId) % 10 - 1)
                kural_number = str(int(kuralId)-1)
                total = (int(session['user']['points']['stars']['total']) + stars)
                - int(session['user']['points']['stars']['kurals_completed'][int(
                    adhigaram_number)][int(kural_number)])
                condition = {'email': session['user']['email']}

                dataToBeUpdated = {
                    "points.stars.kurals_completed."+adhigaram_number+"."+kural_number: stars, "points.stars.total": total
                }
                db.user_details.update_one(
                    condition, {"$set": dataToBeUpdated})

                session['user']['points']['stars']['total'] = total
                session['user']['points']['stars']['kurals_completed'][int(
                    adhigaram_number)][int(kural_number)] = stars
                session.modified = True

                return render_template('learn_thirukkural_1.html', stars=stars, count=count, kural=kural_data.find_one(query))

    def compareKural(self):
            transcript = ""
            count = 0
            stars = 0
            if request.method == "POST":
                f = request.files['audio_data']
                with open('audio.wav', 'wb') as audio:
                    f.save(audio)

                file = "audio.wav"
                recognizer = sr.Recognizer()
                audioFile = sr.AudioFile(file)
                print()
                with audioFile as source:
                    data = recognizer.record(source)
                transcript = recognizer.recognize_google(
                    data, language="ta-IN", show_all = True)
                if(not transcript ):
                    return  jsonify({"stars": 0, "count": 0}), 200
                spokenText = transcript['alternative'][0]['transcript']
                spoken_words = []
                for i in spokenText.split():
                    spoken_words.append(i)
                print(spoken_words)

                kuralId = request.form.get("getKuralId")


                
                kural_data = db['kural_data']
                query = {"kural_id": int(kuralId)}

                kural = kural_data.find_one(query)
                kuralWords = kural['kural'][0][0] + kural['kural'][1][0]

                for word in spoken_words:
                    if(word in kuralWords):
                        count += 1

                if(count > 0 and count <= 3):
                    stars = 1
                elif(count > 3 and count <= 6):
                    stars = 2
                elif(count == 7):
                    stars = 3
                else:
                    stars = 0
                    
                adhigaram_number = str(int(kuralId) % 10 - 1)
                kural_number = str(int(kuralId)-1)

                total = (int(session['user']['points']['stars']['total']) + stars)
                - int(session['user']['points']['stars']['kurals_completed'][int(
                    adhigaram_number)][int(kural_number)])
                condition = {'email': session['user']['email']}

                dataToBeUpdated = {
                    "points.stars.kurals_completed."+adhigaram_number+"."+kural_number: stars, "points.stars.total": total
                }
                db.user_details.update_one(
                    condition, {"$set": dataToBeUpdated})

                session['user']['points']['stars']['total'] = total
                session['user']['points']['stars']['kurals_completed'][int(
                    adhigaram_number)][int(kural_number)] = stars
                session.modified = True

                return  str(stars)+","+str(count), 200
               

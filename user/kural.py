from flask import Flask, json, jsonify, request, redirect, render_template, session
from app import db
import random


class kural:
    def fetchKural(self):
        if request.method == "POST":
            select_adhigaram = request.form.get('select_adhigaram')
            adhigaram_data = db['adhigaram_data']
            query = {"adhigaram": select_adhigaram}
            adhigaram = adhigaram_data.find(
                query, {"_id": 0, "adhigaram_id": 1})
            adhigaram_list = list(adhigaram)
            return jsonify({"adhigaram_id": adhigaram_list[0]["adhigaram_id"]}), 200

    def learn_thirukkural(self):
        if request.method == "GET":
            kuralId = request.args.get("kuralId")
            kural_data = db['kural_data']
            query = {"kural_id": int(kuralId)}
            return render_template('learn_thirukkural.html', kural=kural_data.find_one(query))

    def selected_game(self):
        if request.method == "POST":
            select_adhigaram = request.form.get('select_adhigaram')
            random_kural = request.form.get('random_kural')
            game_type = request.form.get('game_type')
            error = ''
            if((select_adhigaram == '' and random_kural == None) or game_type == None):

                if(game_type == None):
                    error = '*விளையாட்டை தேர்வுசெய்க '
                else:
                    error = '*அதிகாரம் தேர்வுசெய்க'
                return jsonify({"error": error}), 401
            
            adhigaramNumber = 0

            if(select_adhigaram != ''):
                adhigaram_data = db['adhigaram_data']
                select_adhigaram = select_adhigaram.strip()
                query = {"adhigaram": select_adhigaram}
                print(select_adhigaram)

                adhigaram = adhigaram_data.find(
                    query, {"_id": 0, "adhigaram_id": 1})
                adhigaram_list = list(adhigaram)
                print(adhigaram_list)
                #kuralStarList = session['user']['points']['stars']['kurals_completed'][int(adhigaram_list[0]["adhigaram_id"]-1)]
                adhigaramNumber = adhigaram_list[0]['adhigaram_id']
                # for star in kuralStarList:
                #     if star == 0:
                #         error = '*'+select_adhigaram + \
                #             ' அதிகாரத்திலுள்ள அணைத்து குறள்களையும் கற்ற பின் விளையாடலாம்'
                #         return jsonify({"error": error}), 401
            else:
                adhigaramNumber = random.randint(0, 132)

            adhigaram_data = db['adhigaram_data']
            query = {"adhigaram": select_adhigaram}
            adhigaram = adhigaram_data.find(
                query, {"_id": 0, "adhigaram_id": 1})
            adhigaram_list = list(adhigaram)
            print(adhigaram_list)
            adhigaramNumber = adhigaram_list[0]['adhigaram_id'] 
             #Calculate the correct Kural ID
            kural_start = (adhigaramNumber - 1) * 10 + 1
            kural_end = adhigaramNumber * 10
            kuralNumber = random.randint(kural_start, kural_end)


            query = {"kural_id": int(kuralNumber)}
            return jsonify({"kuralId": str(kuralNumber), "site": game_type}), 200

    def drag_drop_game(self):
        if request.method == "GET":
            kuralId = request.args.get("kuralId")
            kural_data = db['kural_data']
            query = {"kural_id": int(kuralId)}
            kuralData = kural_data.find_one(query)
            kuralWordsList = kuralData['kural'][0][0].split(
            ) + kuralData['kural'][1][0].split()
            random.shuffle(kuralWordsList)
            return render_template('drag_drop_game.html', kuralWord=kuralWordsList, porul=kuralData['porul'], kuralId=kuralId)

    def evaluate_drag_game(self):
        if request.method == "POST":
            userAssignedKural = []
            userAssignedKural.append(request.form.get("word1"))
            userAssignedKural.append(request.form.get("word2"))
            userAssignedKural.append(request.form.get("word3"))
            userAssignedKural.append(request.form.get("word4"))
            userAssignedKural.append(request.form.get("word5"))
            userAssignedKural.append(request.form.get("word6"))
            userAssignedKural.append(request.form.get("word7"))
            kuralId = request.form.get("kuralId")
            kural_data = db['kural_data']
            query = {"kural_id": int(kuralId)}
            kuralData = kural_data.find_one(query)
            kuralWordsList = kuralData['kural'][0][0].split(
            ) + kuralData['kural'][1][0].split()
            diamonds = 0
            correctOrder = 0
            if(userAssignedKural == kuralWordsList):
                diamonds = 3
            else:
                for i in range(0, 7):
                    if(userAssignedKural[i] == kuralWordsList[i]):
                        correctOrder += 1

                if(correctOrder > 0 and correctOrder <= 3):
                    diamonds = 1
                elif(correctOrder > 3 and correctOrder <= 6):
                    diamonds = 2
                else:
                    diamonds = 0

            if (diamonds > 0):
                adhigaram_number = str(int(kuralId) % 10)
                total = 0
                if (int(session['user']['points']['diamonds']['drag_drop'][int(adhigaram_number)]) < int(session['user']['points']['diamonds']['total']) + diamonds):
                    total = (int(session['user']['points']['diamonds']['total']) + diamonds) - int(
                        session['user']['points']['diamonds']['drag_drop'][int(adhigaram_number)])
                else:
                    total = int(session['user']['points']['diamonds']
                                ['drag_drop'][int(adhigaram_number)])
                condition = {'email': session['user']['email']}
                dataToBeUpdated = {
                    "points.diamonds.drag_drop."+adhigaram_number: diamonds, "points.diamonds.total": total}

                db.user_details.update_one(
                    condition, {"$set": dataToBeUpdated})

                session['user']['points']['diamonds']['total'] = total
                session['user']['points']['diamonds']['drag_drop'][int(
                    adhigaram_number)] = diamonds

                session.modified = True

            return render_template('drag_drop_game_1.html', kuralWord=(kuralWordsList), porul=kuralData['porul'], diamonds=diamonds)

    def fillups_game(self):
        if request.method == "GET":
            kuralId = request.args.get("kuralId")
            kural_data = db['kural_data']
            query = {"kural_id": int(kuralId)}
            kuralData = kural_data.find_one(query)
            kuralWordsList = kuralData['kural'][0][0].split(
            ) + kuralData['kural'][1][0].split()

            missingWordIndex = random.randint(0, 6)
            missingWord = kuralWordsList[missingWordIndex]
            kuralWordsList[missingWordIndex] = "__________"
            options = ["நீடுவாழ்", "யாண்டும்", "தாள்சேர்ந்தார்க்"]
            options.append(missingWord)
            random.shuffle(options)
            return render_template('fillups_game.html', kuralWord=kuralWordsList, porul=kuralData['porul'], kuralId=kuralId, options=options, index=missingWordIndex)

    def evaluate_fillups_game(self):
        if request.method == "POST":
            kuralId = request.form.get("kuralId")
            answer = request.form.get("answer")
            answerIndex = request.form.get("index")

            kural_data = db['kural_data']
            query = {"kural_id": int(kuralId)}
            kuralData = kural_data.find_one(query)
            kuralWordsList = kuralData['kural'][0][0].split(
            ) + kuralData['kural'][1][0].split()
            diamonds = 0
            if(kuralWordsList[int(answerIndex)] == answer):
                diamonds = 2
                adhigaram_number = str(int(kuralId) % 10)

                if (int(session['user']['points']['diamonds']['fillups'][int(adhigaram_number)]) < int(session['user']['points']['diamonds']['total']) + diamonds):
                    total = (int(session['user']['points']['diamonds']['total']) + diamonds) - int(
                        session['user']['points']['diamonds']['fillups'][int(adhigaram_number)])
                else:
                    total = int(session['user']['points']['diamonds']
                                ['fillups'][int(adhigaram_number)])
                condition = {'email': session['user']['email']}

                dataToBeUpdated = {
                    "points.diamonds.fillups."+adhigaram_number: diamonds, "points.diamonds.total": total}

                db.user_details.update_one(
                    condition, {"$set": dataToBeUpdated})

                session['user']['points']['diamonds']['total'] = total
                session['user']['points']['diamonds']['fillups'][int(
                    adhigaram_number)] = diamonds

                session.modified = True

            return render_template('fillups_game_1.html', diamonds=diamonds)

from flask import Flask, render_template, request, jsonify, session
import random
import csv
import os

app = Flask(__name__)
app.secret_key = "english-quiz-secret-key"

CLASS_CODES = ["10A-ENG"]

CLASS_STUDENTS = {
    "10A-ENG": [
        "Maha", "Aisha", "Sara", "Lama", "Hessa", "Noor", "Reem",
        "Joud", "Dana", "Ghada", "Amal", "Hala", "Rana", "Maryam",
        "Layan", "Noura", "Afnan", "Basma", "Raghad", "Abrar",
        "Razan", "Shahad", "Rahaf", "Jana", "Nisreen", "Alanoud",
        "Nouf", "Fatimah", "Malak", "Dalia", "Rowan", "Lujain",
        "Shaima", "Sondos", "Moneera", "Laila", "Hoor"
    ]
}

ALL_QUESTIONS = [
    {
        "unit": "Unit 1",
        "question": "My brother ___ 15 years old.",
        "options": ["am", "is", "are", "be"],
        "answer": 1,
        "explanation": "We say 'My brother is 15 years old.' (he → is).",
        "tip": "Think about verb 'be' with HE/SHE/IT (singular subject)."
    },
    {
        "unit": "Unit 1",
        "question": "They ___ from Saudi Arabia.",
        "options": ["is", "are", "am", "be"],
        "answer": 1,
        "explanation": "We use 'are' with 'they'.",
        "tip": "Is 'they' singular or plural? Choose the plural form of 'be'."
    },
    {
        "unit": "Unit 1",
        "question": "I go to school ___ bus.",
        "options": ["in", "on", "by", "at"],
        "answer": 2,
        "explanation": "We say 'by bus', 'by car', 'by train'.",
        "tip": "Think about the preposition we use with transport."
    },
    {
        "unit": "Unit 2",
        "question": "What time ___ you get up?",
        "options": ["do", "does", "are", "is"],
        "answer": 0,
        "explanation": "We say 'What time do you get up?' with 'you'.",
        "tip": "For questions with 'you', which auxiliary verb do we usually use?"
    },
    {
        "unit": "Unit 2",
        "question": "There ___ a book on the desk.",
        "options": ["is", "are", "am", "be"],
        "answer": 0,
        "explanation": "We say 'There is a book' because 'book' is singular.",
        "tip": "Check if 'book' is singular or plural."
    },
    {
        "unit": "Unit 2",
        "question": "My friends ___ football every day.",
        "options": ["play", "plays", "playing", "to play"],
        "answer": 0,
        "explanation": "With 'my friends' we use 'play'.",
        "tip": "Is 'my friends' singular or plural?"
    },
    {
        "unit": "Unit 3",
        "question": "This is my father. ___ a doctor.",
        "options": ["He is", "She is", "It is", "They are"],
        "answer": 0,
        "explanation": "We say 'He is a doctor.' for 'my father'.",
        "tip": "Which pronoun replaces 'my father'?"
    },
    {
        "unit": "Unit 3",
        "question": "We have English ___ Monday.",
        "options": ["in", "on", "at", "by"],
        "answer": 1,
        "explanation": "We use 'on' with days.",
        "tip": "Remember the preposition used with days of the week."
    }
]

TIME_LIMIT = 20
RESULTS_FILE = "quiz_results.csv"


def save_result(class_code, name, unit_filter, score, total_questions):
    percent = round(score * 100 / total_questions) if total_questions else 0

    file_exists = os.path.exists(RESULTS_FILE)

    with open(RESULTS_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "ClassCode",
                "Name",
                "UnitFilter",
                "Score",
                "TotalQuestions",
                "Percent"
            ])

        writer.writerow([
            class_code,
            name,
            unit_filter,
            score,
            total_questions,
            percent
        ])


@app.route("/")
def home():
    return render_template(
        "index.html",
        class_codes=CLASS_CODES,
        students=CLASS_STUDENTS["10A-ENG"]
    )


@app.route("/start", methods=["POST"])
def start_quiz():
    data = request.get_json()

    name = data.get("name", "").strip()
    class_code = data.get("class_code", "").strip()
    unit_filter = data.get("unit", "All units")

    if not name:
        return jsonify({
            "success": False,
            "message": "Please enter student name."
        })

    if class_code not in CLASS_CODES:
        return jsonify({
            "success": False,
            "message": "Invalid class."
        })

    if name not in CLASS_STUDENTS.get(class_code, []):
        return jsonify({
            "success": False,
            "message": "This name is not in the class list."
        })

    if unit_filter == "All units":
        questions = ALL_QUESTIONS[:]
    else:
        questions = [
            q for q in ALL_QUESTIONS
            if q["unit"] == unit_filter
        ]

    if not questions:
        return jsonify({
            "success": False,
            "message": "No questions for this unit."
        })

    random.shuffle(questions)

    session["student_name"] = name
    session["class_code"] = class_code
    session["unit_filter"] = unit_filter
    session["questions"] = questions
    session["current_index"] = 0
    session["score"] = 0
    session["attempts_left"] = 3
    session["answered"] = []

    return jsonify({
        "success": True,
        "total": len(questions)
    })


@app.route("/question")
def get_question():
    questions = session.get("questions", [])

    if not questions:
        return jsonify({
            "success": False,
            "message": "Quiz has not started."
        })

    index = session.get("current_index", 0)

    if index >= len(questions):
        return jsonify({
            "success": False,
            "finished": True
        })

    question = questions[index]

    return jsonify({
        "success": True,
        "question": question["question"],
        "options": question["options"],
        "unit": question["unit"],
        "number": index + 1,
        "total": len(questions),
        "student": session.get("student_name", ""),
        "time_limit": TIME_LIMIT
    })


@app.route("/answer", methods=["POST"])
def answer_question():
    questions = session.get("questions", [])

    if not questions:
        return jsonify({
            "success": False,
            "message": "Quiz has not started."
        })

    index = session.get("current_index", 0)

    if index >= len(questions):
        return jsonify({
            "success": False,
            "finished": True
        })

    data = request.get_json()
    selected = data.get("answer")

    question = questions[index]
    correct_answer = question["answer"]

    try:
        selected = int(selected)
    except (TypeError, ValueError):
        return jsonify({
            "success": False,
            "message": "Invalid answer."
        })

    if selected == correct_answer:
        score = session.get("score", 0) + 1
        session["score"] = score

        return jsonify({
            "success": True,
            "correct": True,
            "message": "Excellent! Keep going.",
            "explanation": question["explanation"],
            "score": score,
            "attempts_left": session.get("attempts_left", 3)
        })

    attempts_left = session.get("attempts_left", 3) - 1
    session["attempts_left"] = attempts_left

    if attempts_left <= 0:
        return jsonify({
            "success": True,
            "correct": False,
            "finished_question": True,
            "message": "No attempts left.",
            "tip": question["tip"],
            "correct_answer": question["options"][correct_answer],
            "explanation": question["explanation"],
            "score": session.get("score", 0),
            "attempts_left": 0
        })

    return jsonify({
        "success": True,
        "correct": False,
        "finished_question": False,
        "message": f"Incorrect. Attempts left: {attempts_left}",
        "tip": question["tip"],
        "attempts_left": attempts_left,
        "score": session.get("score", 0)
    })


@app.route("/next", methods=["POST"])
def next_question():
    questions = session.get("questions", [])

    if not questions:
        return jsonify({
            "success": False,
            "message": "Quiz has not started."
        })

    index = session.get("current_index", 0)

    index += 1
    session["current_index"] = index
    session["attempts_left"] = 3

    if index >= len(questions):
        score = session.get("score", 0)
        total = len(questions)

        save_result(
            session.get("class_code", ""),
            session.get("student_name", ""),
            session.get("unit_filter", ""),
            score,
            total
        )

        return jsonify({
            "success": True,
            "finished": True,
            "score": score,
            "total": total,
            "percent": round(score * 100 / total) if total else 0
        })

    return jsonify({
        "success": True,
        "finished": False,
        "number": index + 1
    })


@app.route("/results")
def results():
    if not os.path.exists(RESULTS_FILE):
        return jsonify([])

    rows = []

    with open(RESULTS_FILE, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            rows.append(row)

    return jsonify(rows)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

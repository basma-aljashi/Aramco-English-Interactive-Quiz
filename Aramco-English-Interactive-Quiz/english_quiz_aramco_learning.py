import tkinter as tk
from tkinter import ttk, messagebox
import random
import csv
import os

# ========= إعدادات عامة =========

EXCEL_FILE_LINK = "https://example.com/your_excel_results_file"  # عدّليه لو عندكم رابط حقيقي

# محاولة استخدام qrcode + Pillow لو متوفرة
try:
    import qrcode
    from PIL import Image, ImageTk
    QR_REAL = True
except Exception:
    QR_REAL = False

# شُعب متاحة (اختيار من القائمة)
CLASS_CODES = ["10A-ENG"]

# قائمة الطالبات لكل شعبة (عدّلي الأسماء للواقع)
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

# ========= أسئلة + Tips =========

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
        "tip": "Think about the preposition we use with transport (bus, car, train)."
    },
    {
        "unit": "Unit 2",
        "question": "What time ___ you get up?",
        "options": ["do", "does", "are", "is"],
        "answer": 0,
        "explanation": "We say 'What time do you get up?' with 'you'.",
        "tip": "For questions with 'you', which auxiliary verb do we usually use (without -es)?"
    },
    {
        "unit": "Unit 2",
        "question": "There ___ a book on the desk.",
        "options": ["is", "are", "am", "be"],
        "answer": 0,
        "explanation": "We say 'There is a book' (singular).",
        "tip": "Check if 'book' is singular or plural, then choose the matching form of 'there ___'."
    },
    {
        "unit": "Unit 2",
        "question": "My friends ___ football every day.",
        "options": ["play", "plays", "playing", "to play"],
        "answer": 0,
        "explanation": "With 'my friends' (they) we use 'play'.",
        "tip": "Is 'my friends' singular or plural? For plural subjects, use the base verb without -s."
    },
    {
        "unit": "Unit 3",
        "question": "This is my father. ___ a doctor.",
        "options": ["He is", "She is", "It is", "They are"],
        "answer": 0,
        "explanation": "We say 'He is a doctor.' for 'my father'.",
        "tip": "Which pronoun replaces 'my father'? Use that pronoun + verb."
    },
    {
        "unit": "Unit 3",
        "question": "We have English ___ Monday.",
        "options": ["in", "on", "at", "by"],
        "answer": 1,
        "explanation": "We use 'on' with days: on Monday, on Tuesday, ...",
        "tip": "Remember the preposition we use with days of the week (Monday, Tuesday…)."
    },
]

# ========= ألوان (أخضر + أزرق فاتح) =========

BG_COLOR = "#f0fafb"         # خلفية عامة فاتحة
CARD_COLOR = "#ffffff"       # بطاقات
ACCENT_GREEN = "#00a38a"     # أخضر
ACCENT_BLUE = "#0077b6"      # أزرق
ACCENT_DARK = "#005075"      # أزرق أغمق
TEXT_COLOR = "#00334d"
CORRECT_COLOR = "#2e7d32"
WRONG_COLOR = "#c62828"
FLASH_GOOD = "#c8e6c9"
FLASH_BAD = "#ffcdd2"
HINT_BG = "#e0f7fa"          # خلفية Hint أزرق-أخضر فاتح

TIME_LIMIT = 20
RESULTS_FILE = "quiz_results.csv"

ENCOURAGE_CORRECT = [
    "Excellent! Keep going. ✅",
    "Well done, future engineer. 🌟",
    "Brilliant choice. 💡",
    "Nice work, move to the next one. 🎯",
    "Great job, your grammar is strong. 📘",
]

ENCOURAGE_WRONG = [
    "Check the subject carefully.",
    "Look at the verb tense and form.",
    "Think about singular vs. plural.",
    "Read the whole sentence again slowly.",
    "Look at the pronoun and match the verb.",
]

BANNER_MESSAGES = [
    "Tip: Read the whole sentence before choosing.",
    "Focus on verb 'be': am / is / are.",
    "Subject–verb agreement: he/she/it vs they/we.",
    "Look at prepositions: in / on / at / by.",
]

# ========= صوت (اختياري) =========

try:
    import winsound

    def play_correct():
        winsound.Beep(900, 150)
        winsound.Beep(1100, 150)

    def play_wrong():
        winsound.Beep(400, 200)

    def play_time_over():
        winsound.Beep(300, 400)

    def start_music():
        try:
            winsound.PlaySound("background.wav",
                               winsound.SND_ASYNC | winsound.SND_LOOP)
        except Exception:
            pass

    def stop_music():
        try:
            winsound.PlaySound(None, winsound.SND_PURGE)
        except Exception:
            pass

except ImportError:
    def play_correct(): pass
    def play_wrong(): pass
    def play_time_over(): pass
    def start_music(): pass
    def stop_music(): pass

# ========= CSV =========

def ensure_results_file():
    if not os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["ClassCode", "Name", "UnitFilter", "Score",
                             "TotalQuestions", "Percent"])


def save_result(class_code, name, unit_filter, score, total_questions):
    ensure_results_file()
    percent = round(score * 100 / total_questions) if total_questions else 0
    with open(RESULTS_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([class_code, name, unit_filter, score, total_questions, percent])


def load_results():
    if not os.path.exists(RESULTS_FILE):
        return []
    rows = []
    with open(RESULTS_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                if "ClassCode" not in row:
                    row["ClassCode"] = "N/A"
                row["Score"] = int(row.get("Score", 0))
                row["TotalQuestions"] = int(row.get("TotalQuestions", 0))
                row["Percent"] = int(row.get("Percent", 0))
                rows.append(row)
            except Exception:
                continue
    rows.sort(key=lambda r: r["Percent"], reverse=True)
    return rows


# ========= التطبيق الرئيسي =========

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("English Quiz - Aramco Edition")
        self.root.geometry("1000x650")
        self.root.configure(bg=BG_COLOR)

        self.student_name = ""
        self.class_code = ""
        self.unit_filter = "All units"
        self.questions = ALL_QUESTIONS[:]
        self.current_index = 0
        self.score = 0
        self.attempts_left = 3
        self.question_finished = False
        self.timer_seconds = TIME_LIMIT
        self.timer_job = None
        self.banner_index = 0
        self.qr_img = None
        self.review_seen = False
        self.answered = []   # True إذا السؤال انتهى (للسماح بالمراجعة فقط)

        self.prev_visible = True  # للتحكم في ظهور زر Previous

        start_music()
        self.build_ui()
        self.start_banner_rotation()
        self.animate_ball()

    # ---- UI ----

    def build_ui(self):
        self.build_header()
        self.build_frames()
        self.build_start_screen()
        self.build_review_screen()
        self.build_quiz_screen()
        self.show_start()
        self.build_animation_ball()

    def build_header(self):
        header = tk.Frame(self.root, bg=ACCENT_DARK, height=70)
        header.pack(fill="x", side="top")

        left = tk.Frame(header, bg=ACCENT_DARK)
        left.pack(side="left", padx=20, pady=5)

        title = tk.Label(
            left,
            text="English Interactive Quiz – Grade 10",
            font=("Segoe UI", 18, "bold"),
            bg=ACCENT_DARK,
            fg="white"
        )
        title.pack(anchor="w")

        self.banner_label = tk.Label(
            left,
            text="",
            font=("Segoe UI", 10, "italic"),
            bg=ACCENT_DARK,
            fg="#ffecb3"
        )
        self.banner_label.pack(anchor="w")

        dash_button = tk.Button(
            header,
            text="Class Dashboard",
            font=("Segoe UI", 10, "bold"),
            bg="#ffe082",
            fg="black",
            activebackground="#ffecb3",
            bd=0,
            padx=12,
            pady=4,
            command=self.open_dashboard
        )
        dash_button.pack(side="right", padx=15, pady=15)

    def start_banner_rotation(self):
        def rotate():
            self.banner_label.config(text=BANNER_MESSAGES[self.banner_index])
            self.banner_index = (self.banner_index + 1) % len(BANNER_MESSAGES)
            self.root.after(4000, rotate)
        rotate()

    def build_frames(self):
        self.main_frame = tk.Frame(self.root, bg=BG_COLOR)
        self.main_frame.pack(fill="both", expand=True)

        self.start_frame = tk.Frame(self.main_frame, bg=BG_COLOR)
        self.review_frame = tk.Frame(self.main_frame, bg=BG_COLOR)
        self.quiz_frame = tk.Frame(self.main_frame, bg=BG_COLOR)

    def build_start_screen(self):
        card = tk.Frame(self.start_frame, bg=CARD_COLOR,
                        bd=2, relief="ridge", padx=30, pady=30)
        card.pack(expand=True)

        tk.Label(
            card,
            text="English Quiz – Term 1",
            font=("Segoe UI", 20, "bold"),
            bg=CARD_COLOR,
            fg=TEXT_COLOR
        ).pack(pady=(0, 10))

        tk.Label(
            card,
            text="Class / Session:",
            font=("Segoe UI", 11),
            bg=CARD_COLOR,
            fg=TEXT_COLOR
        ).pack(anchor="w", pady=(10, 2))

        self.class_var = tk.StringVar(value=CLASS_CODES[0])
        class_combo = ttk.Combobox(
            card,
            textvariable=self.class_var,
            values=CLASS_CODES,
            state="readonly",
            width=20
        )
        class_combo.pack(pady=(0, 8))

        tk.Label(
            card,
            text="Student Name:",
            font=("Segoe UI", 11),
            bg=CARD_COLOR,
            fg=TEXT_COLOR
        ).pack(anchor="w")

        self.name_entry = tk.Entry(card, font=("Segoe UI", 11), width=30)
        self.name_entry.pack(pady=(2, 10))

        tk.Label(
            card,
            text="Unit:",
            font=("Segoe UI", 11),
            bg=CARD_COLOR,
            fg=TEXT_COLOR
        ).pack(anchor="w", pady=(10, 2))

        units = sorted(set(q["unit"] for q in ALL_QUESTIONS))
        self.unit_options = ["All units"] + units
        self.unit_var = tk.StringVar(value="All units")

        unit_combo = ttk.Combobox(
            card,
            textvariable=self.unit_var,
            values=self.unit_options,
            state="readonly",
            width=20
        )
        unit_combo.pack(pady=(0, 15))

        info_label = tk.Label(
            card,
            text=(
                "You will first see a grammar page based on the quiz questions.\n"
                "Then you answer timed questions with hints and explanations."
            ),
            font=("Segoe UI", 9),
            bg=CARD_COLOR,
            fg=TEXT_COLOR,
            justify="left"
        )
        info_label.pack(pady=(0, 15))

        review_btn = tk.Button(
            card,
            text="Review grammar ▶",
            font=("Segoe UI", 12, "bold"),
            bg=ACCENT_GREEN,
            fg="white",
            activebackground=ACCENT_BLUE,
            bd=0,
            padx=20,
            pady=8,
            command=self.go_to_review
        )
        review_btn.pack(pady=5)

    def build_review_screen(self):
        card = tk.Frame(self.review_frame, bg=CARD_COLOR,
                        bd=2, relief="ridge", padx=30, pady=30)
        card.pack(expand=True, fill="both", padx=40, pady=40)

        header = tk.Frame(card, bg=ACCENT_BLUE)
        header.pack(fill="x", pady=(0, 15))
        tk.Label(
            header,
            text="Grammar Map for This Quiz",
            font=("Segoe UI", 18, "bold"),
            bg=ACCENT_BLUE,
            fg="white"
        ).pack(side="left", padx=10, pady=5)

        tk.Label(
            header,
            text="Focus on these rules – they appear in the questions.",
            font=("Segoe UI", 9, "italic"),
            bg=ACCENT_BLUE,
            fg="#e0f7fa"
        ).pack(side="right", padx=10)

        grid = tk.Frame(card, bg=CARD_COLOR)
        grid.pack(pady=5, fill="both", expand=True)

        def rule_box(parent, title, lines, color, icon):
            frame = tk.Frame(parent, bg=color, bd=0, padx=12, pady=10)
            top = tk.Frame(frame, bg=color)
            top.pack(fill="x")
            tk.Label(
                top, text=icon, font=("Segoe UI Emoji", 18),
                bg=color, fg=TEXT_COLOR
            ).pack(side="left", padx=(0, 6))
            tk.Label(
                top, text=title,
                font=("Segoe UI", 11, "bold"),
                bg=color, fg=TEXT_COLOR
            ).pack(side="left")
            tk.Label(
                frame, text="\n".join(lines),
                font=("Segoe UI", 10),
                bg=color, fg=TEXT_COLOR,
                justify="left"
            ).pack(anchor="w", pady=(4, 0))
            return frame

        box1 = rule_box(
            grid,
            "Verb 'be' (am / is / are)",
            [
                "I → am   (I am 15).",
                "He / She / It → is   (My brother is 15 years old.)",
                "We / You / They → are   (They are from Saudi Arabia.)",
                "My father is a doctor. → He is a doctor."
            ],
            "#e0f2f1",
            "👤"
        )
        box1.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

        box2 = rule_box(
            grid,
            "There is / There are",
            [
                "Use THERE IS + singular noun:",
                "  There is a book on the desk.",
                "Use THERE ARE + plural noun:",
                "  There are books on the desk."
            ],
            "#e3f2fd",
            "📚"
        )
        box2.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")

        box3 = rule_box(
            grid,
            "Present Simple (do / play)",
            [
                "Question with YOU → Do you ...?",
                "  What time do you get up?",
                "For HE / SHE / IT → verb + s:",
                "  She plays football.",
                "For plural subjects (my friends / they) → verb (no s):",
                "  My friends play football every day."
            ],
            "#fff3e0",
            "⏰"
        )
        box3.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

        box4 = rule_box(
            grid,
            "Prepositions & Transport",
            [
                "on + days: on Monday, on Tuesday, on Friday.",
                "at + clock time: at 7:30, at 10 o'clock.",
                "by + transport: by bus, by car, by train.",
                "Example: I go to school by bus.",
            ],
            "#f1f8e9",
            "🚌"
        )
        box4.grid(row=1, column=1, padx=10, pady=5, sticky="nsew")

        for i in range(2):
            grid.grid_columnconfigure(i, weight=1)
        for j in range(2):
            grid.grid_rowconfigure(j, weight=1)

        bottom = tk.Frame(card, bg=CARD_COLOR)
        bottom.pack(fill="x", pady=(10, 0))

        tk.Label(
            bottom,
            text="When you start the questions, you cannot go back to this page.",
            font=("Segoe UI", 9, "italic"),
            bg=CARD_COLOR,
            fg=WRONG_COLOR
        ).pack(side="left", padx=5)

        next_btn = tk.Button(
            bottom,
            text="Next ▶",
            font=("Segoe UI", 12, "bold"),
            bg=ACCENT_BLUE,
            fg="white",
            activebackground=ACCENT_GREEN,
            bd=0,
            padx=24,
            pady=6,
            command=self.start_quiz_from_review
        )
        next_btn.pack(side="right", padx=5)

    def build_quiz_screen(self):
        left = tk.Frame(self.quiz_frame, bg=BG_COLOR)
        left.pack(side="left", fill="both", expand=True, padx=(20, 10), pady=20)

        right = tk.Frame(self.quiz_frame, bg=BG_COLOR)
        right.pack(side="left", fill="both", expand=True, padx=(10, 20), pady=20)

        self.q_card = tk.Frame(left, bg=CARD_COLOR, bd=2, relief="ridge", padx=20, pady=20)
        self.q_card.pack(fill="both", expand=True)

        self.q_title_label = tk.Label(
            self.q_card,
            text="Question",
            font=("Segoe UI", 14, "bold"),
            bg=CARD_COLOR,
            fg=ACCENT_DARK
        )
        self.q_title_label.pack(anchor="w")

        timer_row = tk.Frame(self.q_card, bg=CARD_COLOR)
        timer_row.pack(fill="x", pady=(5, 5))

        self.timer_label = tk.Label(
            timer_row,
            text="",
            font=("Segoe UI", 11, "bold"),
            bg=CARD_COLOR,
            fg=WRONG_COLOR
        )
        self.timer_label.pack(side="right")

        self.timer_bar_width = 260
        self.timer_bar_canvas = tk.Canvas(
            timer_row, width=self.timer_bar_width, height=8,
            bg="#e0e0e0", highlightthickness=0
        )
        self.timer_bar_canvas.pack(side="left", padx=(0, 10), pady=2)
        self.timer_bar = self.timer_bar_canvas.create_rectangle(
            0, 0, self.timer_bar_width, 8, fill="#81c784", outline=""
        )

        self.question_label = tk.Label(
            self.q_card,
            text="",
            font=("Segoe UI", 13),
            bg=CARD_COLOR,
            fg=TEXT_COLOR,
            wraplength=380,
            justify="left"
        )
        self.question_label.pack(pady=(15, 10), anchor="w")

        self.progress_label = tk.Label(
            self.q_card,
            text="",
            font=("Segoe UI", 10),
            bg=CARD_COLOR,
            fg=TEXT_COLOR
        )
        self.progress_label.pack(anchor="e", pady=(0, 0))

        self.a_card = tk.Frame(right, bg=CARD_COLOR, bd=2, relief="ridge", padx=20, pady=20)
        self.a_card.pack(fill="both", expand=True)

        self.option_buttons = []
        for i in range(4):
            btn = tk.Button(
                self.a_card,
                text=f"Option {i+1}",
                font=("Segoe UI", 11),
                bg="white",
                fg=TEXT_COLOR,
                activebackground="#e1f5fe",
                relief="raised",
                bd=1,
                width=30,
                command=lambda idx=i: self.check_answer(idx)
            )
            btn.pack(pady=4)
            self.option_buttons.append(btn)

        self.feedback_label = tk.Label(
            self.a_card,
            text="",
            font=("Segoe UI", 11, "bold"),
            bg=CARD_COLOR,
            fg=TEXT_COLOR
        )
        self.feedback_label.pack(pady=(8, 2))

        self.hint_frame = tk.Frame(self.a_card, bg=HINT_BG, bd=1, relief="solid", padx=10, pady=6)
        self.hint_label = tk.Label(
            self.hint_frame,
            text="",
            font=("Segoe UI", 11, "bold"),
            bg=HINT_BG,
            fg=ACCENT_DARK,
            justify="left",
            wraplength=360
        )
        self.hint_label.pack(anchor="w")
        self.hint_frame.pack_forget()

        self.explanation_label = tk.Label(
            self.a_card,
            text="",
            font=("Segoe UI", 10),
            bg=CARD_COLOR,
            fg=TEXT_COLOR,
            wraplength=380,
            justify="left"
        )
        self.explanation_label.pack(pady=(6, 8))

        bottom = tk.Frame(self.a_card, bg=CARD_COLOR)
        bottom.pack(fill="x", pady=(10, 0))

        self.score_label = tk.Label(
            bottom,
            text="Score: 0 / 0",
            font=("Segoe UI", 10, "bold"),
            bg=CARD_COLOR,
            fg=TEXT_COLOR
        )
        self.score_label.pack(side="left")

        self.total_label = tk.Label(
            bottom,
            text="Total score: 0 / 0 (0%)",
            font=("Segoe UI", 10, "bold"),
            bg=CARD_COLOR,
            fg=TEXT_COLOR
        )
        self.total_label.pack(side="left", padx=15)

        nav = tk.Frame(self.a_card, bg=CARD_COLOR)
        nav.pack(fill="x", pady=(8, 0))

        self.nav_frame = nav
        self.prev_button = tk.Button(
            nav,
            text="◀ Previous",
            font=("Segoe UI", 10, "bold"),
            bg="#cfd8dc",
            fg=TEXT_COLOR,
            activebackground="#b0bec5",
            bd=0,
            width=12,
            command=self.prev_question
        )
        self.prev_button.pack(side="left")

        self.next_button = tk.Button(
            nav,
            text="Next ▶",
            font=("Segoe UI", 10, "bold"),
            bg=ACCENT_GREEN,
            fg="white",
            activebackground=ACCENT_BLUE,
            bd=0,
            width=12,
            command=self.next_question
        )
        self.next_button.pack(side="right")

    # ---- الكرة المتحركة ----

    def build_animation_ball(self):
        self.anim_frame = tk.Frame(self.root, bg=BG_COLOR)
        self.anim_frame.place(relx=1.0, rely=1.0, x=-60, y=-60, anchor="se")

        self.anim_canvas = tk.Canvas(
            self.anim_frame, width=50, height=50, bg=BG_COLOR, highlightthickness=0
        )
        self.anim_canvas.pack()
        self.ball = self.anim_canvas.create_oval(
            20, 20, 36, 36,
            fill=ACCENT_GREEN, outline=""
        )
        self.anim_dy = -2

    def animate_ball(self):
        self.anim_canvas.move(self.ball, 0, self.anim_dy)
        _, y0, _, y1 = self.anim_canvas.coords(self.ball)
        if y0 <= 5 or y1 >= 45:
            self.anim_dy *= -1
        self.root.after(50, self.animate_ball)

    # ---- التنقل بين الصفحات ----

    def show_start(self):
        self.review_frame.pack_forget()
        self.quiz_frame.pack_forget()
        self.start_frame.pack(fill="both", expand=True)

    def show_review(self):
        self.start_frame.pack_forget()
        self.quiz_frame.pack_forget()
        self.review_frame.pack(fill="both", expand=True)

    def show_quiz(self):
        self.start_frame.pack_forget()
        self.review_frame.pack_forget()
        self.quiz_frame.pack(fill="both", expand=True)

    def go_to_review(self):
        name = self.name_entry.get().strip()
        class_code = self.class_var.get().strip()
        if not name:
            messagebox.showwarning("Name required", "Please enter student name.")
            return
        if class_code in CLASS_STUDENTS and name not in CLASS_STUDENTS[class_code]:
            msg = (
                "This name is not in the class list.\n"
                "If the student is not registered, you can add her name later in CLASS_STUDENTS."
            )
            messagebox.showwarning("Name not in list", msg)
        self.student_name = name
        self.class_code = class_code
        self.unit_filter = self.unit_var.get()
        self.show_review()

    def start_quiz_from_review(self):
        if self.unit_filter == "All units":
            self.questions = ALL_QUESTIONS[:]
        else:
            self.questions = [q for q in ALL_QUESTIONS if q["unit"] == self.unit_filter]

        if not self.questions:
            messagebox.showerror("No questions", "No questions for this unit.")
            self.show_start()
            return

        random.shuffle(self.questions)
        self.current_index = 0
        self.score = 0
        self.answered = [False] * len(self.questions)

        self.score_label.config(text=f"Score: {self.score} / {len(self.questions)}")
        self.update_total_score()

        self.review_seen = True
        self.show_quiz()
        self.load_question()

    # ---- منطق الكويز ----

    def update_total_score(self):
        total = len(self.questions) if self.questions else 0
        percent = round(self.score * 100 / total) if total else 0
        self.total_label.config(
            text=f"Total score: {self.score} / {total} ({percent}%)"
        )

    def reset_timer(self):
        if self.timer_job is not None:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None

    def clear_timer_display(self):
        self.timer_label.config(text="")
        self.timer_bar_canvas.coords(self.timer_bar, 0, 0, 0, 8)

    def update_timer_bar(self):
        frac = max(0, min(1, self.timer_seconds / TIME_LIMIT))
        x1 = int(self.timer_bar_width * frac)
        self.timer_bar_canvas.coords(self.timer_bar, 0, 0, x1, 8)
        if frac > 0.5:
            color = "#81c784"
        elif frac > 0.25:
            color = "#ffb74d"
        else:
            color = "#e57373"
        self.timer_bar_canvas.itemconfig(self.timer_bar, fill=color)

    def start_timer(self):
        self.reset_timer()
        self.timer_seconds = TIME_LIMIT
        self.timer_label.config(text=f"Time: {self.timer_seconds}s")
        self.update_timer_bar()

        def tick():
            if self.question_finished:
                return
            self.timer_seconds -= 1
            if self.timer_seconds <= 0:
                self.timer_label.config(text="Time: 0s")
                self.update_timer_bar()
                play_time_over()
                self.feedback_label.config(
                    text="Time is over.",
                    fg=WRONG_COLOR
                )
                self.question_finished = True
                self.answered[self.current_index] = True
                self.finish_question(show_explanation=True)
                self.next_button.config(state="normal")
                self.root.after(1200, self.next_question)
                return
            self.timer_label.config(text=f"Time: {self.timer_seconds}s")
            self.update_timer_bar()
            self.timer_job = self.root.after(1000, tick)

        self.timer_job = self.root.after(1000, tick)

    def flash_cards(self, color):
        original_q = self.q_card.cget("bg")
        original_a = self.a_card.cget("bg")

        self.q_card.config(bg=color)
        self.a_card.config(bg=color)
        self.root.after(
            150,
            lambda: (self.q_card.config(bg=original_q),
                     self.a_card.config(bg=original_a))
        )

    def update_nav_buttons(self):
        if self.current_index == 0:
            if self.prev_visible:
                self.prev_button.pack_forget()
                self.prev_visible = False
        else:
            if not self.prev_visible:
                self.prev_button.pack(side="left")
                self.prev_visible = True

    def load_question(self):
        self.reset_timer()
        self.clear_timer_display()
        self.question_finished = False
        self.feedback_label.config(text="", fg=TEXT_COLOR)
        self.hint_label.config(text="")
        self.hint_frame.pack_forget()
        self.explanation_label.config(text="")

        self.update_nav_buttons()

        q = self.questions[self.current_index]
        self.q_title_label.config(
            text=f"{self.student_name} – {self.class_code} – {q['unit']} – Question {self.current_index + 1}/{len(self.questions)}"
        )
        self.question_label.config(text=q["question"])

        for i, opt in enumerate(q["options"]):
            self.option_buttons[i].config(
                text=f"{chr(65+i)}. {opt}",
                bg="white",
                state="normal"
            )

        progress = "●" * (self.current_index + 1) + "○" * (len(self.questions) - self.current_index - 1)
        self.progress_label.config(text=progress)

        if self.answered and self.answered[self.current_index]:
            self.next_button.config(state="normal")
            correct_text = q["options"][q["answer"]]
            self.feedback_label.config(text="Finished question (review only).", fg=TEXT_COLOR)
            self.explanation_label.config(
                text=f"Correct answer: {correct_text}\n{q['explanation']}"
            )
            for btn in self.option_buttons:
                btn.config(state="disabled")
        else:
            self.next_button.config(state="disabled")
            self.attempts_left = 3
            self.start_timer()

    def finish_question(self, show_explanation):
        self.reset_timer()
        self.clear_timer_display()
        q = self.questions[self.current_index]
        if show_explanation:
            correct_text = q["options"][q["answer"]]
            self.explanation_label.config(
                text=f"Correct answer: {correct_text}\n{q['explanation']}"
            )
        for btn in self.option_buttons:
            btn.config(state="disabled")
        self.next_button.config(state="normal")

    def check_answer(self, idx):
        if self.question_finished:
            return

        q = self.questions[self.current_index]
        btn = self.option_buttons[idx]

        original_btn_bg = btn.cget("bg")

        def restore_btn_color():
            btn.config(bg=original_btn_bg)

        btn.config(state="disabled", bg="#eeeeee")

        if idx == q["answer"]:
            # وميض أخضر في الكارد + زر الإجابة
            self.flash_cards(FLASH_GOOD)
            btn.config(bg="#c8e6c9")
            self.root.after(180, restore_btn_color)

            play_correct()
            self.score += 1
            self.score_label.config(
                text=f"Score: {self.score} / {len(self.questions)}"
            )
            self.update_total_score()

            msg = random.choice(ENCOURAGE_CORRECT)
            self.feedback_label.config(text=msg, fg=CORRECT_COLOR)

            self.hint_frame.pack_forget()

            self.question_finished = True
            self.answered[self.current_index] = True
            self.finish_question(show_explanation=False)
            self.root.after(700, self.next_question)
        else:
            # وميض أحمر في الكارد + زر الإجابة
            self.flash_cards(FLASH_BAD)
            btn.config(bg="#ffcdd2")
            self.root.after(180, restore_btn_color)

            play_wrong()
            self.attempts_left -= 1

            tip_text = q.get("tip", "Check the grammar rule for this question.")
            extra = random.choice(ENCOURAGE_WRONG)
            self.feedback_label.config(
                text=f"Incorrect. Attempts left: {self.attempts_left}",
                fg=WRONG_COLOR
            )
            self.hint_label.config(text=f"TIP 💡: {tip_text}\n{extra}")
            self.hint_frame.pack(fill="x", pady=(4, 4))

            if self.attempts_left <= 0:
                self.question_finished = True
                self.answered[self.current_index] = True
                self.finish_question(show_explanation=True)
                self.root.after(1200, self.next_question)

    def next_question(self):
        if self.current_index + 1 >= len(self.questions):
            self.end_quiz()
        else:
            self.current_index += 1
            self.load_question()

    def prev_question(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.load_question()

    def end_quiz(self):
        total = len(self.questions)
        percent = round(self.score * 100 / total) if total else 0
        save_result(self.class_code, self.student_name, self.unit_filter,
                    self.score, total)
        messagebox.showinfo(
            "Quiz Finished",
            f"{self.student_name}, you finished the quiz.\n\n"
            f"Final score: {self.score} / {total} ({percent}%)"
        )
        self.show_start()

    # ---- Dashboard ----

    def open_dashboard(self):
        results = load_results()

        win = tk.Toplevel(self.root)
        win.title("Class Dashboard")
        win.geometry("900x560")
        win.configure(bg=BG_COLOR)

        tk.Label(
            win,
            text="Class Dashboard – English Quiz",
            font=("Segoe UI", 16, "bold"),
            bg=BG_COLOR,
            fg=TEXT_COLOR
        ).pack(pady=10)

        top_frame = tk.Frame(win, bg=BG_COLOR)
        top_frame.pack(fill="x", padx=10)

        tk.Label(
            top_frame,
            text="Class:",
            font=("Segoe UI", 10),
            bg=BG_COLOR,
            fg=TEXT_COLOR
        ).pack(side="left", padx=(0, 4))

        dash_class_var = tk.StringVar(value=CLASS_CODES[0])
        dash_class_combo = ttk.Combobox(
            top_frame,
            textvariable=dash_class_var,
            values=CLASS_CODES,
            state="readonly",
            width=12
        )
        dash_class_combo.pack(side="left")

        qr_canvas = tk.Canvas(
            top_frame, width=130, height=130, bg="white", highlightthickness=1,
            highlightbackground=ACCENT_DARK
        )
        qr_canvas.pack(side="right", padx=10, pady=5)
        self.draw_qr_or_fake(qr_canvas)

        tk.Label(
            top_frame,
            text="Scan QR to open shared results file\n(if EXCEL_FILE_LINK is set).",
            font=("Segoe UI", 9),
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            justify="right"
        ).pack(side="right", padx=5)

        cols = ("Class", "Name", "Unit", "Score", "Total", "Percent")
        tree = ttk.Treeview(
            win, columns=cols, show="headings", height=10
        )
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, anchor="center", width=110)
        tree.pack(fill="x", padx=10, pady=(10, 5))

        bottom_frame = tk.Frame(win, bg=BG_COLOR)
        bottom_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        absent_frame = tk.Frame(bottom_frame, bg=CARD_COLOR, bd=2, relief="ridge")
        absent_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
        tk.Label(
            absent_frame,
            text="Absent students",
            font=("Segoe UI", 11, "bold"),
            bg=CARD_COLOR,
            fg=WRONG_COLOR
        ).pack(anchor="w", padx=8, pady=4)

        absent_listbox = tk.Listbox(
            absent_frame,
            font=("Segoe UI", 10),
            bg=CARD_COLOR,
            fg=TEXT_COLOR,
            borderwidth=0,
            highlightthickness=0
        )
        absent_listbox.pack(fill="both", expand=True, padx=8, pady=4)

        chart_frame = tk.Frame(bottom_frame, bg=BG_COLOR)
        chart_frame.pack(side="left", fill="both", expand=True, padx=(5, 0))

        chart_canvas = tk.Canvas(
            chart_frame, bg="white", height=170, highlightthickness=1,
            highlightbackground=ACCENT_DARK
        )
        chart_canvas.pack(fill="both", expand=True)

        def refresh_dashboard(*_):
            class_code = dash_class_var.get()
            for item in tree.get_children():
                tree.delete(item)
            filtered = [r for r in results if r.get("ClassCode", "") == class_code]
            for row in filtered:
                tree.insert("", "end", values=(
                    row.get("ClassCode", ""),
                    row.get("Name", ""),
                    row.get("UnitFilter", ""),
                    row.get("Score", 0),
                    row.get("TotalQuestions", 0),
                    f"{row.get('Percent', 0)}%"
                ))

            absent_listbox.delete(0, tk.END)
            all_students = CLASS_STUDENTS.get(class_code, [])
            present_names = {r.get("Name", "") for r in filtered}
            for name in all_students:
                if name not in present_names:
                    absent_listbox.insert(tk.END, name)

            self.draw_top_chart(chart_canvas, filtered)

        dash_class_var.trace_add("write", refresh_dashboard)
        refresh_dashboard()

    def draw_qr_or_fake(self, canvas):
        canvas.delete("all")
        if QR_REAL and EXCEL_FILE_LINK:
            try:
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_M,
                    box_size=3,
                    border=2,
                )
                qr.add_data(EXCEL_FILE_LINK)
                qr.make(fit=True)
                img = qr.make_image(fill_color="black", back_color="white")
                self.qr_img = ImageTk.PhotoImage(img)
                canvas.create_image(65, 65, image=self.qr_img)
                return
            except Exception:
                pass

        size = 11
        cell = 8
        margin = 10
        random.seed(42)
        for r in range(size):
            for c in range(size):
                if random.random() < 0.35:
                    x0 = margin + c * cell
                    y0 = margin + r * cell
                    x1 = x0 + cell
                    y1 = y0 + cell
                    canvas.create_rectangle(
                        x0, y0, x1, y1,
                        fill=ACCENT_DARK, outline=ACCENT_DARK
                    )

    def draw_top_chart(self, canvas, results):
        canvas.delete("all")
        if not results:
            canvas.create_text(
                10, 10, anchor="nw",
                text="No results yet for this class.",
                font=("Segoe UI", 10),
                fill=TEXT_COLOR
            )
            return

        top = sorted(results, key=lambda r: r.get("Percent", 0), reverse=True)[:5]
        max_percent = max(r.get("Percent", 0) for r in top) or 1

        width = int(canvas.winfo_width() or canvas.winfo_reqwidth())
        height = int(canvas.winfo_height() or canvas.winfo_reqheight())
        margin = 40
        bar_width = (width - 2 * margin) / len(top)

        for i, row in enumerate(top):
            x0 = margin + i * bar_width + 10
            x1 = margin + (i + 1) * bar_width - 10
            bar_max_h = height - 2 * margin
            bar_h = bar_max_h * row.get("Percent", 0) / max_percent
            y1 = height - margin
            y0 = y1 - bar_h

            canvas.create_rectangle(
                x0, y0, x1, y1,
                fill=ACCENT_GREEN, outline=ACCENT_BLUE
            )
            canvas.create_text(
                (x0 + x1) / 2, y0 - 10,
                text=f"{row.get('Percent', 0)}%",
                font=("Segoe UI", 9),
                fill=TEXT_COLOR
            )
            canvas.create_text(
                (x0 + x1) / 2, height - margin + 12,
                text=row.get("Name", ""),
                font=("Segoe UI", 8),
                fill=TEXT_COLOR
            )


# ========= تشغيل =========

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
    stop_music()

# English Interactive Quiz – Advantage Academy

## Live Demo

[Open the English Interactive Quiz](https://aramco-english-interactive-quiz.onrender.com/)

## Overview

I developed this interactive English quiz as a learning tool for Advantage Academy, supported by Saudi Aramco. The idea was to give students a simple way to practice English, strengthen their understanding of the course material, and measure their level through interactive questions.

The quiz was designed to make learning more engaging by allowing students to answer questions, receive feedback, use tips when needed, and learn from their mistakes while completing the quiz.

## Purpose

The main purpose of the quiz is to support students in improving their English skills and provide a simple way to measure their understanding of the topics covered in the course.

The quiz focuses on:

- Practicing English grammar and vocabulary
- Measuring students' understanding through questions
- Providing immediate feedback
- Helping students learn from their mistakes
- Making the learning process more interactive
- Recording and reviewing quiz results

## Feedback from Supervisors

The idea was discussed with the supervisors, and their feedback was taken into consideration during the development of the quiz. The concept received positive feedback from the supervisors.

## Student Experience

The student starts by selecting the class, entering their name, and choosing the unit they want to practice.

Before starting the quiz, students can review important grammar topics. The quiz then presents questions based on the selected unit.

During the quiz, the student can:

1. Read the question and choose an answer.
2. Use a tip when they need help.
3. Submit the answer and receive feedback.
4. Review the explanation when an answer is incorrect.
5. Try again and continue learning from the mistake.
6. Move to the next question using the navigation button.
7. Answer the questions within the available time using the built-in timer.
8. View the final result after completing the quiz.

This structure connects practice with assessment and gives students an opportunity to understand their mistakes instead of only receiving a final score.

## Main Features

- Interactive English questions for Grade 10 students
- Questions covering Units 1–3
- Grammar review before starting the quiz
- Built-in timer
- Tips for questions that need additional support
- Immediate feedback after answering
- Explanations for incorrect answers
- Opportunity to try again
- Next-question navigation
- Student name and class selection
- Score calculation
- Quiz result recording
- Class results and performance tracking
- Simple and student-friendly interface

## Topics Covered

The quiz includes English topics such as:

- Verb "Be"
- There is / There are
- Present Simple
- Prepositions
- Transportation
- Basic English grammar and vocabulary

## Technologies Used

- Python
- Flask
- Tkinter
- HTML5
- CSS3
- JavaScript
- CSV

Python was used for the main application logic, while Flask, HTML, CSS, and JavaScript were used for the web-based version of the quiz. CSV was used to store quiz results.

## Application Structure

```text
Aramco-English-Interactive-Quiz/
│
├── app.py
├── requirements.txt
│
├── templates/
│   └── index.html
│
└── english_quiz_aramco_learning.py
```

## Application Components

### app.py

Contains the Flask application and the main web-based quiz logic. It handles the quiz flow, student information, questions, answers, scoring, session data, and quiz results.

### templates/index.html

Contains the web interface that students use to start the quiz, answer questions, receive feedback, and move between questions.

### english_quiz_aramco_learning.py

Contains the original Python interactive quiz application developed using Tkinter. It includes the quiz questions, grammar review, timer, feedback, scoring, and class results.

### requirements.txt

Contains the Python packages required to run the web version of the application.

## Learning and Assessment

The quiz was designed to connect assessment with learning. Instead of only showing whether an answer is right or wrong, the system provides tips and explanations to help students understand their mistakes and continue practicing.

The recorded results also provide a way to review student performance and identify areas where additional practice may be needed.

## Project Context

This project was developed as part of the digital learning activities connected to Advantage Academy and Saudi Aramco. It combines programming with an educational purpose by turning English practice into an interactive digital experience.

Working on this project allowed me to connect programming with a real learning need, from designing the quiz flow and question interaction to handling answers, timing, feedback, scoring, and results.

## Future Improvements

Possible future improvements include adding more English units and questions, expanding the question bank, adding more detailed performance reports, and connecting the system to a database for long-term student progress tracking.

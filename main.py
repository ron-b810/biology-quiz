import streamlit as st
import json
import random


# פונקציה לטעינת השאלות מקובץ ה-JSON
def load_questions():
    try:
        with open('questions.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        st.error("קובץ השאלות (questions.json) לא נמצא!")
        return []


# אתחול ה-State (זיכרון של האפליקציה)
if 'questions' not in st.session_state:
    st.session_state.questions = load_questions()
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'total_answered' not in st.session_state:
    st.session_state.total_answered = 0
if 'current_q' not in st.session_state and st.session_state.questions:
    st.session_state.current_q = random.choice(st.session_state.questions)

# --- ממשק המשתמש ---
st.set_page_config(page_title="Biology Exam", layout="centered")

st.markdown("<h1 style='text-align: center; color: #4CAF50;'>מבחן תיאוריה בביולוגיה 🧬</h1>", unsafe_allow_html=True)

# הצגת סטטיסטיקה בצד
st.sidebar.title("סטטיסטיקה")
st.sidebar.write(f"תשובות נכונות: {st.session_state.score}")
st.sidebar.write(f"סה\"כ שאלות: {st.session_state.total_answered}")

if st.session_state.questions:
    q = st.session_state.current_q

    st.markdown(f"### שאלה {q['id']}")
    st.info(q['question'])

    # אם יש תמונה לשאלה (אופציונלי - דורש שתשמור תמונות בתיקייה)
    if q.get('has_image'):
        st.warning("⚠️ שים לב: שאלה זו מתייחסת לתמונה מהמבחן המקורי")

    # טופס התשובות
    with st.form(key='quiz_form'):
        # ערבוב סדר התשובות כדי שיהיה מעניין
        options = q['options']

        selected_option = st.radio("בחר את התשובה הנכונה:", options, index=None)

        submit_btn = st.form_submit_button("בדוק תשובה 🚀")

        if submit_btn:
            if selected_option:
                if selected_option == q['correct_answer']:
                    st.success(f"נכון מאוד! התשובה היא: {selected_option}")
                    st.balloons()
                    st.session_state.score += 1
                else:
                    st.error(f"טעות! התשובה הנכונה היא: {q['correct_answer']}")

                st.session_state.total_answered += 1

                # כפתור מעבר לשאלה הבאה (מופיע רק אחרי שעונים)
                if st.form_submit_button("לשאלה הבאה ➡️"):
                    st.session_state.current_q = random.choice(st.session_state.questions)
                    st.rerun()
            else:
                st.warning("לא בחרת תשובה!")

    # כפתור ידני להחלפת שאלה
    if st.button("דלג לשאלה אחרת"):
        st.session_state.current_q = random.choice(st.session_state.questions)
        st.rerun()

else:
    st.write("אין שאלות בקובץ... תמלא את ה-JSON יא עצלן 😉")
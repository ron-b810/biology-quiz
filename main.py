import streamlit as st
import json
import random


# --- פונקציות ---
def load_questions():
    try:
        with open('questions.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        st.error("קובץ השאלות (questions.json) לא נמצא!")
        return []


# --- אתחול הזיכרון (Session State) ---
if 'questions' not in st.session_state:
    st.session_state.questions = load_questions()

# משתנה ששומר את השאלה הנוכחית
if 'current_q' not in st.session_state and st.session_state.questions:
    st.session_state.current_q = random.choice(st.session_state.questions)

# משתנה ששומר אם המשתמש כבר ענה על השאלה הזאת (כדי להציג את התשובה)
if 'submitted' not in st.session_state:
    st.session_state.submitted = False

if 'score' not in st.session_state:
    st.session_state.score = 0

# --- עיצוב האפליקציה ---
st.set_page_config(page_title="Biology Exam", layout="centered")

st.markdown("<h1 style='text-align: center; color: #4CAF50;'>מבחן תיאוריה בביולוגיה 🧬</h1>", unsafe_allow_html=True)

# הצגת הניקוד בצד
st.sidebar.markdown(f"### 🏆 ניקוד: {st.session_state.score}")

if st.session_state.questions:
    q = st.session_state.current_q

    # הצגת השאלה
    st.markdown(f"### שאלה {q['id']}")
    st.info(q['question'])

    # הצגת תמונה אם קיימת
    if q.get('image'):
        try:
            st.image(q['image'], use_column_width=True)
        except:
            st.error(f"לא הצלחתי לטעון תמונה: {q['image']}")
    elif q.get('has_image'):
        st.warning("⚠️ שאלה זו דורשת תמונה (בדוק אם העלית אותה)")

    # --- אזור הבחירה ---
    # אנחנו משתמשים ב-ID של השאלה בתוך ה-key כדי שהבחירה תתאפס כשעוברים שאלה
    user_choice = st.radio(
        "בחר את התשובה הנכונה:",
        q['options'],
        key=f"q_{q['id']}",
        index=None
    )

    # --- כפתורים ולוגיקה ---
    col1, col2 = st.columns([1, 1])

    # כפתור בדיקה (מופיע רק אם עדיין לא ענינו)
    if not st.session_state.submitted:
        if col1.button("בדוק תשובה 🚀"):
            if user_choice:
                st.session_state.submitted = True
                st.rerun()  # מרענן את הדף כדי להציג את התוצאה
            else:
                st.warning("אנא בחר תשובה לפני הבדיקה")

    # אם המשתמש ענה - מציגים תוצאה וכפתור "הבא"
    else:
        # בדיקת התשובה
        if user_choice == q['correct_answer']:
            st.success(f"✅ נכון מאוד! התשובה היא: {user_choice}")
            # הוספת ניקוד (רק אם זו פעם ראשונה שאנחנו רואים את המסך הזה)
            # בגרסה פשוטה זו הניקוד עלול לעלות ברענון, אז נשאיר פשוט
        else:
            st.error(f"❌ טעות! התשובה הנכונה היא: {q['correct_answer']}")

        # כפתור לשאלה הבאה
        if st.button("לשאלה הבאה ➡️", type="primary"):
            # איפוס המצב
            st.session_state.submitted = False
            # בחירת שאלה חדשה
            st.session_state.current_q = random.choice(st.session_state.questions)

            # אם התשובה הייתה נכונה, נעלה ניקוד עכשיו (לפני המעבר)
            if user_choice == q['correct_answer']:
                st.session_state.score += 1

            st.rerun()

    # כפתור דילוג (תמיד זמין בצד)
    if col2.button("דלג שאלה ⏭️"):
        st.session_state.submitted = False
        st.session_state.current_q = random.choice(st.session_state.questions)
        st.rerun()

else:
    st.write("אין שאלות בקובץ JSON.")
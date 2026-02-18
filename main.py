import streamlit as st
import json
import random


# --- פונקציות ---
def load_questions():
    try:
        with open('questions.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []


# --- אתחול הזיכרון (Session State) ---
if 'all_data' not in st.session_state:
    st.session_state.all_data = load_questions()
if 'quiz_started' not in st.session_state:
    st.session_state.quiz_started = False
if 'quiz_complete' not in st.session_state:
    st.session_state.quiz_complete = False

# --- עיצוב ---
st.set_page_config(page_title="מבחן ביולוגיה", layout="centered")
st.markdown("<h1 style='text-align: center;'>🧬 הכנה למבחן בביולוגיה</h1>", unsafe_allow_html=True)

# --- שלב 0: מסך פתיחה ---
if not st.session_state.quiz_started and not st.session_state.quiz_complete:
    st.subheader("הגדרות המבחן")
    actual_max = len(st.session_state.all_data)
    # הוספתי 3 לרשימת האופציות לבקשתך
    options_list = [3, 33, 66, 99, 132, 165, actual_max]
    valid_options = sorted(list(set([opt for opt in options_list if opt <= actual_max])))

    num_q = st.selectbox("כמה שאלות תרצה במבחן?", valid_options)

    if st.button("התחל מבחן 🚀"):
        st.session_state.selected_questions = random.sample(st.session_state.all_data, num_q)
        st.session_state.total_questions_limit = num_q  # המכסה המקסימלית
        st.session_state.current_display_idx = 1  # המונה שרץ על המסך (1 עד X)
        st.session_state.correct_count = 0
        st.session_state.submitted = False
        st.session_state.quiz_started = True
        st.rerun()

# --- שלב 1: מהלך המבחן ---
elif st.session_state.quiz_started:
    questions = st.session_state.selected_questions
    q = questions[0]  # תמיד לוקחים את השאלה הראשונה ברשימה הדינמית

    total_limit = st.session_state.total_questions_limit
    current_num = st.session_state.current_display_idx

    st.write(f"**שאלה {current_num} מתוך {total_limit}**")
    st.progress(min(current_num / total_limit, 1.0))

    st.info(q.get('question', 'שאלה חסרה'))

    if q.get('image'):
        st.image(q['image'], use_container_width=True)

    user_choice = st.radio("בחר תשובה:", q.get('options', []), key=f"q_{current_num}", index=None)

    col1, col2 = st.columns(2)


    # פונקציה לסיום שאלה/דילוג ובדיקה אם הגענו לסוף המכסה
    def move_to_next_or_finish():
        if st.session_state.current_display_idx >= total_limit:
            st.session_state.quiz_started = False
            st.session_state.quiz_complete = True
        else:
            st.session_state.current_display_idx += 1
            st.session_state.submitted = False
        st.rerun()


    if not st.session_state.submitted:
        if col1.button("בדוק תשובה ✅"):
            if user_choice:
                st.session_state.submitted = True
                if user_choice == q.get('correct_answer'):
                    st.session_state.correct_count += 1
                st.rerun()
            else:
                st.warning("בחר תשובה קודם")

        if col2.button("דלג על השאלה ⏭️"):
            # מוציאים את השאלה הנוכחית מהרשימה (כדי שלא תחזור במבחן הקצר)
            st.session_state.selected_questions.pop(0)
            move_to_next_or_finish()

    else:
        if user_choice == q.get('correct_answer'):
            st.success(f"נכון מאוד! {user_choice}")
            st.balloons()
        else:
            st.error(f"טעות. התשובה הנכונה: {q.get('correct_answer')}")

        if st.button("המשך ➡️", type="primary"):
            st.session_state.selected_questions.pop(0)
            move_to_next_or_finish()

# --- שלב 2: סיום ---
elif st.session_state.quiz_complete:
    st.balloons()
    score = st.session_state.correct_count
    total = st.session_state.total_questions_limit
    percent = int((score / total) * 100)

    st.markdown(f"<h2 style='text-align: center;'>הציון שלך: {percent}%</h2>", unsafe_allow_html=True)
    st.write(f"ענית נכון על {score} מתוך {total} שאלות שהוצגו.")

    if st.button("נסה מבחן חדש 🔄"):
        st.session_state.quiz_complete = False
        st.rerun()
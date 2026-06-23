import streamlit as st
from datetime import datetime, timedelta

# --- Page Configuration ---
st.set_page_config(page_title="Global Trichology", page_icon="🔬", layout="wide")

# --- Custom CSS for Theme (Navy Blue, Light Blue, White) ---
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #FFFFFF;
    }
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #000080 !important; /* Navy Blue */
    }
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #ADD8E6; /* Light Blue */
    }
    [data-testid="stSidebar"] * {
        color: #000080 !important;
    }
    /* Buttons */
    .stButton>button {
        background-color: #000080;
        color: #FFFFFF !important;
        border: none;
        border-radius: 5px;
        padding: 10px 24px;
    }
    .stButton>button:hover {
        background-color: #ADD8E6;
        color: #000080 !important;
        border: 1px solid #000080;
    }
    /* Info/Alert boxes */
    .stAlert {
        background-color: #ADD8E6;
        color: #000080;
    }
    </style>
""", unsafe_allow_html=True)

# --- Session State Initialization ---
if 'completed_lessons' not in st.session_state:
    st.session_state.completed_lessons = 0
if 'active_lesson' not in st.session_state:
    st.session_state.active_lesson = 1
if 'lesson_start_time' not in st.session_state:
    st.session_state.lesson_start_time = datetime.now()

# --- Mock Lesson Data ---
lesson_plan = {
    1: {"title": "Anatomy of Hair and Scalp", "topic": "Hair Follicle Structure"},
    2: {"title": "Hair Growth Cycles", "topic": "Anagen, Catagen, Telogen Phases"},
    3: {"title": "Common Scalp Conditions", "topic": "Dandruff, Psoriasis, Seborrheic Dermatitis"},
    4: {"title": "Types of Hair Loss (Alopecia)", "topic": "Androgenetic Alopecia & Alopecia Areata"},
    5: {"title": "Nutrition and Hair Health", "topic": "Vitamins, Minerals, and Diet"},
    6: {"title": "Chemical Damage & Repair", "topic": "pH Levels and Structural Integrity"},
    7: {"title": "Consultation and Analysis", "topic": "Microscopic Scalp Evaluations"},
    8: {"title": "Holistic Trichology Treatments", "topic": "Essential Oils and Scalp Massage"},
    9: {"title": "Clinical Treatments and Modalities", "topic": "Low-Level Laser Therapy (LLLT)"},
    10: {"title": "Business of Trichology", "topic": "Ethics, State Laws, and Client Management"}
}

# --- Timer Logic ---
# Set to 3600 seconds (1 hour) for production. 
# Change to 10 seconds right now if you want to test the app quickly.
REQUIRED_SECONDS = 3600  

def check_timer():
    elapsed = datetime.now() - st.session_state.lesson_start_time
    return elapsed.total_seconds() >= REQUIRED_SECONDS

def advance_lesson():
    st.session_state.completed_lessons += 1
    st.session_state.active_lesson += 1
    st.session_state.lesson_start_time = datetime.now() # Reset timer for the next lesson

# --- Sidebar Navigation ---
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Blank_square.svg/120px-Blank_square.svg.png", width=50) # Placeholder for your logo
st.sidebar.title("Global Trichology")
st.sidebar.markdown("---")
st.sidebar.subheader("Course Progress")
progress_bar = st.sidebar.progress(st.session_state.completed_lessons / 10)
st.sidebar.write(f"**Lessons Completed:** {st.session_state.completed_lessons} / 10")

st.sidebar.markdown("---")
if st.sidebar.button("Reset Progress (Dev Tool)"):
    st.session_state.clear()
    st.rerun()

# --- Main Interface ---
st.title("Global Trichology Certification")

if st.session_state.active_lesson <= 10:
    current = lesson_plan[st.session_state.active_lesson]
    
    st.header(f"Lesson {st.session_state.active_lesson}: {current['title']}")
    
    # State compliance timer display
    elapsed_time = datetime.now() - st.session_state.lesson_start_time
    remaining_time = max(0, REQUIRED_SECONDS - int(elapsed_time.total_seconds()))
    
    if remaining_time > 0:
        minutes, seconds = divmod(remaining_time, 60)
        st.warning(f"⏳ **State Requirement Timer:** You must study this material for {minutes}m {seconds}s more before taking the quiz.")
    else:
        st.success("✅ **Timer Complete:** You may now submit the quiz to advance.")

    # Tabs for Study Guide and Quiz
    tab1, tab2 = st.tabs(["📖 Study Guide", "📝 Lesson Quiz"])

    with tab1:
        st.subheader(f"Topic: {current['topic']}")
        st.write("""
        *Welcome to this lesson.* Please review the following study materials thoroughly. State board requirements mandate that you spend a minimum of 60 minutes reviewing this module. Ensure you understand the cellular functions and clinical manifestations outlined below.
        
        **Study Materials:**
        - Reading Chapter: [Insert text here]
        - Video Lecture: [Insert embedded video link here]
        - Vocabulary Review: [Insert terms here]
        """)
        
    with tab2:
        st.subheader("Knowledge Check")
        st.write("Complete the quiz below to verify your understanding. You cannot submit until the state-mandated 1-hour timer has elapsed.")
        
        q1 = st.radio("1. What is the primary focus of this lesson?", ["Scalp Health", "Skin Care", "Nail Growth", "Bone Density"], index=None)
        q2 = st.radio("2. True or False: You must complete 10 lessons for certification.", ["True", "False"], index=None)
        
        # Validation and Submission
        if st.button("Submit Quiz & Advance"):
            if not check_timer():
                st.error("Wait! You have not met the 1-hour minimum study time required by state regulations.")
            elif q1 is None or q2 is None:
                st.error("Please answer all questions before submitting.")
            else:
                st.balloons()
                advance_lesson()
                st.rerun()

elif st.session_state.active_lesson == 11:
    st.header("🎓 Final Certification Exam")
    st.success("Congratulations! You have completed the 10-hour state requirement. The final exam is now unlocked.")
    st.write("This exam consists of 100 comprehensive questions covering Anatomy, Hair Loss, and Clinical Treatments.")
    
    st.info("The exam will open in a secure browser window. You must score an 80% or higher to receive your Global Trichology Certificate.")
    if st.button("Begin Final Exam"):
        st.write("*(Exam portal opens here...)*")

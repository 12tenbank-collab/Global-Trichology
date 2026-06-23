import streamlit as st
from datetime import datetime, timedelta
import time

# --- Page Configuration ---
st.set_page_config(page_title="Global Trichology", page_icon="🔬", layout="wide")

# --- CUSTOM THEME (Navy, Light Blue, White) ---
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; }
    [data-testid="stSidebar"] { background-color: #000080; }
    [data-testid="stSidebar"] * { color: #FFFFFF !important; }
    h1, h2, h3 { color: #000080 !important; font-family: 'Helvetica Neue', sans-serif; }
    .stButton>button {
        background-color: #000080;
        color: #FFFFFF !important;
        border-radius: 20px;
        border: 2px solid #ADD8E6;
    }
    .main-box {
        background-color: #f0f4f8;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #ADD8E6;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Home"
if 'completed_lessons' not in st.session_state:
    st.session_state.completed_lessons = 0
if 'lesson_start_time' not in st.session_state:
    st.session_state.lesson_start_time = None

# --- CONSTANTS ---
LOGO_URL = "http://googleusercontent.com/image_collection/image_retrieval/598258075546678371"
TEST_PREP_IMG = "http://googleusercontent.com/image_collection/image_retrieval/1218677147972910425"
CONTINUED_ED_IMG = "http://googleusercontent.com/image_collection/image_retrieval/12797348955438761267"
CAREER_ADV_IMG = "http://googleusercontent.com/image_collection/image_retrieval/4169267514374572343"
REQUIRED_SECONDS = 3600 # 1 Hour

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.image(LOGO_URL, width=150)
    st.title("Navigation")
    selection = st.radio("Go to:", ["Home", "Lesson Plan", "Test Prep", "FAQ", "Support"])
    st.session_state.current_page = selection
    
    st.markdown("---")
    st.write(f"**Progress:** {st.session_state.completed_lessons}/10 Lessons")
    st.progress(st.session_state.completed_lessons / 10)

# --- PAGE: HOME ---
if st.session_state.current_page == "Home":
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(LOGO_URL, use_column_width=True)
    with col2:
        st.title("Welcome to Global Trichology")
        st.subheader("Professional Medical & Educational Certification")
        st.write("""
            Global Trichology is a premier paid platform dedicated to the science of hair and scalp health. 
            Our comprehensive 10-lesson course is designed to meet strict state requirements, 
            providing a blend of medical knowledge and clinical practice to prepare you for global licensure.
        """)

    st.markdown("---")
    
    # Career Sections
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.image(TEST_PREP_IMG, caption="Success Starts Here")
        st.subheader("Test Prep")
        st.write("Master the curriculum with our focused exam strategies. We provide mock board exams, flashcards for anatomy, and case study reviews to ensure you are fully prepared for certification.")
        
    with c2:
        st.image(CONTINUED_ED_IMG, caption="Keep Growing")
        st.subheader("Continued Education")
        st.write("Stay at the forefront of the industry. Our continued education modules offer advanced insights into microscopic scalp analysis, regenerative therapies, and the latest in laser technology.")
        
    with c3:
        st.image(CAREER_ADV_IMG, caption="Build Your Practice")
        st.subheader("Career Advancement")
        st.write("Transform your knowledge into a thriving business. Learn clinic management, ethical marketing, and professional documentation to lead your own multidisciplinary hair health team.")

# --- PAGE: LESSON PLAN ---
elif st.session_state.current_page == "Lesson Plan":
    st.title("Your Lesson Plan")
    
    lesson_num = st.session_state.completed_lessons + 1
    
    if lesson_num <= 10:
        st.header(f"Current Module: Lesson {lesson_num}")
        
        # Timer Logic
        if st.session_state.lesson_start_time is None:
            if st.button("Start 1-Hour Study Session"):
                st.session_state.lesson_start_time = datetime.now()
                st.rerun()
        else:
            elapsed = datetime.now() - st.session_state.lesson_start_time
            remaining = max(0, REQUIRED_SECONDS - int(elapsed.total_seconds()))
            
            if remaining > 0:
                mins, secs = divmod(remaining, 60)
                st.warning(f"⏳ State Requirement: {mins}m {secs}s remaining before you can take the quiz.")
                time.sleep(1) # Simple refresh trigger
                st.rerun()
            else:
                st.success("✅ Requirement met! You may now complete the Study Guide and Quiz.")
                
                with st.expander("📖 View Study Guide"):
                    st.write("Detailed medical content for Lesson", lesson_num)
                
                if st.button("Take Quiz & Advance"):
                    st.session_state.completed_lessons += 1
                    st.session_state.lesson_start_time = None
                    st.balloons()
                    st.rerun()
    else:
        st.success("🎓 All lessons complete! Final Exam Unlocked in 'Test Prep' tab.")

# --- PAGE: TEST PREP ---
elif st.session_state.current_page == "Test Prep":
    st.title("Test Prep & Final Exam")
    st.image(TEST_PREP_IMG, width=400)
    
    if st.session_state.completed_lessons < 10:
        st.info("The Final Test will be available here after all 10 lessons are completed.")
        st.subheader("Practice Resources")
        st.write("- Anatomy Flashcards\n- Scalp Condition Image Database\n- Nutrition Quick-Guides")
    else:
        st.header("🏆 Final Certification Exam")
        st.write("You have met the 10-hour state requirement. You may now begin your final evaluation.")
        if st.button("Launch Final Exam"):
            st.write("Final Exam Portal Initializing...")

# --- PAGE: FAQ ---
elif st.session_state.current_page == "FAQ":
    st.title("Frequently Asked Questions")
    with st.expander("Why is there a 1-hour timer?"):
        st.write("To meet state board licensing requirements, students must document 1 hour of active study per lesson.")
    with st.expander("Can I take longer than an hour?"):
        st.write("Yes! You can take as long as you need to master the material, but you cannot advance sooner than 60 minutes.")

# --- PAGE: SUPPORT ---
elif st.session_state.current_page == "Support":
    st.title("Student Support")
    st.write("Need help with the platform or course material? Contact our clinical instructors.")
    st.text_input("Subject")
    st.text_area("Message")
    if st.button("Send Request"):
        st.success("Support ticket created. We will respond within 24 hours.")

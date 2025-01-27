import streamlit as st

st.set_page_config(
    page_title='ChatDC',
    page_icon=':robot_face:'
)

st.title("🌟 Welcome to ChatDC 🌟")

st.markdown("""
## Discover Daly College (DC) 🏫
Explore various topics about Daly College and find answers to your questions. Below is a guide to what you can ask ChatDC about:
""")

# Accurate topics extracted from the database
topics = {
    "🏛 Overview and History": [
        "🕰 Founding of Daly College",
        "📍 The school's location and setup as a day-cum-boarding school",
        "📜 Legacy of Sir Henry Daly and the Indo-Saracenic architectural style"
    ],
    "📋 School Administration": [
        "👩‍🏫 Current and past principals",
        "👨‍🏫 Vice Principals and administrative structure",
        "🛡 Members of the Board of Governors and their roles"
    ],
    "📚 Educational Boards": [
        "🎓 Offerings of CBSE and Cambridge International (CI) boards",
        "📄 Details about board-related exams and transitions"
    ],
    "🏠 Houses and Residences": [
        "👦 Boys' and Girls' boarding houses",
        "📊 House Reports"
        "👶 Residences for students of different age groups"
    ],
    "🎒 Levels of Schooling": [
        "🧒 Pre-Primary, Junior, and Senior school divisions"
    ],
    "🏅 Sports": [
        "⚽ Facilities for cricket, basketball, football, swimming, and shooting",
        "🏆 Sports achievements and key tournaments"
    ],
    "🎭 Cultural and Co-curricular Activities": [
        "🎼 Activities like music, dance, fine arts, photography, dramatics, and woodcraft",
        "🥇 Highlights of cultural achievements and events"
    ],
    "🤝 Community Service": [
        "🌱 Daly Ethos Club initiatives, including drives and eco-friendly projects"
    ],
    "🗓 School Calendar": [
        "📅 Key school events during December, January, February, and March"
    ],
    "📈 Academic Performance": [
        "📝 Results and academic achievements in CI and CBSE boards"
    ],
    "👩‍🎓 Student Leadership": [
        "🎖 Student captains and prefects",
        "🛡 Roles and responsibilities of student leaders"
    ],
    "🧑‍🏫 Faculty and Departments": [
        "📖 Departmental faculty and their specializations",
        "📜 Senior appointments and their contributions"
    ]
}

# Display topics in an expandable and visually engaging format
for topic, details in topics.items():
    with st.expander(topic):
        st.markdown(f"### {topic}")
        for detail in details:
            st.markdown(f"- {detail}")

# Add a footer to encourage interaction
st.markdown("""
---
✨ **Ask any specific question related to the above topics, and ChatDC will provide detailed answers tailored to your queries!** ✨
""")

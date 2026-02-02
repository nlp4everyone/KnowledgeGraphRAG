import streamlit as st

# Define pages
pages = {
    "Homepage": [
        st.Page("pages/home/home_page.py", title="Home Page", icon="🏠"),
    ],
    "Chunk Analysis": [
        st.Page("pages/chunking/chunking_analysis.py", title="Chunk Analysis", icon="📄"),
    ],
}

pg = st.navigation(pages)
pg.run()

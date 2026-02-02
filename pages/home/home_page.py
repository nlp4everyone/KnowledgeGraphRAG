import streamlit as st

st.set_page_config(
    page_title="Homepage",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Graphiti Demo")
st.markdown("---")

st.markdown("""
## Welcome to the KnowledgeGraphRAG Demo

This application demonstrates text parsing and chunk analysis capabilities.

### Available Pages:
- **📊 Chunk Analysis**: Analyze and visualize chunk data with interactive dashboards

Navigate between pages using the sidebar on the left.
""")
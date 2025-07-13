import streamlit as st
from qa_pipeline import FinancialQASystem

@st.cache_resource
def load_system():
    return FinancialQASystem()

qa = load_system()
st.set_page_config(page_title="CSV QA Agent", layout="wide")
st.title("📊 Enhanced CSV Question Answering")
q = st.text_input("Ask about your data:", placeholder="e.g. Compare profit Q2 vs Q3")
if st.button("Submit") and q:
    with st.spinner("Analyzing..."):
        st.success(f"📊 Answer: {qa.answer_query(q)}")

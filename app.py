import streamlit as st
from llm.llm import generate_response

# Page title
st.set_page_config(page_title="AI Research Assistant")

# Heading
st.title("🤖 AI Research Assistant")

st.write("Ask any question to the AI.")

# Input box
user_query = st.text_input("Enter your question:")

# Button
if st.button("Ask"):

    if user_query.strip():

        with st.spinner("Generating response..."):

            answer = generate_response(user_query)

        st.success("Response Generated!")

        st.write(answer)

    else:
        st.warning("Please enter a question.")
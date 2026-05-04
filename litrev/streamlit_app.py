import asyncio
import streamlit as st
from litrev_backend import run_litrev

st.set_page_config(page_title="Literature Review Assistant", page_icon="📚")
st.title("📚 Literature Review Assistant")
st.write("Enter a research topic and I'll find and summarize real papers from arXiv!")

query = st.text_input("Research topic", placeholder="e.g. graph neural networks for chemistry")
n_papers = st.slider("Number of papers", 1, 10, 5)

if st.button("🔍 Search") and query:
    async def _runner():
        chat_placeholder = st.container()
        async for frame in run_litrev(query, num_papers=n_papers):
            role, *rest = frame.split(":", 1)
            content = rest[0].strip() if rest else ""
            with chat_placeholder:
                if role == "search_agent":
                    with st.chat_message("assistant", avatar="🔍"):
                        st.markdown(f"**Search Agent:**\n{content}")
                elif role == "summarizer":
                    with st.chat_message("assistant", avatar="📝"):
                        st.markdown(f"**Summarizer:**\n{content}")

    with st.spinner("Searching arXiv and writing review..."):
        try:
            asyncio.run(_runner())
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(_runner())

    st.success("Literature review complete! 🎉")
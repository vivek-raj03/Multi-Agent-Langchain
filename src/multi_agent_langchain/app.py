
from pathlib import Path
import sys
import streamlit as st
from dotenv import load_dotenv

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Load environment variables
load_dotenv(PROJECT_ROOT / ".env")

from src.multi_agent_langchain.pipeline.pipeline import run_research_pipeline


# Page configuration
st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🔎",
    layout="wide"
)

st.title("🔎 AI Research Assistant")
st.write("Generate research reports using a multi-agent LangChain system.")

# User input
topic = st.text_input(
    "Enter your research topic",
    placeholder="e.g. Kubernetes autoscaling"
)

# Generate report
if st.button("Generate Research Report", type="primary"):

    if not topic.strip():
        st.warning("Please enter a research topic.")

    else:
        try:
            with st.spinner("Your AI agents are researching..."):
                result = run_research_pipeline(topic.strip())

            st.success("Research completed successfully!")

            # Final report
            st.subheader("📄 Research Report")
            st.markdown(result["report"])

            # Critic feedback
            st.subheader("🧐 Critic Review")
            st.markdown(result["feedback"])

            # Optional: expandable research details
            with st.expander("View Search Results"):
                st.write(result["search_results"])

            with st.expander("View Scraped Content"):
                st.write(result["scraped_content"])

        except Exception as e:
            st.error(f"Research failed: {str(e)}")

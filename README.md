# Multi-Agent Research Assistant

## What It Does
Given a research topic, this application automates end-to-end research by coordinating multiple AI agents to gather information from the web, extract in-depth source material, write a structured report, and review the final output for quality.

---

## How It Works
The pipeline (`run_research_pipeline`) passes a shared `state` dictionary through four sequential stages:

1. **Search (`build_search_agent`)**
   - Takes the user's `topic` and queries web search tools to gather recent, relevant sources and URLs.
   - Stores the findings in `state["search_results"]`.

2. **Read & Scrape (`build_reader_agent`)**
   - Inspects the top search results, selects the most relevant URL, and scrapes its full content for deeper context.
   - Stores the extracted text in `state["scraped_content"]`.

3. **Write (`writer_chain`)**
   - Combines both `state["search_results"]` and `state["scraped_content"]` as research context.
   - Synthesizes the information into a structured report saved in `state["report"]`.

4. **Critique (`critic_chain`)**
   - Evaluates the generated report for completeness, clarity, and accuracy.
   - Outputs constructive review notes saved in `state["feedback"]`.

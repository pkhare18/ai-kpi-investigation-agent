# 🚀 KPI Investigation Agent (Claude-powered)

A lightweight **data investigation agent** that analyzes KPI drops using
**multi-step reasoning, tool execution, and Claude**.

------------------------------------------------------------------------

## 🧠 Problem Statement

Most dashboards only show *what happened* (e.g., KPI dropped), but
not: - Why did it happen? - Where did it happen? - What should we do
next?

This project solves that by building an **agent** that: - Detects KPI
changes\
- Investigates them step-by-step\
- Uses data tools (Python functions)\
- Generates root cause analysis and recommendations

------------------------------------------------------------------------

## ⚙️ What Makes This an "Agent"?

This is **not just a chatbot or dashboard**.

It qualifies as an agent because it:

-   ✅ Performs **multi-step reasoning**
-   ✅ **Decides next actions dynamically**
-   ✅ Uses **tools (Python functions) to query data**
-   ✅ Iterates before producing a final answer

------------------------------------------------------------------------

## 🏗️ Architecture

User / KPI Trigger ↓ Claude (Planner) ↓ Decision: What to analyze next?
↓ Python Tool Execution (Pandas) ↓ Result appended to context ↓ Claude
decides next step ↓ (loop continues) ↓ Final Root Cause +
Recommendations

------------------------------------------------------------------------

## 🧩 Tech Stack

-   Python
-   Pandas
-   Streamlit
-   Claude API (Anthropic)
-   CSV dataset

------------------------------------------------------------------------

## 📊 Features

-   KPI dashboard
-   Claude-powered analysis
-   Multi-step investigation loop
-   Tool-based reasoning
-   Root cause + actionable insights

------------------------------------------------------------------------

## 📁 Project Structure

kpi-investigation-agent-claude/ │ ├── app.py ├── agent.py ├──
data_processor.py ├── CLAUDE.md ├── sample_data/ └── README.md

------------------------------------------------------------------------

## ▶️ How to Run

pip install -r requirements.txt streamlit run app.py
streamlit run app.py
https://redesigned-train-6pj4xr4xj5vc44wx-8501.app.github.dev/

------------------------------------------------------------------------

## 🎯 Pitch

"I built a KPI investigation agent that uses Claude to iteratively
analyze metric drops by invoking Python-based tools."

------------------------------------------------------------------------


# 🧠 CSV Question Answering — Advanced Version

Advanced version of my CSV QA agent — now supports fine-tuning on SQuAD-style data, comparison/growth questions, yes/no trends, and a modular architecture.

It supports natural language queries like:
- "What was profit in Q3?"
- "Compare revenue between Q1 and Q3"
- "Did tax increase from Q2 to Q4?"
- "What is the percentage growth in income from Q1 to Q2?"

It works on **financial reports, business dashboards, or any quarterly tabular data** — transforming raw spreadsheets into an interactive, intelligent agent.

---

## 🚀 Features

- 🤖 Fine-tuned BERT on CSV-derived QA pairs
- 📊 Custom SQuAD-style dataset generation from CSVs
- 💬 Natural language interface (Streamlit + CLI)
- 🔁 Handles:
  - Quarter-to-quarter comparisons
  - Growth and percentage change queries
  - Yes/No financial trend detection
- 🧠 Fuzzy topic recognition for flexible queries
- 🔧 Modular codebase for extension or retraining

---

## 📁 Directory Structure

advanced_version/
├── app.py                 # Streamlit frontend
├── main.py                # CLI interface
├── qa_pipeline.py         # Core QA system
├── dataset_builder.py     # SQuAD-style training data generator
├── train_model.py         # BERT fine-tuning script
├── test.py                # Quick test runner
├── config.py              # Topic and quarter mappings
├── loader.py              # CSV loader / cleaner
├── Trent.csv              # Sample financial dataset

---

## 💬 Example Questions

- "What is the tax amount in Mar-24?"
- "Compare profit in Jun-24 and Sep-24"
- "Did expenses increase from Q1 to Q4?"
- "How much did income change between Q2 and Q3?"

---

## ⚙️ Getting Started

### 1. Install requirements
pip install -r requirements.txt

### 2. Fine-tune the model (optional)
python dataset_builder.py     # Generates squad.json
python train_model.py         # Fine-tunes BERT on your CSV

### 3. Run Streamlit app
streamlit run app.py

Or run in CLI:
python main.py

---

## 📌 Use Cases

- Financial report summarization
- Business intelligence dashboards
- Conversational interfaces over Excel-like data
- Executive Q&A bots

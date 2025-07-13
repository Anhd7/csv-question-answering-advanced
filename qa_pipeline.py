import re
from fuzzywuzzy import process
from transformers import pipeline, AutoTokenizer, AutoModelForQuestionAnswering
from config import TOPIC_ALIASES, QUARTER_MAPPING, MODEL_CONFIG
from loader import load_csv

class FinancialQASystem:
    def __init__(self, model_path=None, csv_path=None):
        self.model_path = model_path or MODEL_CONFIG["model_path"]
        self.csv_path = csv_path or MODEL_CONFIG["csv_path"]
        self.df = load_csv(self.csv_path)
        self.qa_pipeline = self._load_model()

    def _load_model(self):
        tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        model = AutoModelForQuestionAnswering.from_pretrained(self.model_path)
        return pipeline("question-answering", model=model, tokenizer=tokenizer)

    def parse_question(self, question):
        question = question.lower()
        quarter = next((mapped for term, mapped in QUARTER_MAPPING.items() if term in question), None)
        topic = next((canonical for alias, canonical in TOPIC_ALIASES.items() if alias in question), None)
        if not topic:
            best_match, score = process.extractOne(question, self.df["topics"].tolist())
            topic = best_match if score > 60 else None
        return topic, quarter

    def get_value(self, topic, quarter):
        row = self.df[self.df["topics"] == topic]
        if not row.empty:
            value = str(row[quarter].values[0]).replace(",", "").strip()
            return value if value.lower() != "nan" else None
        return None

    def handle_complex_query(self, question):
        question_lower = question.lower()
        topic, _ = self.parse_question(question_lower)
        if not topic:
            return None

        if "did" in question_lower or "was" in question_lower:
            return self._process_yesno(question_lower, topic)
        elif "growth" in question_lower or "change" in question_lower:
            return self._process_growth(question_lower, topic)
        elif "compare" in question_lower or "vs" in question_lower:
            return self._process_comparison(question_lower, topic)
        return None

    def _extract_quarters(self, question):
        matches = re.findall(r"(q[1-4]|quarter [1-4]|last quarter|current quarter|past year|year over year)", question)
        return [QUARTER_MAPPING.get(m) for m in matches if m in QUARTER_MAPPING]

    def _process_yesno(self, question, topic):
        qtrs = self._extract_quarters(question)
        if len(qtrs) >= 2:
            val1, val2 = self.get_value(topic, qtrs[0]), self.get_value(topic, qtrs[1])
            if val1 and val2:
                val1, val2 = float(val1), float(val2)
                increase = val2 > val1
                direction = "increased" if increase else "decreased"
                change = (val2 - val1) / val1 * 100
                answer = "yes" if (
                    ("increase" in question and increase) or 
                    ("decrease" in question and not increase)
                ) else "no"
                return f"{topic} {direction} from {val1} to {val2} ({abs(change):.2f}%). Answer: {answer}"
        return None

    def _process_growth(self, question, topic):
        qtrs = self._extract_quarters(question)
        if "past year" in question or "year over year" in question:
            qtrs = ["sep-23", "sep-24"]
        if len(qtrs) >= 2:
            val1, val2 = self.get_value(topic, qtrs[0]), self.get_value(topic, qtrs[1])
            if val1 and val2:
                val1, val2 = float(val1), float(val2)
                change = (val2 - val1) / val1 * 100
                direction = "increased" if change > 0 else "decreased"
                return f"{topic} {direction} by {abs(change):.2f}% from {qtrs[0]} to {qtrs[1]}"
        return None

    def _process_comparison(self, question, topic):
        qtrs = self._extract_quarters(question)
        if len(qtrs) >= 2:
            val1, val2 = self.get_value(topic, qtrs[0]), self.get_value(topic, qtrs[1])
            if val1 and val2:
                val1, val2 = float(val1), float(val2)
                change = (val2 - val1) / val1 * 100
                return f"{topic} changed from {val1} ({qtrs[0]}) to {val2} ({qtrs[1]}). {'Increase' if change >= 0 else 'Decrease'} of {abs(change):.2f}%"
        return None

    def answer_query(self, question):
        try:
            complex_answer = self.handle_complex_query(question)
            if complex_answer:
                return complex_answer
            topic, quarter = self.parse_question(question)
            if not topic or not quarter:
                return "Please ask about a specific metric and quarter (e.g. 'What was revenue in Q3?')"
            value = self.get_value(topic, quarter)
            if not value:
                return f"Could not find {topic} data for {quarter}"
            return f"The {topic} for {quarter} is {value}."
        except Exception as e:
            return f"Error processing your question: {str(e)}"

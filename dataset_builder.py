import pandas as pd
import json
import random
from datetime import datetime

# Configuration
QUARTERS = ["Sep-24", "Jun-24", "Mar-24", "Dec-23"]
QUARTER_ALIASES = {
    "q1": "Mar-24", "q2": "Jun-24", "q3": "Sep-24", "q4": "Dec-23",
    "first quarter": "Mar-24", "second quarter": "Jun-24",
    "last quarter": "Dec-23", "current quarter": "Sep-24"
}

def load_csv(file_path="Trent.csv"):
    """Load and preprocess the CSV file"""
    df = pd.read_csv(file_path)
    df.columns = [col.strip() for col in df.columns]
    df["Topics"] = df["Topics"].str.strip()
    return df

def clean_number(value):
    """Remove commas and convert to float"""
    try:
        return float(str(value).replace(",", "").strip())
    except:
        return None

def generate_comparison_examples(topic, q1, q2, val1, val2):
    """Generate comparison QA pairs for training"""
    examples = []
    
    # Basic comparison context
    change = ((val2 - val1) / val1) * 100
    direction = "increased" if val2 > val1 else "decreased"
    context = f"The {topic} {direction} from {val1} in {q1} to {val2} in {q2} ({abs(change):.2f}%)."
    
    # Yes/No questions
    examples.append({
        "context": context,
        "qas": [{
            "question": f"Did {topic} increase from {q1} to {q2}?",
            "id": f"comp_yesno_{hash(f'{topic}{q1}{q2}')}",
            "answers": [{
                "text": "yes" if val2 > val1 else "no",
                "answer_start": context.find("yes" if val2 > val1 else "no")
            }]
        }]
    })
    
    # Percentage change questions
    examples.append({
        "context": context,
        "qas": [{
            "question": f"What was the percentage change in {topic} from {q1} to {q2}?",
            "id": f"comp_pct_{hash(f'{topic}{q1}{q2}')}",
            "answers": [{
                "text": f"{abs(change):.2f}%",
                "answer_start": context.find(f"{abs(change):.2f}%")
            }]
        }]
    })
    
    return examples

def generate_squad_data(df):
    """Generate SQuAD format dataset"""
    data = []
    
    for _, row in df.iterrows():
        topic = str(row["Topics"]).lower()
        
        # 1. Basic fact questions (original)
        for q in QUARTERS:
            raw_value = row[q]
            value = clean_number(raw_value)
            if value is None:
                continue
                
            # Standard QA pair
            data.append({
                "context": f"The {topic} for {q} is {value}.",
                "qas": [{
                    "question": f"What is the {topic} for {q}?",
                    "id": f"basic_{hash(f'{topic}{q}')}",
                    "answers": [{
                        "text": str(value),
                        "answer_start": len(f"The {topic} for {q} is ")
                    }]
                }]
            })
        
        # 2. Comparison questions (new)
        valid_quarters = [q for q in QUARTERS if clean_number(row[q]) is not None]
        if len(valid_quarters) >= 2:
            # Generate all possible quarter pairs
            for i in range(len(valid_quarters)):
                for j in range(i+1, len(valid_quarters)):
                    q1, q2 = valid_quarters[i], valid_quarters[j]
                    val1, val2 = clean_number(row[q1]), clean_number(row[q2])
                    data.extend(generate_comparison_examples(topic, q1, q2, val1, val2))
    
    # Shuffle to mix basic and comparison examples
    random.shuffle(data)
    
    return {
        "version": "2.0",
        "data": [{
            "title": "Financial_QAs",
            "paragraphs": data
        }]
    }

def export_squad(squad_data, out_file="squad.json"):
    """Save dataset to JSON file"""
    with open(out_file, "w") as f:
        json.dump(squad_data, f, indent=2)
    print(f"✅ Generated {len(squad_data['data'][0]['paragraphs'])} QA pairs")

if __name__ == "__main__":
    print("Building enhanced training dataset...")
    df = load_csv()
    squad_data = generate_squad_data(df)
    export_squad(squad_data)
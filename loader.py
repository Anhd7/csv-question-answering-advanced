import pandas as pd

def load_csv(file_path):
    df = pd.read_csv(file_path)
    df.columns = [col.strip().lower() for col in df.columns]
    if "topics" in df.columns:
        df["topics"] = df["topics"].str.strip().str.lower()
    return df

def chunk_csv_as_text(df, chunk_size=800):
    text = df.to_string(index=False)
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

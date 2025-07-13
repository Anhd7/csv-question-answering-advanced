# config.py

TOPIC_ALIASES = {
    "revenue": "net sales/income from operations",
    "profit": "net profit/(loss) for the period",
    "expenses": "other expenses",
    "tax": "tax",
    "income": "total income from operations",
    "sales": "net sales/income from operations"
}

QUARTER_MAPPING = {
    "q1": "mar-24", "1st quarter": "mar-24", "jan-mar": "mar-24",
    "q2": "jun-24", "2nd quarter": "jun-24", "apr-jun": "jun-24",
    "q3": "sep-24", "3rd quarter": "sep-24", "jul-sep": "sep-24",
    "q4": "dec-23", "4th quarter": "dec-23", "oct-dec": "dec-23",
    "current": "sep-24", "previous": "jun-24", "last": "dec-23",
    "past year": "year_comparison", "year over year": "year_comparison",
    "september 2024": "sep-24", "march 2024": "mar-24", "december 2023": "dec-23"
}

MODEL_CONFIG = {
    "model_path": "qa_finetuned",
    "csv_path": "Trent.csv"
}

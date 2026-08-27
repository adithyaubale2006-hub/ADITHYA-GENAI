# app/pipeline.py

# 1. Import your functions from the model files
from models.sentiment import sentiment_analysis
from models.classifier import classify_text
from models.summarization import summarize

def process_text(text):
    """
    Takes a single text input, runs it through all 3 models, 
    and returns a combined dictionary of results.
    """
    print("Running models... (this might take a moment)")
    
    # 2. Run Sentiment Analysis
    sentiment_data = sentiment_analysis(text)
    
    # 3. Run Summarization
    summary_data = summarize(text)
    
    # 4. Run Classification
    classification_data = classify_text(text)
    
    # 5. Combine everything into the final JSON/dictionary structure
    return {
        "sentiment": sentiment_data["sentiment"],
        "summary": summary_data, 
        "classification": classification_data["predicted_category"],
        "confidence": classification_data["confidence"]
    }

# --- Test the combined pipeline ---
#if __name__ == "__main__":
    test_text = """
    Apple just released a brand new MacBook Pro with an M3 chip. 
    The performance is absolutely incredible for video editing and gaming. 
    I am highly impressed with the battery life, though the price is a bit high.
    """
    
    final_result = process_text(test_text)
    
    # Print nicely formatted
    import json
    print(json.dumps(final_result, indent=4))
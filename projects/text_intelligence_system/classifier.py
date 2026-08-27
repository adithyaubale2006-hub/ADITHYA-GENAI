from transformers import pipeline

# Load the model OUTSIDE the function so it only loads once when the app starts
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def classify_text(text):
    # Define your categories
    categories = [
    "Technology",
    "Education",
    "Business",
    "Finance",
    "Health",
    "Sports",
    "Entertainment",
    "Politics",
    "Science",
    "Travel",
    "Food",
    "Product Review",
    "Customer Support",
    "Job & Career",
    "News",
    "Other"
]
    
    # Get the results from the model
    result = classifier(text, candidate_labels=categories)
    
    # Return the top category and its confidence score
    return {
        "predicted_category": result["labels"][0],
        "confidence": f"{result['scores'][0] * 100:.2f}%"
    }

# --- Test it locally ---
#if __name__ == "__main__":#
    print(classify_text("I just bought a new laptop for gaming."))

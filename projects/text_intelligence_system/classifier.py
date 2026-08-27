from transformers import pipeline

# Load the model once
classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli"
)

# Classification categories
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

def classify_text(text):

    # Get classification results
    result = classifier(
        text,
        candidate_labels=categories
    )

    predicted_category = result["labels"][0]
    confidence = result["scores"][0]

    # Confidence threshold
    threshold = 0.50

    if confidence < threshold:
        predicted_category = "Other"

    return {
        "predicted_category": predicted_category,
        "confidence": f"{confidence * 100:.2f}%"
    }


# Test locally
#if __name__ == "__main__":
    print(classify_text(
        "I just bought a new laptop for gaming."
    ))

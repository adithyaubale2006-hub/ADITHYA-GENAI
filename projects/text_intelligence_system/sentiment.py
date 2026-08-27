#Install Libraries
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch

#Load Model and Tokenizer
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")

def sentiment_analysis(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    
    with torch.no_grad(): # Good practice to add this so it doesn't compute gradients during inference
        outputs = model(**inputs)
        
    logits = outputs.logits

    # Probabilities
    probabilities = torch.softmax(logits, dim=1)
    confidence = torch.max(probabilities).item()

    # Predictions
    predictions = torch.argmax(logits, dim=1)
    sentiment = "positive" if predictions.item() == 1 else "negative"
    
    return {
        "sentiment": sentiment,
        "confidence": f"{confidence*100:.2f}" # Added quotes and the missing comma above
    }

#test 
print(sentiment_analysis("He is a great person and always helps others."))
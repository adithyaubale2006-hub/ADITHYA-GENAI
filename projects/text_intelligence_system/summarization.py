from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

def summarize(text):
    tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")
    model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-large-cnn")

    inputs = tokenizer(text, return_tensors="pt", max_length=1024,  truncation=True, padding=True)

    summary_ids = model.generate(inputs["input_ids"], max_length=150, min_length=30, length_penalty=2.0, num_beams=4, early_stopping=True)

    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    return summary


#test
#print(summarize("The quick brown fox jumps over the lazy dog. This is a test sentence to check the summarization"))

    


from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

class Model:
    def __init__(self, model_name):
        self.model_name = model_name
        self.tokenizer = self.load_tokenizer()  # Corrected method call
        self.model = self.load_model()  # Corrected method call

    def load_model(self):
        model = AutoModelForSequenceClassification.from_pretrained(
            self.model_name)
        return model

    def load_tokenizer(self):
        tokenizer = AutoTokenizer.from_pretrained(self.model_name,use_fast=False)
        return tokenizer

    def get_pipeline(self):
        # Use the Hugging Face pipeline with the initialized model and tokenizer
        if self.model and self.tokenizer:
            self.model.eval()
            # Replace with appropriate Hugging Face pipeline
            classifier = pipeline('zero-shot-classification',
                                  model=self.model, tokenizer=self.tokenizer)
            return classifier
        else:
            raise ValueError("Model and tokenizer not initialized.")


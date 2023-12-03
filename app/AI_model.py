from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline


class AIModel:
    def __init__(self, model_name):
        self.model_name = model_name
        self.tokenizer = self.load_tokenizer() 
        self.model = self.load_model() 

    # load's the model
    def load_model(self):
        model = AutoModelForSequenceClassification.from_pretrained(
            self.model_name)
        return model
    # load's the tokenizer
    def load_tokenizer(self):
        tokenizer = AutoTokenizer.from_pretrained(
            self.model_name, use_fast=False)
        return tokenizer

    # returns a pipeline based on the model and tokenizer
    def get_pipeline(self, text: str):
        # Use the Hugging Face pipeline with the initialized model and tokenizer
        if self.model and self.tokenizer:
            self.model.eval()
            classifier = pipeline(text,
                                  model=self.model, tokenizer=self.tokenizer)
            return classifier
        else:
            raise ValueError("Model and tokenizer not initialized.")


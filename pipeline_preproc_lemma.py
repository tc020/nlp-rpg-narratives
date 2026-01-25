import re
import spacy
from nltk.tokenize import word_tokenize

class TextPreprocessingPipeline:
    def __init__(self, spacy_model="de_core_news_sm"):
        print("Lade spaCy-Modell ...")
        self.nlp = spacy.load(spacy_model)

    """def normalize_and_tokenize(self, text):
        #text = text.lower()
        tokens = word_tokenize(text)
        return tokens"""
    
    def normalize_and_tokenize(self, text_or_tokens):
        if isinstance(text_or_tokens, list):
            text = " ".join(text_or_tokens)
        else:
            text = text_or_tokens

        text = text.lower()
        tokens = word_tokenize(text)
        return tokens


    def clean_tokens(self, tokens): #Von Satzzeichen und Ziffern bereinigen
        cleaned = [
            re.sub(r"[^\w\s]", "", token)
            for token in tokens
            if re.sub(r"[^\w\s]", "", token) and not token.isdigit()
        ]
        return cleaned

    def lemmatize(self, text):
        #doc = self.nlp(" ".join(tokens))
        doc = self.nlp(text)
        return [token.lemma_ for token in doc]


    def process_post(self, text, debug=False):
        if debug:
            print("\n--- Starte Verarbeitung für Post ---")
            print(f"Original: {text}")
            print("Typ lemmas:", type(lemmas))
            print("Typ tokens:", type(tokens))

        # 1. Lemmatisierung auf Rohtext
        lemmas = self.lemmatize(text)

        # 2. Lowercase + Tokenisierung
        tokens = self.normalize_and_tokenize(lemmas)

        # 3. Bereinigung
        cleaned_tokens = self.clean_tokens(tokens)

        # 4. Finaler String
        final_str = " ".join(cleaned_tokens)

        if debug:
            print(f"Bereinigter & lemmatisierter Post: {final_str}")
            print("--------------------------------------------------")

        return final_str


    def process_posts(self, posts, debug=False):
        return [self.process_post(p, debug=debug) for p in posts]


# --- Beispielnutzung ---
# pipeline = TextPreprocessingPipeline()
# posts_clean = pipeline.process_posts(posts, debug=True)

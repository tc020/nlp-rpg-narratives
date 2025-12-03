import re
import spacy
from nltk.tokenize import word_tokenize

class TextPreprocessingPipeline:
    def __init__(self, spacy_model="de_core_news_sm"):
        print("Lade spaCy-Modell ...")
        self.nlp = spacy.load(spacy_model)

    def normalize_and_tokenize(self, text):
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

    def lemmatize(self, tokens):
        doc = self.nlp(" ".join(tokens))
        return [token.lemma_ for token in doc]

    def process_post(self, text, debug=False):
        if debug:
            print(f"\n--- Starte Verarbeitung für Post ---")
            print(f"Original: {text}")

        # 1. Normalisierung & Tokenisierung
        tokens = self.normalize_and_tokenize(text)

        # 2. Bereinigung
        cleaned_tokens = self.clean_tokens(tokens)

        # 3. Lemmatisierung
        lemmas = self.lemmatize(cleaned_tokens)

        # 4. Finaler String
        final_str = " ".join(lemmas).lower()

        if debug:
            #print(f"\nLemmatisierte Wörter (Liste): {lemmas}")
            print(f"Bereinigter & lemmatsierter Post: {final_str}")
            print("--------------------------------------------------")

        return final_str

    def process_posts(self, posts, debug=False):
        return [self.process_post(p, debug=debug) for p in posts]


# --- Beispielnutzung ---
# pipeline = TextPreprocessingPipeline()
# posts_clean = pipeline.process_posts(posts, debug=True)

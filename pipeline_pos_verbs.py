import spacy

class VerbExtractionPipeline:
    def __init__(self, spacy_model="de_core_news_sm"):
        print("Lade spaCy-Modell für Verbextraktion ...")
        self.nlp = spacy.load(spacy_model)

    def extract_verbs(self, text, debug=False):
        if debug:
            print(f"\n--- Verarbeitung für Post (Verben behalten) ---")
            print(f"Original: {text}")

        doc = self.nlp(text)

        # spaCy POS-Tags für Verben im Deutschen
        # VERB = Vollverb, AUX = Hilfsverb (sein, haben, werden)
        verbs = [token.text for token in doc if token.pos_ in ("VERB", "AUX")]

        final_str = " ".join(verbs)

        if debug:
            print(f"Gefundene Verben: {verbs}")
            print(f"Finaler Verb-String: {final_str}")
            print("--------------------------------------------------")

        return final_str

    def process_posts(self, posts, debug=False):
        return [self.extract_verbs(p, debug=debug) for p in posts]

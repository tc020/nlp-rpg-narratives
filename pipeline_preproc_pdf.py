import re
import nltk
from nltk.tokenize import word_tokenize

#1) POSTS aus doc.spans["layout"] extrahieren (mit Link-Filter)
def extract_posts_from_layout(doc):
    posts = []
    current_post = ""

    #Regex für Links
    link_pattern = re.compile(r"(https?://\S+|www\.\S+)", re.IGNORECASE)

    for span in doc.spans["layout"]:

        #Abschnittsüberschrift ==> neuer Post
        if span.label_ == "section_header":
            if current_post.strip():
                posts.append(current_post.strip())
            current_post = ""
            continue

        #normaler Text
        if span.label_ == "text":
            text = span.text

            #Falls Link enthalten ==> überspringen
            if link_pattern.search(text):
                continue
            
            current_post += text + " "

    #letzten Post hinzufügen
    if current_post.strip():
        posts.append(current_post.strip())

    return posts



#2) POSTS mit Regex bereinigen
def clean_posts(posts):

    cleaned = []

    #2a: "von <Name> Verfasst: DATUM ZEIT" entfernen
    pattern_full = r"von\s+\w+(?:\s+\w+)*\s+Verfasst:\s+\d{2}\.\d{2}\.\d{4}\s+\d{2}:\d{2}"

    for t in posts:
        neu = re.sub(pattern_full, "", t).strip()
        cleaned.append(neu)

    #alle Zahlen entfernen
    cleaned = [re.sub(r"\d+", "", t).strip() for t in cleaned]

    #2b: 2-Wort-Posts löschen (meist nur "von Autor")
    cleaned = [s for s in cleaned if len(s.split()) != 2]

    #2c: "von <Name>" am Anfang löschen
    cleaned = [re.sub(r"^von\s+\w+\s+", "", t) for t in cleaned]

    #2d: Nochmals überall "Verfasst: DATUM ZEIT" löschen
    pattern_date = r"Verfasst:\s+\d{2}\.\d{2}\.\d{4}\s+\d{2}:\d{2}"
    cleaned = [re.sub(pattern_date, "", t).strip() for t in cleaned]

    #2e: leere Texte entfernen
    cleaned = [x for x in cleaned if x != ""]

    return cleaned

def clean_posts_from_direct_speech(posts):

    cleaned = []

    # 2a: "von <Name> Verfasst: DATUM ZEIT" entfernen
    pattern_full = r"von\s+\w+(?:\s+\w+)*\s+Verfasst:\s+\d{2}\.\d{2}\.\d{4}\s+\d{2}:\d{2}"

    for t in posts:
        neu = re.sub(pattern_full, "", t).strip()
        cleaned.append(neu)

    # Direkte Rede in allen Anführungszeichen entfernen
    quote_chars = r"[\"'„“‚‘»«›‹]"
    quote_pattern = rf"{quote_chars}[^\"'„“‚‘»«›‹]*{quote_chars}"
    cleaned = [re.sub(quote_pattern, "", t).strip() for t in cleaned]

    # >>> NEU: alle Zahlen entfernen
    cleaned = [re.sub(r"\d+", "", t).strip() for t in cleaned]

    # 2b: 2-Wort-Posts löschen (meist nur "von Autor")
    cleaned = [s for s in cleaned if len(s.split()) != 2]

    # 2c: "von <Name>" am Anfang löschen
    cleaned = [re.sub(r"^von\s+\w+\s+", "", t) for t in cleaned]

    # 2d: "Verfasst: DATUM ZEIT" entfernen (falls noch Reste)
    pattern_date = r"Verfasst:\s+\d{2}\.\d{2}\.\d{4}\s+\d{2}:\d{2}"
    cleaned = [re.sub(pattern_date, "", t).strip() for t in cleaned]

    # 2e: leere Texte entfernen
    cleaned = [x for x in cleaned if x != ""]

    return cleaned

import re
import string

def clean_posts_from_direct_speechV2(posts, debug=False):

    def dbg(label, value):
        if debug:
            print(f"[DEBUG] {label}: {value}")

    cleaned = []

    # 2a: "von <Name> Verfasst: DATUM ZEIT" entfernen
    pattern_full = r"von\s+\w+(?:\s+\w+)*\s+Verfasst:\s+\d{2}\.\d{2}\.\d{4}\s+\d{2}:\d{2}"

    for t in posts:
        orig = t
        neu = re.sub(pattern_full, "", t).strip()
        dbg("Original", orig)
        dbg("Nach Entfernen pattern_full", neu)
        cleaned.append(neu)

    # Direkte Rede entfernen
    quote_chars = r"[\"'„“‚‘»«›‹]"
    quote_pattern = rf"{quote_chars}[^\"'„“‚‘»«›‹]*{quote_chars}"
    cleaned2 = []
    for t in cleaned:
        new_t = re.sub(quote_pattern, "", t).strip()
        dbg("Nach Entfernen direkter Rede", new_t)
        cleaned2.append(new_t)
    cleaned = cleaned2

    # Zahlen entfernen
    cleaned2 = []
    for t in cleaned:
        new_t = re.sub(r"\d+", "", t).strip()
        dbg("Nach Entfernen Zahlen", new_t)
        cleaned2.append(new_t)
    cleaned = cleaned2

    # Satzzeichen entfernen
    punctuation_pattern = rf"[{re.escape(string.punctuation)}„”‚‘«»‹›]"
    cleaned2 = []
    for t in cleaned:
        new_t = re.sub(punctuation_pattern, "", t).strip()
        dbg("Nach Entfernen Satzzeichen", new_t)
        cleaned2.append(new_t)
    cleaned = cleaned2

    # 2b: 2-Wort-Posts löschen
    before = cleaned[:]
    cleaned = [s for s in cleaned if len(s.split()) != 2]
    dbg("Nach Entfernen 2-Wort-Posts", cleaned)

    # 2c: "von <Name>" am Anfang löschen
    cleaned2 = []
    for t in cleaned:
        new_t = re.sub(r"^von\s+\w+\s+", "", t)
        dbg("Nach Entfernen von <Name>", new_t)
        cleaned2.append(new_t)
    cleaned = cleaned2

    # 2d: Restliche "Verfasst: DATUM ZEIT" entfernen
    pattern_date = r"Verfasst:\s+\d{2}\.\d{2}\.\d{4}\s+\d{2}:\d{2}"
    cleaned2 = []
    for t in cleaned:
        new_t = re.sub(pattern_date, "", t).strip()
        dbg("Nach Entfernen pattern_date", new_t)
        cleaned2.append(new_t)
    cleaned = cleaned2

    # 2e: Leere Einträge entfernen
    before = cleaned[:]
    cleaned = [x for x in cleaned if x.strip() != ""]
    dbg("Endgültiges Ergebnis", cleaned)

    return cleaned


#3) Gesamtpipeline
def process_doc_into_posts(doc):
    posts = extract_posts_from_layout(doc)  #Posts extrahieren
    #final_posts = clean_posts(posts)        #Bereinigen
    print(posts)
    final_posts = clean_posts_from_direct_speech(posts, debug=True)
    return final_posts                      #Fertige Posts zurückgeben
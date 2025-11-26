import glob
from tqdm import tqdm
from PyPDF2 import PdfMerger
import spacy
from spacy_layout import spaCyLayout
import os


def load_and_merge_pdfs(folder_path, merged_filename="_combined.pdf"):
    # ---------------------------------------------------------
    # Findet alle PDFs in einem Ordner, merged sie zu einer Datei und gibt den Pfad zurück.
    # ---------------------------------------------------------

    #Alle PDF-Dateien im Ordner finden
    pdf_files = glob.glob(os.path.join(folder_path, "*.pdf"))

    if not pdf_files:
        raise FileNotFoundError(f"Keine PDFs gefunden in: {folder_path}")

    print("\nGefundene PDF-Dateien:")
    for pdf in pdf_files:
        print("  ", pdf)

    #Pfad für gemergtes PDF
    merged_pdf_path = os.path.join(folder_path, merged_filename)

    print("\n🔄 PDFs werden zusammengeführt...\n")
    merger = PdfMerger()

    for pdf in tqdm(pdf_files, desc="PDFs mergen"):
        merger.append(pdf)

    merger.write(merged_pdf_path)
    merger.close()

    print("\n✅ Erfolgreich gemerged zu:", merged_pdf_path)

    return merged_pdf_path



def load_spacy_layout_doc(merged_pdf_path):
    # ---------------------------------------------------------
    # Initialisiert spaCyLayout und lädt das gemergte PDF als Doc.
    # ---------------------------------------------------------

    nlp = spacy.blank("de")         #spaCy-Model
    layout = spaCyLayout(nlp)       #spaCyLayout-Wrapper

    print("\n📄 spaCyLayout liest das kombinierte PDF ein...\n")

    doc = layout(merged_pdf_path)

    print("spaCy-Model und -Wrapper geladen.")
    print("\nGesamtlänge des Textes:", len(doc.text))

    return doc



def process_pdf_folder(folder_path):
    merged_pdf = load_and_merge_pdfs(folder_path)   #PDFs mergen
    doc = load_spacy_layout_doc(merged_pdf)         #gemergtes PDF mit spaCyLayout einlesen
    return doc                                      #Doc zurückgeben

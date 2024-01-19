import os
import numpy as np
import scipy as sp
import ix as ix
from whoosh.fields import Schema, TEXT
from whoosh.index import create_in, open_dir
from whoosh.qparser import QueryParser
from whoosh.searching import Searcher

def indexeaza_fisiere(txt_files, index_path):
    # Definirea schemei (structura) indexului
    schema = Schema(content=TEXT)

    # Crearea unui director pentru index (dacă nu există)
    if not os.path.exists(index_path):
        os.makedirs(index_path)

    index = create_in(index_path, schema)

    # Deschiderea indexului pentru scriere
    writer = index.writer()

    for txt_file in txt_files:
        indexeaza_fisier(writer, txt_file)

    # Salvarea modificărilor
    writer.commit()


def indexeaza_fisier(writer, file_path):
    with open(file_path, 'r', encoding='latin-1') as file:
        content = file.read()

    # Adăugarea unui document în index
    writer.add_document(content=content)


# Caută în index pe baza întrebării

# Caută în index pe baza întrebării și returnează rezultatele
def cauta_in_index(intrebare, index_path):
    # Deschiderea indexului pentru căutare
    index = open_dir(index_path)

    # Crearea unui obiect QueryParser pentru a transforma întrebarea într-o interogare
    query_parser = QueryParser("content", schema=index.schema)

    # Interogare
    query = query_parser.parse(intrebare)

    # Deschiderea searcher-ului și căutarea
    with index.searcher() as searcher:
        # Căutarea directă
        results = searcher.search(query)

    return results





# Exemplu de utilizare
folder_input = "wikipediaDataMining2"
folder_output = "IndexedFiles"
index_path = os.path.join(folder_output, "index")

# Construiește lista cu fișierele .txt din directorul de intrare
fisiere_txt = [os.path.join(folder_input, f) for f in os.listdir(folder_input) if f.endswith(".txt")]

# Indexează fișierele .txt
indexeaza_fisiere(fisiere_txt, index_path)

# Efectuează o căutare în funcție de întrebare
intrebare = "England"
results = cauta_in_index(intrebare, index_path)

if results:
    first_result_content = results[0].get("content", "Conținutul nu este disponibil")
    # Poți face aici orice altă verificare sau procesare a conținutului primului rezultat
else:
    print("Nu s-au găsit rezultate pentru întrebare.")

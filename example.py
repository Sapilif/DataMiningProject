from whoosh.fields import Schema, TEXT, ID
from whoosh import index
from whoosh.qparser import QueryParser
import os.path

# Creare director pentru index
index_dir = "dir"
if not os.path.exists(index_dir):
    os.mkdir(index_dir)

# Definire schema
schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT(stored=True))

# Creare index
ind = index.create_in(index_dir, schema)

# Citire conținut din fișier .txt și adăugare în index
file_path = "wikipediaDataMining2/test.txt"
with open(file_path, 'r', encoding='utf-8') as file:
    file_content = file.read()

# Adăugare document în index
with ind.writer() as writer:
    writer.add_document(title=u"doc", content=file_content, path=u"/a")

# Căutare în index
with ind.searcher() as searcher:
    query = QueryParser("content", ind.schema).parse("england")
    results = searcher.search(query, terms=True)
    for r in results:
        print(r, r.score)
        if results.has_matched_terms():
            print(results.matched_terms())

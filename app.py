import json
import chromadb

with open('biblia_acf.json', 'r', encoding='utf-8') as f:
    bible = json.load(f)


documents = []
metadata = []
ids = []

for book in bible:
    book_name = book.get("name")
    book_abbreviation = book.get("abbrev")

    for chapter_id, chapter in enumerate(book.get('chapters', []), start=1):
        for i_verse, verse in enumerate(chapter, start=1):
            verse_id = f"{book_abbreviation}.{chapter_id}.{i_verse}"

            text = verse.strip()
            if not text:
                continue

            documents.append(text)
            metadata.append({
                "book": book_name,
                "chapter": chapter_id,
                "verse": verse_id,
                "reference": f"{book_name} {chapter_id}:{verse_id}"
            })
            ids.append(verse_id)

print(f"Total of loaded verse: {len(documents)}.")


client = chromadb.PersistentClient(path="/chrome_bible")
collection = client.get_or_create_collection(name="hole_bible")

batch_size = 500
for i in range(0, len(documents), batch_size):
    collection.add(
        ids=ids[i:i+batch_size],
        documents=documents[i:i+batch_size],
        metadata=metadata[i:i+batch_size]
    )

print(f"Collection populated in {collection.count()}.")


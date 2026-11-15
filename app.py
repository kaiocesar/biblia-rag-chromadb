import json

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
            verse_id = f"{book_abbreviation}.{chapter_id}.{verse_id}"

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
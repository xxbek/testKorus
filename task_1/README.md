1. Start DB server (Postgres)
2. Translate initial .scv row name to English, like in real DB:

    books:
    - id (int)
    - name (text)
    - author (text)
    - publishing_office (text)
    - publication_city (text)
    - page_number (int)
    - instance_id (int)
    - admission_date (date)
    
    book_lending:
    - id (int)
    - issue_date (date)
    - return_date (date)
    - id_card_number (int)
    
    readers:
    - id (int)
    - surname (text)
    - name (text)
    - patronymic (text)
    - birthday (date)
    - sex (text)
    - address (text)
    - phone (text)

3. Import data from .csv to DB using Datagrip
4. Write requests and test them

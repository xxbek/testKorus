-- -- 1
SELECT publication_city
FROM book
WHERE EXTRACT('Year' FROM date(admission_date)) - 5 = 2016
GROUP BY publication_city
HAVING COUNT(*) = (
    SELECT COUNT(*) as published_book_amount
    FROM book
    WHERE EXTRACT('Year' FROM date(admission_date)) - 5 = 2016
    GROUP BY publication_city
    ORDER BY published_book_amount DESC
    LIMIT 1
    )

-- -- 2

SELECT book.name, book.author, count(*)
FROM book
GROUP BY book.name, book.author
HAVING book.name = 'Война и мир' and book.author = 'Л.Н.Толстой'

/*
Схема базы составлена некорректно для этого задания. Таблица "Книги" представляет из себя уникальные строки на каждую книгу.
Однако столбец "ID экземпляра" подразумевает множественные значения -
нам нужно повторять строку для описания следующего экземпляра одной и той же книги.
Таким образом нарушен один из принципов нормализации БД.

Выход из этой проблемы - удаление поля "ID экземпляра" и создание таблицы "Экземпляры"("id", "book_id")
с внешним ключом к таблице "Книги" (один ко многим).
Так же некорректным я считаю поле "ID экземпляра" в таблице "Выдачи книг". Это поле является Primary Key, хотя должно
быть ссылкой на экземпляр книги к таблице "Экземпляры".

На проекте в таких ситуациях я разговаривал с тимлидом и указывал на явную ошибку проектирования.
Запрос исходя из таблицы instances("id", "book_id"):

SELECT book.name, book.author, COUNT(*)
FROM book
JOIN instances
ON instances.book_id = book.id
WHERE book.name = 'Война и мир' and book.author LIKE '%Толстой%'
GROUP BY book.name, book.author

*/

-- -- 3

SELECT readers.name, readers.surname, readers.birthday, count(*) as lended_books
FROM  readers
JOIN book_lending
ON readers.id = book_lending.id_card_number
GROUP BY readers.id, readers.name, readers.surname, readers.birthday
HAVING count(*) = (
    SELECT count(*)
    FROM  readers
    JOIN book_lending
    ON readers.id = book_lending.id_card_number
    GROUP BY readers.id, readers.name, readers.surname, readers.birthday
    ORDER BY 1 DESC
    LIMIT 1
    )
ORDER BY birthday DESC


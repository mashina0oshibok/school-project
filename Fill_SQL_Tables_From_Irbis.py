import irbis
import SQL_Databases
from config import *

# Connect to SQL databases
authors_table = SQL_Databases.AuthorsDatabase(Database_path)
books_table = SQL_Databases.BooksDatabase(Database_path)

# Connect to Irbis64 server
irbis64_client = irbis.Connection()
irbis64_client.parse_connection_string(
    f"host={Irbis_Host};port={Irbis_Port};database={Irbis_database_name};user={Irbis_User};password={Irbis_Password};")
irbis64_client.connect()

if not irbis64_client.connected:
    print('Connection Error!')
    exit(1)

# Execute search in Irbis64 server database
found = irbis64_client.search('"A=$"')
print(f'Records count: {len(found)}')

# Execute transfer of each record
for mfn in found:
    try:
        # Read the record from the server
        record = irbis64_client.read_record(mfn)

        # Add author to SQL database
        surname = record.fm(700, 'a')
        initials = record.fm(700, 'b')
        decryption = record.fm(700, 'g')

        # Check author existence in SQL database
        if surname is not None:
            if not authors_table.author_exists_by_name(surname, initials, decryption):
                authors_table.add_author(surname, initials, decryption)
            author_id = authors_table.get_author_by_name(surname, initials, decryption)[0]['[id]']
        else:
            surname = initials = decryption = "No author"
            if not authors_table.author_exists_by_name(surname, initials, decryption):
                authors_table.add_author(surname, initials, decryption)
            author_id = authors_table.get_author_by_name(surname, initials, decryption)[0]['[id]']

        # Add book to SQL database
        title = record.fm(200, 'a')
        subtitle_information = record.fm(200, 'e')
        authors = record.fm(200, 'f')
        if title is None:
            raise Exception("book with no title was skipped")

        # print(record)
        total_amount = sum(map(int, record.fma(910, '1')))
        issued_amount = sum(map(int, record.fma(910, '2')))

        # Check book existence in SQL database
        book_id = books_table.get_book(title, subtitle_information, author_id)
        if len(book_id) == 0:
            books_table.add_book(title, subtitle_information, authors, total_amount, issued_amount, author_id)
        else:
            book_id = book_id[0]['[id]']
            books_table.change_book_total_amount(book_id, total_amount)
            books_table.change_book_issued_amount(book_id, issued_amount)
    except Exception as exception:
        print(exception)

# Disconnect from Irbis server
irbis64_client.disconnect()

# Disconnect from SQL databases
authors_table.close()
books_table.close()

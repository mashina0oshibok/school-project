import sqlite3
# import telebot
from datetime import datetime


class SQLDatabase:
    def __init__(self, database_path):
        self.connection = sqlite3.connect(database_path, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def get_column_names(self, table_name):
        """:return: list of column names (each is enclosed in [])"""
        columns_info = self.cursor.execute(f'PRAGMA table_info([{table_name}])').fetchall()
        column_names = [f"[{column_info[1]}]" for column_info in columns_info]
        return column_names

    def get_all_records(self, table_name):
        """:return: list of dictionaries representing records (columns = keys)"""
        with self.connection:
            search = self.cursor.execute(f"SELECT * FROM [{table_name}]").fetchall()
            return self.search_result_to_dict(table_name, search)

    def get_records_by_value(self, table_name, key_column_name, value):
        """
        looking for records with 'value' in column 'key_column_name'
        :return: list of dictionaries representing records (columns = keys)
        """
        with self.connection:
            search = self.cursor.execute(
                f"SELECT * FROM [{table_name}] WHERE [{key_column_name}] = '{value}'").fetchall()
            return self.search_result_to_dict(table_name, search)

    def search_result_to_dict(self, table_name, search):
        """
        assigns column_names (= keys) to search results (= values)
        :return: list of dictionaries representing records (columns = keys, search results = values)
        """
        columns = self.get_column_names(table_name)
        result = []
        for i in range(len(search)):
            result.append({columns[j]: search[i][j] for j in range(len(columns))})
        return result

    def record_exists(self, table_name, key_column_name, desired_value):
        """checks if record with 'desired_value' value in column 'key_column_name' exists"""
        with self.connection:
            result = self.cursor.execute(
                f"SELECT * FROM [{table_name}] WHERE [{key_column_name}] = {desired_value}").fetchall()
            return len(result) > 0

    def add_record(self, table_name, start_column, *args):
        """
        adds a record (with *args values) to table
        :param table_name name of the table you want to be recorded
        :param start_column column from which recording begins
        :return: True if the operation completed successfully, False if not
        """
        try:
            columns = self.get_column_names(table_name)
            columns_to_complete = columns[start_column:len(columns)]
            columns_in_request = ", ".join(columns_to_complete)
            with self.connection:
                self.cursor.execute(
                    f"INSERT INTO [{table_name}] ({columns_in_request}) " +
                    f"VALUES ({'?, ' * (len(columns_to_complete) - 1) + '?'})", args)
            return True
        except sqlite3.Error as exception:
            # TODO: add logging to errors
            print(exception)
            return False

    def close(self):
        self.connection.close()


class UsersDatabase(SQLDatabase):
    def __init__(self, database_path, db_name="users"):
        """extends SQLDatabase()"""
        super().__init__(database_path)
        self.db_name = db_name

    def get_users(self):
        """
        extends SQLDatabase.get_all_records()
        :return: list of dictionaries representing records (columns = keys)
        """
        return self.get_all_records(self.db_name)

    def get_user_by_id(self, user_id):
        """
        extends SQLDatabase.get_records_by_desired_value()
        :param user_id should be unique column
        :return: dictionary representing record (columns = keys)
        :exception user_id should be unique column, but wasn't
        """
        result = self.get_records_by_value(self.db_name, "user id", user_id)
        if len(result) > 1:
            Exception("user_id should be unique column, but wasn't")
        return result[0]

    def user_exists(self, user_id):
        """
        extends SQLDatabase.record_exists()
        :return: True if user with 'user_id' exists otherwise False
        """
        return self.record_exists(self.db_name, "user id", user_id)

    # def add_user(self, user: type(telebot.types.User)):
    #     """
    #     extends SQLDatabase.add_record()
    #     :return: True if the operation completed successfully, False if not
    #     """
    #     return self.add_record(self.db_name, 0, user.id, user.first_name, user.last_name, user.username)

    def add_user(self, user_id, user_first_name, user_last_name, user_username):
        """
        extends SQLDatabase.add_record()
        :return: True if the operation completed successfully, False if not
        """
        return self.add_record(self.db_name, 0, user_id, user_first_name, user_last_name, user_username)


class AuthorsDatabase(SQLDatabase):
    def __init__(self, database_path, db_name="authors"):
        """extends SQLDatabase()"""
        super().__init__(database_path)
        self.db_name = db_name

    def get_authors(self):
        """
        extends SQLDatabase.get_all_records()
        :return: list of dictionaries representing records (columns = keys)
        """
        return self.get_all_records(self.db_name)

    def get_author_by_id(self, author_id):
        """
        extends SQLDatabase.get_records_by_desired_value()
        :param author_id should be unique column
        :return: dictionary representing record (columns = keys)
        :exception author_id should be unique column, but wasn't
        """
        result = self.get_records_by_value(self.db_name, "id", author_id)
        if len(result) > 1:
            Exception("user_id should be unique column, but wasn't")
        return result[0]

    def get_author_by_name(self, surname, initials, decryption):
        """
        extends SQLDatabase.get_records_by_desired_value()
        :return: list of dictionaries representing authors records with 'surname', 'initials', 'decryption'
        (columns = keys)
        """
        with self.connection:
            command = f"SELECT * FROM [{self.db_name}] WHERE surname = '{surname}'"
            if initials is not None:
                command += f" AND initials = '{initials}'"
            if decryption is not None:
                command += f" AND decryption = '{decryption}'"
            search = self.cursor.execute(command).fetchall()
            return self.search_result_to_dict(self.db_name, search)

    def author_exists(self, author_id):
        """
        extends SQLDatabase.record_exists()
        :return: True if author with 'author_id' exists otherwise False
        """
        return self.record_exists(self.db_name, "id", author_id)

    def author_exists_by_name(self, surname, initials, decryption):
        with self.connection:
            command = f"SELECT * FROM [{self.db_name}] WHERE surname = '{surname}'"
            if initials is not None:
                command += f" AND initials = '{initials}'"
            if decryption is not None:
                command += f" AND decryption = '{decryption}'"
            search = self.cursor.execute(command).fetchall()
            return len(search) > 0

    def add_author(self, surname, initials, decryption):
        """
        extends SQLDatabase.add_record()
        :return: True if the operation completed successfully, False if not
        """
        return self.add_record(self.db_name, 1, surname, initials, decryption)


class BooksDatabase(SQLDatabase):
    def __init__(self, database_path, db_name="books"):
        """extends SQLDatabase()"""
        super().__init__(database_path)
        self.db_name = db_name

    def get_books(self):
        """
        extends SQLDatabase.get_all_records()
        :return: list of dictionaries representing records (columns = keys)
        """
        return self.get_all_records(self.db_name)

    def get_book_by_id(self, book_id):
        """
        extends SQLDatabase.get_records_by_desired_value()
        :param book_id should be unique column
        :return: dictionary representing record (columns = keys)
        :exception book_id should be unique column, but wasn't
        """
        result = self.get_records_by_value(self.db_name, "id", book_id)
        if len(result) > 1:
            Exception("book id should be unique column, but wasn't")
        return result[0]

    def get_books_by_title(self, title):
        """
        extends SQLDatabase.get_records_by_desired_value()
        :return: list of dictionaries representing books records with 'title' in 'title' column (columns = keys)
        """
        return self.get_records_by_value(self.db_name, "title", f"'{title}'")

    def get_books_with_title_occurrence(self, title):
        """
        extends SQLDatabase.get_records_by_desired_value()
        :return: list of dictionaries representing books records
        with an occurrence of the word 'title' in 'title' column (columns = keys)
        """
        with self.connection:
            search = self.cursor.execute(
                f"SELECT * FROM [{self.db_name}] WHERE title LIKE \"%{title}%\" ORDER BY title").fetchall()
            return self.search_result_to_dict(self.db_name, search)

    def get_author_books(self, author_id):
        """
        extends SQLDatabase.get_records_by_desired_value()
        :return: list of dictionaries representing books records
        with 'author_id' in 'first author id' column (columns = keys)
        """
        with self.connection:
            search = self.cursor.execute(
                f"SELECT * FROM [{self.db_name}] WHERE [first author id] = {author_id}").fetchall()
            return self.search_result_to_dict(self.db_name, search)

    def get_book(self, title, subtitle_information, author_id):
        with self.connection:
            search = self.cursor.execute(
                f"SELECT * FROM [{self.db_name}] WHERE [title] = '{title}' AND " +
                f"[subtitle information] = '{subtitle_information}' AND [first author id] = {author_id}").fetchall()
            return self.search_result_to_dict(self.db_name, search)

    # def book_exists(self, title):
    #     """
    #     extends SQLDatabase.record_exists()
    #     :return: True if book with 'title' exists otherwise False
    #     """
    #     return self.record_exists(self.db_name, "title", f"'{title}'")

    def book_exists(self, title, subtitle_information, author_id):
        """
        extends SQLDatabase.record_exists()
        :return: True if book with 'title' exists otherwise False
        """
        with self.connection:
            search = self.cursor.execute(
                f"SELECT * FROM [{self.db_name}] WHERE [title] = '{title}' AND " +
                f"[subtitle information] = '{subtitle_information}' AND [first author id] = {author_id}")\
                .fetchall()
            return len(search) > 0

    def add_book(self, title, subtitle_information, authors, total_amount, issued_amount, first_author_id):
        """
        extends SQLDatabase.add_record()
        :return: True if the operation completed successfully, False if not
        """
        return self.add_record(
            self.db_name, 1, title, subtitle_information, authors, total_amount, issued_amount, first_author_id)

    def change_book_total_amount(self, book_id, new_total_amount):
        with self.connection:
            self.cursor.execute(
                f"UPDATE [{self.db_name}] SET [total amount] = {new_total_amount} WHERE id = {book_id}")

    def change_book_issued_amount(self, book_id, new_issued_amount):
        with self.connection:
            self.cursor.execute(
                f"UPDATE [{self.db_name}] SET [issued amount] = {new_issued_amount} WHERE id = {book_id}")


class RequestsDatabase(SQLDatabase):
    def __init__(self, database_path, db_name="requests"):
        """extends SQLDatabase()"""
        super().__init__(database_path)
        self.db_name = db_name

    @staticmethod
    def get_request_id(user_id, book_id):
        """request_id is connected with 'user_id', 'book_id'"""
        return f"{user_id}-{book_id}"

    def get_requests(self):
        """
        extends SQLDatabase.get_all_records()
        :return: list of dictionaries representing requests records (columns = keys)
        """
        return self.get_all_records(self.db_name)

    def get_request_by_id(self, request_id):
        """
        extends SQLDatabase.get_records_by_desired_value()
        :param request_id should be unique column
        :return: dictionary representing request record (columns = keys)
        :exception request_id should be unique column, but wasn't
        """
        result = self.get_records_by_value(self.db_name, "id", request_id)
        if len(result) > 1:
            Exception("request id should be unique column, but wasn't")
        return result[0]

    def get_requests_by_user_id(self, user_id):
        """
        extends SQLDatabase.get_records_by_desired_value()
        :return: list of dictionaries representing requests records
        with 'user_id' in 'user id' column (columns = keys)
        """
        with self.connection:
            search = self.cursor.execute(
                f"SELECT * FROM [{self.db_name}] WHERE [user id] = {user_id} ORDER BY date DESC, time").fetchall()
            return self.search_result_to_dict("requests", search)

    def get_user_requests_count(self, user_id):
        """
        extends RequestsDatabase.get_requests_by_user_id()
        :return: count of user requests
        """
        return len(self.get_requests_by_user_id(user_id))

    def get_requests_by_book_id(self, book_id):
        """
        extends SQLDatabase.get_records_by_desired_value()
        :return: list of dictionaries representing requests records
        with 'book_id' in 'book id' column (columns = keys)
        """
        with self.connection:
            search = self.cursor.execute(
                f"SELECT * FROM [{self.db_name}] WHERE [book id] = {book_id} ORDER BY [creation datetime] DESC")\
                .fetchall()
            return self.search_result_to_dict(self.db_name, search)

    def get_book_requests_count(self, book_id):
        """
        extends RequestsDatabase.get_requests_by_book_id()
        :return: count of book requests
        """
        return len(self.get_requests_by_book_id(book_id))

    def get_request_creation_datetime(self, request_id):
        """:return: datetime if the operation completed successfully, None if not"""
        search_result = self.cursor.execute(
            f"SELECT [creation datetime] FROM requests WHERE id = '{request_id}'").fetchall()
        try:
            result = datetime.strptime(search_result[0][0], " %Y-%m-%d %H:%M:%S")
            return result
        except sqlite3.Error as exception:
            print(exception)
            return None

    def get_request_notification_datetime(self, request_id):
        """:return: datetime if the operation completed successfully, None if not"""
        search_result = self.cursor.execute(
            f"SELECT [notification datetime] FROM requests WHERE id = '{request_id}'").fetchall()
        try:
            result = datetime.strptime(search_result[0][0], " %Y-%m-%d %H:%M:%S")
            return result
        except sqlite3.Error as exception:
            print(exception)
            return None

    def get_request_days_to_receive(self, request_id):
        """:return: datetime if the operation completed successfully, None if not"""
        search_result = self.cursor.execute(
            f"SELECT [days to receive] FROM requests WHERE id = '{request_id}'").fetchall()
        return search_result[0][0]

    def change_request_days_to_receive(self, request_id, new_days_to_receive):
        with self.connection:
            self.cursor.execute(
                f"UPDATE [{self.db_name}] SET [days to receive] = {new_days_to_receive} WHERE id = '{request_id}'")

    def request_exists(self, request_id):
        """
        extends SQLDatabase.record_exists()
        :return: True if request with 'request_id' exists otherwise False
        """
        return self.record_exists(self.db_name, "id", f"'{request_id}'")

    def user_request_exists(self, user_id):
        """
        extends SQLDatabase.record_exists()
        :return: True if request with 'user_id' in 'user id' column exists otherwise False
        """
        return self.record_exists(self.db_name, "user id", user_id)

    def book_request_exists(self, book_id):
        """
        extends SQLDatabase.record_exists()
        :return: True if request with 'book_id' in 'book id' column exists otherwise False
        """
        return self.record_exists(self.db_name, "book id", book_id)

    def delete_request(self, request_id):
        """:return: True if request was deleted successfully otherwise False"""
        try:
            with self.connection:
                self.cursor.execute(f"DELETE FROM [{self.db_name}] WHERE id = '{request_id}'")
            return True
        except sqlite3.Error as exception:
            print(exception)
            return False

    def add_user_request(self, user_id, book_id, days_to_receive=1):
        """
        extends SQLDatabase.add_record()
        :return: True if the operation completed successfully, False if not
        """
        datetime_format = "%Y-%m-%d %H:%M:%S"
        return self.add_record(
            "requests", 0, f"{user_id}-{book_id}", user_id, book_id, f"{datetime.now(): {datetime_format}}", 0, None,
            days_to_receive)

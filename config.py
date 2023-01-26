Database_path = "SQLite3DataBase.db"

Irbis_Host = "999.999.9.999"
Irbis_Port = "6666"
Irbis_database_name = "IBIS"
Irbis_User = "1"
Irbis_Password = "1"

Start_Message = """
We haven't created a start message yet
"""

Create_Authors_Table = """
CREATE TABLE authors (
    id         INTEGER      PRIMARY KEY
                            NOT NULL
                            UNIQUE,
    surname    VARCHAR (50) NOT NULL,
    initials   VARCHAR (20),
    decryption VARCHAR (50)
);
"""

Create_Books_Table = """
CREATE TABLE books (
    id                           INTEGER       PRIMARY KEY
                                               UNIQUE
                                               NOT NULL,
    title                        VARCHAR (50)  NOT NULL,
    [subtitle information]       VARCHAR (50)  ,
    [responsibility information] VARCHAR (100) ,
    [total amount]               INTEGER       NOT NULL,
    [issued amount]              INTEGER       NOT NULL,
    [first author id]            INTEGER       NOT NULL
                                               REFERENCES authors (id) ON DELETE RESTRICT
                                                                       ON UPDATE CASCADE
);
"""

Create_Users_Table = """
CREATE TABLE users (
    [user id]    INTEGER      PRIMARY KEY
                              UNIQUE
                              NOT NULL,
    [first name] VARCHAR (50),
    [last name]  VARCHAR (50),
    username     VARCHAR (50) 
);
"""

Create_Requests_Table = """
CREATE TABLE requests (
    id                      STRING   PRIMARY KEY
                                     UNIQUE
                                     NOT NULL,
    [user id]               INTEGER  NOT NULL
                                     REFERENCES users ([user id]) ON DELETE RESTRICT
                                                                  ON UPDATE CASCADE,
    [book id]               INTEGER  NOT NULL
                                     REFERENCES books (id) ON DELETE RESTRICT
                                                           ON UPDATE CASCADE,
    [creation datetime]     DATETIME NOT NULL,
    [was notified]          BOOLEAN  NOT NULL,
    [notification datetime] DATETIME,
    [days to receive]       INTEGER  NOT NULL
);
"""

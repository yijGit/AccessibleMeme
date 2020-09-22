import sqlite3
from sqlite3 import Error
from sys import argv
from search import descript
 
# create a database connection to the SQLite database
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return conn

# create a table from the create_table_sql statement
def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

# inserts meme name into NAMES table
# returns row ID 
def insert_meme(conn, meme):
    sql = ''' INSERT INTO names(name)
              VALUES(?) '''
    cur = conn.cursor()
    cur.execute(sql, (meme,))
    return cur.lastrowid

# inserts meme description into DESCRIPTIONS table
# returns row ID 
def insert_description(conn, description):
    sql = ''' INSERT INTO descriptions(description,meme_id)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, description)
    return cur.lastrowid

# inserts meme image into IMAGES table
# returns row ID 
def insert_image(conn, image):
    sql = ''' INSERT INTO images(image,meme_id)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, image)
    return cur.lastrowid

def create_db():
    database = r"/Users/jlyi/Desktop/Sy 19-20/Spring/IW/IW-Spring-2020/memes.db"
 
    sql_create_names_table = """CREATE TABLE IF NOT EXISTS names (
                                    meme_id integer PRIMARY KEY,
                                    name text NOT NULL
                                    );"""
 
    sql_create_descriptions_table = """CREATE TABLE IF NOT EXISTS descriptions (
                                    description text NOT NULL,
                                    meme_id integer NOT NULL,
                                    FOREIGN KEY (meme_id) REFERENCES names (meme_id)
                                );"""

    sql_create_images_table = """CREATE TABLE IF NOT EXISTS images (
                                    image text NOT NULL,
                                    meme_id integer NOT NULL,
                                    FOREIGN KEY (meme_id) REFERENCES names (meme_id)
                                );"""
 
    # create a database connection
    conn = create_connection(database)
 
    # create tables
    if conn is not None:
        # create name table
        create_table(conn, sql_create_names_table)
 
        # create decription table
        create_table(conn, sql_create_descriptions_table)

        # create image table
        create_table(conn, sql_create_images_table)
    else:
        print("Error! cannot create the database connection.")

    # create entries in the tables
    # initializes a db with two initial entries
    with conn:
        # create a name entry
        meme1 = ("Spider-Man Pointing at Spider-Man")
        meme_id1 = insert_meme(conn, meme1)

        meme2 = ("I Am Once Again Asking for Your Financial Support")
        meme_id2 = insert_meme(conn, meme2)
 
        # create a description entry
        description1 = (descript(meme1), meme_id1)
        insert_description(conn, description1)

        description2 = (descript(meme2), meme_id2)
        insert_description(conn, description2)

        # create an image entry
        image1 = ("spiderman-point.jpg", meme_id1)
        insert_image(conn, image1)

        image2 = ("bernie.jpg", meme_id2)
        insert_image(conn, image2)

        conn.commit()
    return conn

# retrieve all the images from the IMAGES table
def select_all_images(conn):
    cur = conn.cursor()
    cur.execute("SELECT image FROM images")
    rows = cur.fetchall()
    return rows

# retrieve all the names from the NAMES table
def select_all_names(conn):
    cur = conn.cursor()
    cur.execute("SELECT name FROM names")
    rows = cur.fetchall()
    return rows

# retrieve all the names from the DESCRIPTIONS table
def select_all_descriptions(conn):
    cur = conn.cursor()
    cur.execute("SELECT description FROM descriptions")
    rows = cur.fetchall()
    return rows

# create a new entry in the meme database
# insert the name, img, and description of meme
def insert_entry(argv):
    img = argv[1]
    name = (argv[2])
    database = r"/Users/jlyi/Desktop/Sy 19-20/Spring/IW/IW-Spring-2020/memes.db"
    conn = create_connection(database)
    with conn:
        meme_id = insert_meme(conn, name)
        print(meme_id)
        image = (img, meme_id)
        insert_image(conn, image)
        description = (descript(name), meme_id)
        insert_description(conn, description)
        conn.commit()
    return conn

if __name__ == '__main__':
    if (len(argv) == 1):
        conn = create_db()
    else:
        conn = insert_entry(argv)
    conn.close()
import sqlite3
import os


class DBManager:

    # Boolean check if table exists
    database_exists = os.path.exists('database.db')

    # Create Connection object (database)
    conn = sqlite3.connect('database.db')

    # Create Cursor object to navigate database
    curs = conn.cursor()

    # Constructor
    def __init__(self):

        # If there is no database, create one (with tables)
        if not self.database_exists:
            self.create_tables()

        # Save (commit) the changes
        self.conn.commit()

    # Create tables in a fresh database
    def create_tables(self):

        self.curs.execute('''CREATE TABLE ipaddress
                                     (ipaddressID integer PRIMARY KEY, ipaddress text)''')
        self.curs.execute('''CREATE TABLE links
                                             (linkID integer PRIMARY KEY, link text)''')
        self.curs.execute('''CREATE TABLE connections
                                             (ipaddressID integer, linkID integer, numConnections integer DEFAULT 1)''')

    def insert_multiple_ips(self, ips):
        for ip in ips:
            self.insert_ip(ip)

    def insert_ip(self, ip):

        self.curs.execute("INSERT INTO ipaddress(ipaddress) VALUES (?) EXCEPT SELECT ipaddress from ipaddress where "
                          "ipaddress = ?", [ip, ip])

        # Save (commit) the changes
        self.conn.commit()

    def insert_multiple_links(self, links):
        for link in links:
            self.insert_link(link)

    def insert_link(self, link):

        self.curs.execute("INSERT INTO links(link) VALUES (?) EXCEPT "
                          "SELECT link from links where link = ?", [link, link])

        # Save (commit) the changes
        self.conn.commit()

    def insert_multiple_connections(self, connections):
        for connection in connections:
            self.insert_connection(connection)

    # Create a new connection row or update existing with a given IP and Link (num already defaults to 1)
    def insert_connection(self, connection):

        # Update (+1) existing connection, if it exists
        self.curs.execute("UPDATE connections SET numConnections = numConnections + 1 WHERE ipaddressID = (SELECT "
                          "ipaddressID FROM ipaddress where ipaddress = ? LIMIT 1) and linkID = (SELECT linkID from "
                          "links where link = ? LIMIT 1)", connection)

        # Create new connection, if one doesn't exist
        self.curs.execute("INSERT INTO connections(ipaddressID, linkID) VALUES ((SELECT ipaddressID FROM ipaddress "
                          "WHERE ipaddress = ? LIMIT 1), (SELECT linkID FROM links WHERE link = ? LIMIT 1)) EXCEPT "
                          "SELECT ipaddressID, linkID from connections where ipaddressID = (SELECT ipaddressID FROM "
                          "ipaddress WHERE ipaddress = ? LIMIT 1) and linkID = (SELECT linkID FROM links WHERE link = "
                          "? LIMIT 1)", connection+connection)

        # Save (commit) the changes
        self.conn.commit()

    # Return a numlinks long list of random links
    def get_links(self, numlinks):

        # 'Randomly' select a batch of links.
        self.curs.execute("SELECT link FROM links ORDER BY RANDOM() LIMIT ?", [numlinks])

        links_list = []

        # Fill links_list with the query results
        for useless_tuple in self.curs.fetchall():
            links_list.append(useless_tuple[0])

        return links_list

    # Closes connection when done
    def close(self):

        # Save (commit) the changes
        self.conn.commit()

        # Close connection
        self.conn.close()

import sys,os
import sqlite3

class MainApplication():
    def __init__(self, mainWindow):
        self.mainWindow = mainWindow
        self.mainWindow.show()
        # data = self.checkDB()
        # self.mainWindow.setTable(data)
        

    def checkDB(self):
        c = self.db_connection.cursor()
        # c.execute(""" 
        # CREATE TABLE IF NOT EXISTS storage_capacity(
            # id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            # storage varchar(200) default null,
            # coal_cap float default null,
            # pellet_cap float default null,
            # iron_cap float default null
        # )
        # """)
        # c.execute(""" 
        # CREATE INDEX storage ON storage_capacity (storage)
        # """)
        # c.execute(""" 
        # CREATE INDEX coal_cap ON storage_capacity (coal_cap)
        # """)
        # c.execute(""" 
        # CREATE INDEX pellet_cap ON storage_capacity (pellet_cap)
        # """)
        # c.execute(""" 
        # CREATE INDEX iron_cap ON storage_capacity (iron_cap)
        # """)
        # self.db_connection.commit()
        # c.execute("insert into storage_capacity (storage,coal_cap,pellet_cap,iron_cap) VALUES('ТестРус',55.5,23.3,125.2)")
        # c.execute("DELETE from storage_capacity")
        # self.db_connection.commit()
        c.execute("""
        SELECT * from storage_capacity
        """)
        res = c.fetchall()
        print(res)
        return res
import sys,os
import sqlite3
db = "den"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, db + ".db")
db_connection = sqlite3.connect(db_path)



class Meteo():
    def __init__(self, windV, windStart, windEnd, precipitation):
        self.windV = windV
        self.windStart = windStart
        self.windEnd = windEnd
        self.precipitation = precipitation

        
        
class Cargo():
    def __init__(self, id=None, type=None):
        self.id = id
        self.type = type
        
    def save(self):
        c = db_connection.cursor()
        c.execute("insert into cargo_types (name) VALUES('" + self.type + "')")
        db_connection.commit()
        
    def delete(self, id):
        c = db_connection.cursor()
        c.execute("DELETE FROM cargo_types WHERE id = " + id + " ")
        db_connection.commit()
        
    def find(self, id):
        c = db_connection.cursor()
        c.execute("select * from cargo_types where id=:id", {"id": id})
        res = c.fetchall()
        return res
        
    def getAll(self):
        c = db_connection.cursor()
        c.execute("""
        SELECT * from cargo_types
        """)
        res = c.fetchall()
        return res
        
        
class TypicalShip():
    def __init__(self, id=None, type=None):
        self.id = id
        self.type = type
        
    def save(self):
        c = db_connection.cursor()
        c.execute("insert into typical_ships (name) VALUES('" + self.type + "')")
        db_connection.commit()
        
    def delete(self, id):
        c = db_connection.cursor()
        c.execute("DELETE FROM typical_ships WHERE id = " + id + " ")
        db_connection.commit()
        
    def find(self, id):
        c = db_connection.cursor()
        c.execute("select * from typical_ships where id=:id", {"id": id})
        res = c.fetchall()
        return res
        
    def getAll(self):
        c = db_connection.cursor()
        c.execute("""
        SELECT * from typical_ships
        """)
        res = c.fetchall()
        return res
        
        
class Storage():
    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name
        
    def save(self):
        c = db_connection.cursor()
        c.execute("insert into storages (name) VALUES('" + self.name + "')")
        db_connection.commit()
        
    def delete(self, id):
        c = db_connection.cursor()
        c.execute("DELETE FROM storages WHERE id = " + id + " ")
        db_connection.commit()
        
    def find(self, id):
        c = db_connection.cursor()
        c.execute("select * from storages where id=:id", {"id": id})
        res = c.fetchall()
        return res
    
    def getByExpCargo(self, expeditor, cargo):
        c = db_connection.cursor()
        c.execute("select * from expeditor_storage_link where expeditor_id = '" + str(expeditor) + "' and cargo = '" + str(cargo) + "'")
        res = c.fetchall()
        return res
    
    def setQuery(self, query):
        c = db_connection.cursor()
        c.execute(query)
        db_connection.commit()
        
    def deleteExpeditor(self, id):
        c = db_connection.cursor()
        c.execute("DELETE FROM expeditor_storage_link WHERE id = " + id + " ")
        db_connection.commit()
        
    def getExpeditors(self, id):
        c = db_connection.cursor()
        c.execute("select * from expeditor_storage_link where storage_id=:id", {"id": id})
        res = c.fetchall()
        return res
        
    def addExpeditor(self, storage_id, expeditor_id, cargo, cargo_amount):
        c = db_connection.cursor()
        c.execute("insert into expeditor_storage_link (storage_id, expeditor_id, cargo, cargo_amount) VALUES('" + storage_id + "','" + expeditor_id + "','" + cargo + "','" + cargo_amount + "')")
        db_connection.commit()
        return c.lastrowid
    
        
    def getAll(self):
        c = db_connection.cursor()
        c.execute("""
        SELECT * from storages
        """)
        res = c.fetchall()
        return res
        

class StorageDefVal():
    def __init__(self, id=None, storage=None, cargo=None, capUF=None, capW=None):
        self.id = id
        self.storage = storage
        self.cargo = cargo
        self.capUF = capUF
        self.capW = capW
        
    def save(self):
        c = db_connection.cursor()
        if self.id != None:
            c.execute("UPDATE storage_default_values set storage = '" + self.storage + "' , cargo = '" + self.cargo + "', capUF = '" + self.capUF + "', capW = '" + self.capW + "' WHERE id = '" + self.id + "'")
            db_connection.commit()
        else:
            c.execute("insert into storage_default_values (storage,cargo,capUF,capW) VALUES('" + self.storage + "','" + self.cargo + "','" + self.capUF + "','" + self.capW + "')")
            db_connection.commit()
        return True
        
    def delete(self, id):
        c = db_connection.cursor()
        c.execute("DELETE FROM storage_default_values WHERE id = " + id + " ")
        db_connection.commit()

        
    def find(self, id):
        c = db_connection.cursor()
        c.execute("select * from storage_default_values where id=:id", {"id": id})
        res = c.fetchall()
        return res
        
    def getBy(self, col, param, value):
        c = db_connection.cursor()
        c.execute("select * from storage_default_values where " + col + " " + param + ":" + value + "", {"" + value + "": value})
        res = c.fetchall()
        return res
        
    def findBy(self, params):
        select = "SELECT * FROM storage_default_values WHERE 1 "
        where = ""
        for k,v in params.items():
            where += " AND " + k + " = " + v + " "
        select += where
        c = db_connection.cursor()
        c.execute(select)
        res = c.fetchall()
        return res
        
    def getAllClean(self):
        c = db_connection.cursor()
        c.execute("""
        SELECT * from storage_default_values
        """)
        res = c.fetchall()
        return res
        
    def getAll(self):
        c = db_connection.cursor()
        c.execute("""
        SELECT * from storage_default_values
        """)
        res = c.fetchall()
        storages = Storage()
        cargos = Cargo()
        k = 0
        for i in res:
            st = storages.find(i[1])
            cargo = cargos.find(i[2])
            i = list(i)
            i[1] = st[0][1]
            i[2] = cargo[0][1]
            i = tuple(i)
            res[k] = i
            k += 1
        return res
        
        
class StorageCap():
    def __init__(self, id=None, storage=None, coal_cap=None, pellet_cap=None, iron_cap=None):
        self.id = id
        self.storage = storage
        self.coal_cap = coal_cap
        self.pellet_cap = pellet_cap
        self.iron_cap = iron_cap
        
    def save(self):
        c = db_connection.cursor()
        c.execute("insert into storage_capacity (storage,coal_cap,pellet_cap,iron_cap) VALUES('" + self.storage + "','" + self.coal_cap + "','" + self.pellet_cap + "','" + self.iron_cap + "')")
        db_connection.commit()
        
    def delete(self, id):
        c = db_connection.cursor()
        c.execute("DELETE FROM storage_capacity WHERE id = " + id + " ")
        db_connection.commit()
        
        
    def getAllClean(self):
        c = db_connection.cursor()
        c.execute("""
        SELECT * from storage_capacity
        """)
        res = c.fetchall()
              
        return res
        
    def getAll(self):
        c = db_connection.cursor()
        c.execute("""
        SELECT * from storage_capacity
        """)
        res = c.fetchall()
        storages = Storage()
        k = 0
        for i in res:
            st = storages.find(i[1])
            
            i = list(i)
            i[1] = st[0][1]
            i = tuple(i)
            res[k] = i
            k += 1
              
        return res
        
        

class Ship():
    def __init__(self, id=None, ship_length=None, osadka=None, max_weight=None, arrival_time=None, name=None, doc=None, priority = None):
        self.id = id
        self.ship_length = ship_length
        self.osadka = osadka
        self.arrival_time = arrival_time
        self.name = name
        self.max_weight = max_weight
        self.doc = doc
        if doc == None:
            self.doc == ""
        self.priority = "0"
        if priority != None:
            self.priority = priority
        
    def save(self):
        c = db_connection.cursor()
        c.execute("insert into ships (ship_length,osadka,arrival_time,name,max_weight,doc,priority) VALUES('" + self.ship_length + "','" + self.osadka + "','" + self.arrival_time + "','" + self.name + "','" + self.max_weight + "','" + self.doc + "', '" + self.priority + "')")
        db_connection.commit()
        
    def delete(self, id):
        c = db_connection.cursor()
        c.execute("DELETE FROM ships WHERE id = " + id + " ")
        db_connection.commit()
        c.execute("DELETE FROM expeditor_ship_link WHERE ship_id = " + id + " ")
        db_connection.commit()
    
    def find(self, id):
        c = db_connection.cursor()
        c.execute("select * from ships where id=:id", {"id": id})
        res = c.fetchall()
        return res
        
    def getAllClean(self):
        c = db_connection.cursor()
        c.execute("""
        SELECT * from ships
        """)
        res = c.fetchall()
              
        return res
        
    def getExpeditors(self, id):
        c = db_connection.cursor()
        c.execute("select * from expeditor_ship_link where ship_id=:id", {"id": id})
        res = c.fetchall()
              
        return res
    
    def addExpeditor(self, ship_id, expeditor_id, cargo, cargo_amount):
        c = db_connection.cursor()
        c.execute("insert into expeditor_ship_link (ship_id, expeditor_id, cargo, cargo_amount) VALUES('" + ship_id + "','" + expeditor_id + "','" + cargo + "','" + cargo_amount + "')")
        db_connection.commit()
        
    def deleteExpeditor(self, id):
        c = db_connection.cursor()
        c.execute("delete from expeditor_ship_link where id = " + id)
        db_connection.commit()
    
    def getLast(self):
        c = db_connection.cursor()
        c.execute("""
        SELECT id, name, arrival_time,ship_length,osadka,max_weight,doc from ships order by id asc limit 1
        """)
        res = c.fetchall()
        return res
    
    def getFirstByTime(self, offset):
        c = db_connection.cursor()
        c.execute("SELECT id, name, arrival_time,ship_length,osadka,max_weight,doc,priority from ships order by arrival_time asc limit " + offset + ",1")
        res = c.fetchall()
        return res
    
    def getByQuery(self, query):
        c = db_connection.cursor()
        
        try:
            c.execute(query)
        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])
        res = c.fetchall()
        return res  
    
    def getBy(self, col, param, value):
        c = db_connection.cursor()
        c.execute("select * from ships where " + col + " " + param + " "  + value + " ")
        res = c.fetchall()
        return res
    
    def getAll(self):
        c = db_connection.cursor()
        c.execute("""
        SELECT id, name, arrival_time,ship_length,osadka,max_weight,doc,priority  from ships
        """)
        res = c.fetchall()
        # cargo = Cargo()
        # k = 0
        # for i in res:
            # c = cargo.find(i[1])
            
            # i = list(i)
            # i[1] = c[0][1]
            # i = tuple(i)
            # res[k] = i
            # k += 1
              
        return res
        
        
class Train():
    def __init__(self, id=None, cargo=None, cargo_amount=None, arrival_time=None, expeditor_id = None, carriages_amount = None, direct_way = None, num = None, railway=None, ship_id=None):
        self.id = id
        self.cargo = cargo
        self.cargo_amount = cargo_amount
        self.arrival_time = arrival_time
        self.expeditor_id = expeditor_id
        self.carriages_amount = carriages_amount
        self.direct_way = direct_way
        self.num = num
        self.railway = railway
        self.ship_id = ship_id
        if ship_id == None:
            self.ship_id = ""
        
    def save(self):
        c = db_connection.cursor()
        c.execute("insert into trains (cargo,cargo_amount,arrival_time,expeditor_id,carriages_amount,direct_way, num, railway, ship_id) VALUES('" + self.cargo + "','" + self.cargo_amount + "','" + self.arrival_time + "','" + self.expeditor_id + "','" + self.carriages_amount + "','" + self.direct_way + "','" + self.num + "','" + self.railway + "', '" + self.ship_id + "')")
        db_connection.commit()
        
    def delete(self, id):
        c = db_connection.cursor()
        c.execute("DELETE FROM trains WHERE id = " + id + " ")
        db_connection.commit()
    
    def find(self, id):
        c = db_connection.cursor()
        c.execute("select * from trains where id=:id", {"id": id})
        res = c.fetchall()
        return res
        
    def getBy(self, col, param, value):
        c = db_connection.cursor()
        c.execute("select * from trains where " + col + " " + param + " "  + value + " ")
        res = c.fetchall()
        return res  

    def getFirstByTime(self, offset):
        c = db_connection.cursor()
        c.execute("SELECT * from trains order by arrival_time asc limit " + offset + ",1")
        res = c.fetchall()
        return res        
        
    def getByQuery(self, query):
        c = db_connection.cursor()
        
        try:
            c.execute(query)
        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])
        res = c.fetchall()
        return res        
        
    def getAllClean(self):
        c = db_connection.cursor()
        c.execute("""
        SELECT * from trains
        """)
        res = c.fetchall()
              
        return res
        
    def getAll(self):
        c = db_connection.cursor()
        c.execute("""
        SELECT id, num, expeditor_id, arrival_time, cargo, carriages_amount, direct_way,railway from trains
        """)
        res = c.fetchall()
        cargo = Cargo()
        k = 0
        for i in res:
            c = cargo.find(i[4])
            
            i = list(i)
            i[4] = c[0][1]
            i = tuple(i)
            res[k] = i
            k += 1
              
        return res
                

        
class DocChar():
    def __init__(self, id=None, num=None, length=None, depth=None, is_used=None):
        self.id = id
        self.num = num
        self.length = length
        self.depth = depth
        self.is_used = is_used
        
    def save(self):
        c = db_connection.cursor()
        if self.id != None:
            c.execute("UPDATE doc_characteristics set num = '" + self.num + "' , length = '" + self.length + "', depth = '" + self.depth + "', is_used = '" + self.is_used + "' WHERE id = '" + self.id + "'")
            db_connection.commit()
        else:
            c.execute("insert into doc_characteristics (num,length,depth, is_used) VALUES('" + self.num + "','" + self.length + "','" + self.depth + "','')")
            db_connection.commit()
        return True
        
    def find(self, id):
        c = db_connection.cursor()
        c.execute("select * from doc_characteristics where id=:id", {"id": id})
        res = c.fetchall()
        return res
        
    def delete(self, id):
        c = db_connection.cursor()
        c.execute("DELETE FROM doc_characteristics WHERE id = " + id + " ")
        db_connection.commit()
        
    def update(self, id, col, val):
        c = db_connection.cursor()
        c.execute("UPDATE doc_characteristics set " + col + " = '" + val + "' WHERE id = '" + id + "'")
        db_connection.commit()
        
    def unuseDoc(self, id):
        self.update(str(id),"is_used", "" )
        
    def useDoc(self, id):
        self.update(str(id),"is_used", "1" )
    
    def getBy(self, col, param, value):
        c = db_connection.cursor()
        c.execute("select * from doc_characteristics where " + col + " " + param + ""  + value + " ")
        res = c.fetchall()
        return res  
    
    def getAll(self):
        c = db_connection.cursor()
        c.execute("""
        SELECT * from doc_characteristics
        """)
        res = c.fetchall()
        return res
        
        
class CranType():
    def __init__(self, id=None, name=None, performance_coal_1=None, performance_iron_1=None, performance_coal_2=None, performance_iron_2=None, performance_coal_3=None, performance_iron_3=None):
        self.id = id
        self.name = name
        self.performance_coal_1 = performance_coal_1
        self.performance_iron_1 = performance_iron_1
        self.performance_coal_2 = performance_coal_2
        self.performance_iron_2 = performance_iron_2
        self.performance_coal_3 = performance_coal_3
        self.performance_iron_3 = performance_iron_3
        
    def save(self):
        c = db_connection.cursor()
        if self.id != None:
            c.execute("UPDATE cran_types set name = '" + self.name + "', performance_coal_1 = '" + self.performance_coal_1 + "' , performance_iron_1 = '" + self.performance_iron_1 + "', performance_coal_2 = '" + self.performance_coal_2 + "', performance_iron_2 = '" + self.performance_iron_2 + "' , performance_coal_3 = '" + self.performance_coal_3 + "' , performance_iron_3 = '" + self.performance_iron_3 + "' WHERE id = '" + self.id + "'")
            db_connection.commit()
        else:
            c.execute("insert into cran_types (name,performance_coal_1,performance_iron_1, performance_coal_2, performance_iron_2,performance_coal_3,performance_iron_3) VALUES('" + self.name + "','" + self.performance_coal_1 + "','" + self.performance_iron_1 + "','" + self.performance_coal_2 + "','" + self.performance_iron_2 + "','" + self.performance_coal_3 + "','" + self.performance_iron_3 + "')")
            db_connection.commit()
        return True
        
    def find(self, id):
        c = db_connection.cursor()
        c.execute("select * from cran_types where id=:id", {"id": id})
        res = c.fetchall()
        return res
        
    def getBy(self, col, param, value):
        c = db_connection.cursor()
        c.execute("select * from cran_types where " + col + " " + param + " "  + value + " ")
        res = c.fetchall()
        return res
        
    def delete(self, id):
        c = db_connection.cursor()
        c.execute("DELETE FROM cran_types WHERE id = " + id + " ")
        db_connection.commit()
        
    def getAll(self):
        c = db_connection.cursor()
        c.execute("""
        SELECT * from cran_types
        """)
        res = c.fetchall()
        return res
        
        
class Cran():
    def __init__(self, id=None, num=None, cran_type=None, type=None, object_id=None):
        """type: 1 - склад 2 - причал 3 - Ж/Д"""
        self.id = id
        self.num = num
        self.cran_type = cran_type
        self.type = type
        self.object_id = object_id
        
    def save(self):
        c = db_connection.cursor()
        if self.id != None:
            c.execute("UPDATE crans set num = '" + self.num + "', cran_type = '" + self.cran_type + "' , type = '" + self.type + "', object_id = '" + self.object_id + "' WHERE id = '" + self.id + "'")
            db_connection.commit()
        else:
            c.execute("insert into crans (num,cran_type,type, object_id) VALUES('" + self.num + "','" + self.cran_type + "','" + self.type + "','" + self.object_id + "')")
            db_connection.commit()
        return True
        
    def find(self, id):
        c = db_connection.cursor()
        c.execute("select * from crans where id=:id", {"id": id})
        res = c.fetchall()
        return res
        
    def delete(self, id):
        c = db_connection.cursor()
        c.execute("DELETE FROM crans WHERE id = " + id + " ")
        db_connection.commit()
        
    def getBy(self, col, param, value):
        c = db_connection.cursor()
        c.execute("select * from crans where " + col + " " + param + " "  + value + " ")
        res = c.fetchall()
        return res
        
    def deleteByNum(self, num):
        c = db_connection.cursor()
        c.execute("DELETE FROM crans WHERE num = " + num + " ")
        db_connection.commit()
        
    def findBy(self, col, param, value):
        c = db_connection.cursor()
        c.execute("select * from crans where " + col + " " + param + ":" + value + "", {"" + value + "": value})
        res = c.fetchall()
        return res
        
    def getAllGroupBy(self):
        c = db_connection.cursor()
        c.execute("""
        select * from crans group by num
        """)
        res = c.fetchall()
        return res
        
    def getAll(self):
        c = db_connection.cursor()
        c.execute("""
        SELECT * from crans
        """)
        res = c.fetchall()
        return res
        
        
class Expeditor():
    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name
        
    def save(self):
        c = db_connection.cursor()
        if self.id != None:
            c.execute("UPDATE expeditors set name = '" + self.name + "' WHERE id = '" + self.id + "'")
            db_connection.commit()
        else:
            c.execute("insert into expeditors (name) VALUES('" + self.name + "')")
            db_connection.commit()
        return True
        
    def find(self, id):
        c = db_connection.cursor()
        c.execute("select * from expeditors where id=:id", {"id": id})
        res = c.fetchall()
        return res
        
    def delete(self, id):
        c = db_connection.cursor()
        c.execute("DELETE FROM expeditors WHERE id = " + id + " ")
        db_connection.commit()
    
    def getAll(self):
        c = db_connection.cursor()
        c.execute("""
        SELECT * from expeditors
        """)
        res = c.fetchall()
        return res
        

class Railway():
    def __init__(self, id=None, num=None, is_used=None, time_start_usage=None):
        self.id = id
        self.num = num
        self.is_used = is_used
        self.time_start_usage = time_start_usage
        
    def save(self):
        c = db_connection.cursor()
        if self.id != None:
            c.execute("UPDATE railways set num = '" + self.num + "', is_used = '" + self.is_used + "', time_start_usage = '" + self.time_start_usage + "' WHERE id = '" + self.id + "'")
            db_connection.commit()
        else:
            c.execute("insert into railways (num, is_used,time_start_usage) VALUES('" + self + "', 0,0)")
            db_connection.commit()
        return True
        
    def find(self, id):
        c = db_connection.cursor()
        c.execute("select * from railways where id=:id", {"id": id})
        res = c.fetchall()
        return res
        
        
    def getBy(self, col, param, value):
        c = db_connection.cursor()
        c.execute("select * from railways where " + col + " " + param + ":" + value + "", {"" + value + "": value})
        res = c.fetchall()
        return res    

    def getUnused(self):
        res = self.getBy('is_used', '!=', '1')
        return res    
        
    def delete(self, id):
        c = db_connection.cursor()
        c.execute("DELETE FROM railways WHERE id = " + id + " ")
        db_connection.commit()
    
    def getAll(self):
        c = db_connection.cursor()
        c.execute("""
        SELECT * from railways
        """)
        res = c.fetchall()
        return res        

        
class CranService():
    def __init__(self, id=None, cran_num=None, date_end=None, date_start=None):
        self.id = id
        self.cran_num = cran_num
        self.date_end = date_end
        self.date_start = date_start
        
    def save(self):
        c = db_connection.cursor()
        if self.id != None:
            c.execute("UPDATE cran_service set date_end = '" + self.date_end + "', date_start = '" + self.date_start + "'  WHERE id = '" + self.id + "'")
            db_connection.commit()
        else:
            c.execute("insert into cran_service (cran_num, date_end, date_start) VALUES('" + self.cran_num + "', '" + self.date_end + "', '" + self.date_start + "')")
            db_connection.commit()
        return True
        
    def find(self, cran_num):
        c = db_connection.cursor()
        c.execute("select * from cran_service where cran_num=:id", {"id": cran_num})
        res = c.fetchall()
        return res
        
    def delete(self, cran_num):
        c = db_connection.cursor()
        c.execute("DELETE FROM cran_service WHERE cran_num = " + cran_num + " ")
        db_connection.commit()
    
    def getAll(self):
        c = db_connection.cursor()
        c.execute("""
        SELECT * from cran_service
        """)
        res = c.fetchall()
        return res
        
        

        
class Main():
    def __init__(self, workers = None, tech = None, METEO = None):
        self.meteo = METEO
        self.workers_resource = workers
        self.tech_resource = tech
        self.calculated_ships = []
        self.calculated_trains = []
        
        # Список добавленных id в таблицу expeditor_storage_link 
        self.exp_stor_link_meta = []
        
        
        # self.time_lines - Основной массив с информацией об операциях [[время начала, время окончания, тип объекта, id объекта, путь/причал, второй тип объекта, id объекта, путь/причал, количество груза, [массив кранов], количество людей, количество техники], ...]
        # путь/причал = None, если объект - склад
        # типы объектов - 1 состав, 2 - судно, 3 - склад
        self.time_lines = []
        
    
    def getNextObject(self):
        ship_instance = Ship()
        ship = ship_instance.getFirstByTime(str(len(self.calculated_ships)))
        train_inst = Train()
        train = train_inst.getFirstByTime(str(len(self.calculated_trains)))
        
        
        if ship != [] and train != []:
            if int(ship[0][2]) < int(train[0][3]):
                self.calculateShip(ship[0][0])
            else:
                self.calculateTrain(train)
        else:
            if ship != []:
                self.calculateShip(ship[0][0])
            if train != []:
                self.calculateTrain(train)
        
        if ship == [] and train == []:
            return False
                
    def sortStoragesByCongestion(self, storages):
        if storages != []:
            new_storages = []
            congestions = []
            
            for row in storages:
                congestion = self.getStorageCongestion(row[2])
                congestions.append(congestion)
            
            
            
            while storages != []:
                idx = congestions.index(max(congestions))
                new_storages.append(storages[idx])
                storages.remove(storages[idx])
                congestions.remove(max(congestions))
                
                
            return new_storages
        else:
            return False
    
    def setTrainRailway(self, arrival_time = None, ship_id = None, cargo = None, expeditor = None):
        t = Train()
        trains = t.getByQuery("SELECT * FROM trains WHERE (railway != '' AND railway != 0)")
        if ship_id == "" or ship_id == "None" or ship_id == "0" or ship_id == "Null":
            ship_id = None
            
        used_rws = []
        tr_ids = []
        all_rws = [2,3,1,4]
        waiting_time = 7200
        if trains != []:
            for tr in trains:
                tr_ids.append(tr[0])
                used_rws.append(tr[8])
            
        if self.time_lines != []:
            for arr in self.time_lines:
                if arr[2] == 1:
                    if arrival_time > arr[0] and arrival_time < arr[1]:
                        if arr[4] not in used_rws:
                            used_rws.append(arr[4])
                            continue
                            
                            
                    if arrival_time > (arr[1] + waiting_time):
                        if arr[3] in tr_ids:
                            if arr[4] in used_rws:
                                used_rws.remove(arr[4])
        
        if used_rws != []:
            for rway in used_rws:
                if rway in all_rws:
                    all_rws.remove(rway)
        
        
        ship_instance = Ship()
        tmp_free_rw = 0
        
        if ship_id != None:
            if isinstance(ship_id, list):
                ship = ship_id
                if (int(arrival_time) + 86400) > int(ship[0][5]):
                    if ship[0][8] == 2 or ship[0][8] == 3:
                        tmp_free_rw = 4
                        
                        
                    if ship[0][8] == 5 or ship[0][8] == 6:
                        tmp_free_rw = 1
                    
                if tmp_free_rw in all_rws:
                    return tmp_free_rw

            else:
                ship = ship_instance.find(ship_id)
                if (int(arrival_time) + 86400) > int(ship[0][5]):
                    if ship[0][8] == 2 or ship[0][8] == 3:
                        tmp_free_rw = 4
                        
                        
                    if ship[0][8] == 5 or ship[0][8] == 6:
                        tmp_free_rw = 1
                    
                if tmp_free_rw in all_rws:
                    return tmp_free_rw
        
        docs_ids = '2,3,5,6'
        ships = ship_instance.getBy('doc', 'in', ' (' + docs_ids + ') order by arrival_time asc')
        if ships != []:
            for ship in ships:
                if tmp_free_rw != 0:
                    break
                exps = ship_instance.getExpeditors(ship[0])
                if exps != []:
                    for exp in exps:
                        if (int(arrival_time) + 86400) > int(ship[5]) and int(exp[3]) == int(cargo) and int(exp[2]) == int(expeditor):
                            if ship[8] == 2 or ship[8] == 3:
                                tmp_free_rw = 4
                                
                            if ship[8] == 5 or ship[8] == 6:
                                tmp_free_rw = 1
                                
                            break
                            
            if tmp_free_rw in all_rws:
                return tmp_free_rw
                
        if ship_id == None:
            tmp_free_rw = all_rws[0]
            
        return tmp_free_rw
    
    def calculateTrain(self, train, from_ship_func = None):
        # кортеж состава (id, тип груза, количество груза, дата прибытия, количество вагонов, id экспедитора, прямой путь, номер поезда, номер пути, дата отправления, id судна)
        train_inst = Train()
        storage_instance = Storage()
        cran = Cran()
        
        ship_instance = Ship()
        already_loaded = 0
        total_time = 0
        # время начала операции
        time_start = train[0][3]
        prior_storages = []
        oper_time_start = 0
        loaded = 0
        
        if train[0][8] == "" or train[0][8] == "0" or train[0][8] == "None" or train[0][8] == None:
            train[0] = list(train[0])
            train[0][8] = self.setTrainRailway(train[0][3], train[0][10], train[0][1], train[0][5])
            train[0] = tuple(train[0])
        
        if train[0][8] < 1:
            self.getNextObject()
            return False
            
        if train[0][8] == 1:
            prior_storages = [9,11]
        if train[0][8] == 2:
            prior_storages = [8,10,7,12]
        if train[0][8] == 3:
            prior_storages = [3,2]
        if train[0][8] == 4:
            prior_storages = [2,1]
        

        
        if str(train[0][10]) != '' and str(train[0][10]).lower() != 'null' and str(train[0][10]) != '0' and str(train[0][10]) != None and str(train[0][10]) != 'None':
            self.calculateShip(train[0][10], 1)
            return False
         
        # docs_ids = '2,3,5,6'
        if from_ship_func == None:
            # ships = ship_instance.getBy('doc', '!=', ' (' + docs_ids + ') order by arrival_time asc')
            ships = ship_instance.getBy('id', '>', ' 0 order by arrival_time asc')
            if ships != []:
                for ship in ships:
                    exps = ship_instance.getExpeditors(ship[0])
                    if exps != []:
                        for exp in exps:
                            if (int(train[0][3]) + 86400) > int(ship[5]) and int(train[0][3]) < int(ship[5]) and int(exp[3]) == int(train[0][1]) and int(exp[2]) == int(train[0][5]):
                                self.calculateShip(ship[0])
                                return False
                            
        
            if self.time_lines != []:
                for row in self.time_lines:
                    if row[1] == 0 and row[2] == 2:
                        ship_exps = []
                        tmp_s_exps = ship_instance.getExpeditors(row[3])
                        for r_s in tmp_s_exps:
                            for tl in self.time_lines:
                                if tl[5] == 2 and tl[6] == row[3]:
                                    if r_s[3] == tl[8]:
                                        if r_s[4] != tl[9]:
                                            val = r_s[4] - tl[9]
                                            ship_exps.append((r_s[0],r_s[1],r_s[2],r_s[3],val))
                        
                        
                        if ship_exps != []:
                            for s_ex in ship_exps:
                                if s_ex[2] == train[0][5] and s_ex[3] == train[0][1]:
                                    self.calculateShip(row, None, train[0][0])
                                    return False

        
        storage_exps = storage_instance.getByExpCargo(train[0][5], train[0][1])
        if storage_exps != []:
            congestions = []
            # Сортируем по заполненности складов 
            sorted = self.sortStoragesByCongestion(storage_exps)
            # tmp_stor = []
            # for st_id in prior_storages:
                # for s_t in sorted:
                    # if s_t[0] == st_id:
                        # tmp_stor.append(s_t)
                        # sorted.remove(s_t)
                        
            # sorted = tmp_stor + sorted
            for storage in sorted:
                storage_id = int(storage[2])
                if self.getStorageCongestion(storage_id) > 98:
                    continue
                    
                # Если есть приоритетные склады с этим же грузом этого же экспедитора
                if storage_id in prior_storages:
                    if already_loaded != train[0][2]:
                        stor_left = self.getStorageCongestionLeft(storage[3], storage_id)
                        oper_time_start = train[0][3]
                        if time_start != train[0][3]:
                            oper_time_start = time_start
                        
                        check_array = self.checkTime(oper_time_start)
                        
                        if check_array[0] < 1 or check_array[1] < 1:
                            continue
                            
                            
                        additional_ids = ""
                        if check_array[2] != []:
                            additional_ids = " and num NOT IN ("
                            for cr in check_array[2]:
                                additional_ids += "'" + str(cr) + "', "
                                
                            additional_ids = additional_ids[:-2] + ")"
                        stor_crans = cran.getBy('object_id', '=', str(storage_id) + " and type=1" + additional_ids)
                        
                        if stor_crans == []:
                            continue
                        
                        # Pnorm кранов
                        Pnorm = 0
                        workers_per_cran = 1
                        if int(train[0][1]) == 26:
                            workers_per_cran = 2
                        tech_per_cran = 1
                        
                        if len(stor_crans) > 3:
                            stor_crans = stor_crans[0:3]
                        
                        workers = workers_per_cran * len(stor_crans)
                        tech = tech_per_cran * len(stor_crans)
                        tmp_cr_list = []
                        used_crans = []
                        for cr1 in stor_crans:
                            used_crans.append(cr1[1])
                            c_t = CranType()
                            c = c_t.find(cr1[2])
                            if int(train[0][1]) == 1:
                                tmp_cr_list.append(int(c[0][6]))
                            else:
                                tmp_cr_list.append(int(c[0][7]))
                        
                        Pnorm = sum(tmp_cr_list)
                        
                        if check_array[0] < workers or check_array[1] < tech:
                            tmp_pnorm = Pnorm
                            Pnorm = min((check_array[0] / workers), (check_array[1] / tech)) * tmp_pnorm
                            workers = check_array[0]
                            tech = check_array[1]
                            
                        
                        loaded = 0
                        if stor_left >= (int(train[0][2]) - int(already_loaded)):
                            loaded = (int(train[0][2]) - int(already_loaded))
                            already_loaded = already_loaded + (int(train[0][2]) - int(already_loaded))
                        else:
                            loaded = int(stor_left)
                            already_loaded = already_loaded + int(stor_left)
                        
                        time = loaded / Pnorm * 43200
                        if self.meteo != []:
                            for meteo in self.meteo:
                                k = 1
                                # if meteo.precipitation == 1:
                                    # if train[0][1] == 26:
                                        # k = 0
                                
                                if meteo.windV > 10.7 and meteo.windV <= 13.8:
                                    k = 0.95
                                
                                if meteo.windV > 13.8 and meteo.windV <= 15:
                                    k = 0.9
                                
                                if meteo.windV > 15 and meteo.windV <= 20:
                                    k = 0.8
                                    
                                if meteo.windV > 20:
                                    k = 0
                                    
                                if int(meteo.windStart) > oper_time_start and int(meteo.windEnd) < (oper_time_start + time):
                                    
                                    dt = meteo.windEnd - meteo.windStart
                                    if k != 0:
                                        new_time = time - dt + dt / k
                                    else:
                                        new_time = time + dt
                                
                                if int(meteo.windStart) > oper_time_start and int(meteo.windEnd) >= (oper_time_start + time):
                                    
                                    dt = (oper_time_start + time) - meteo.windStart
                                    if k != 0:
                                        new_time = time - dt + dt / k
                                    else:
                                        new_time = time + dt
                                
                                if int(meteo.windStart) <= oper_time_start and int(meteo.windEnd) < (oper_time_start + time):
                                    
                                    dt = meteo.windEnd - oper_time_start
                                    if k != 0:
                                        new_time = time - dt + dt / k
                                    else:
                                        new_time = time + dt
                                
                                if int(meteo.windStart) < oper_time_start and int(meteo.windEnd) > (oper_time_start + time):
                                    new_time = time / k
                                    time = new_time
                                
                        
                        
                        total_time += time
                        time_start = oper_time_start + time
                        amount = str(int(storage[4]) + int(loaded))
                        storage_instance.setQuery("update expeditor_storage_link set cargo_amount = '" + amount + "' WHERE id = " + str(storage[0]))
                        self.time_lines.append([oper_time_start, time_start, 1, train[0][0], train[0][8], 3, storage_id, None, train[0][1], loaded, used_crans, workers, tech])
                            
                else:
                    if already_loaded != train[0][2]:
                        # Только уголь может быть таким подвозом
                        if int(storage[3]) == 1:
                            stor_left = self.getStorageCongestionLeft(storage[3], storage_id)
                            oper_time_start = train[0][3]
                            if time_start != train[0][3]:
                                oper_time_start = time_start
                            
                            check_array = self.checkTime(oper_time_start)
                            additional_ids = ""
                            if check_array[2] != []:
                                additional_ids = " and num NOT IN ("
                                for cr in check_array[2]:
                                    additional_ids += "'" + str(cr) + "', "
                                    
                                additional_ids = additional_ids[:-2] + ")"
                            stor_crans = cran.getBy('object_id', '=', str(storage_id) + " and type=1 " + additional_ids)
                            rw_crans = cran.getBy('object_id', '=', str(train[0][8]) + " and type=3 " + additional_ids)
                            
                            if stor_crans == [] or rw_crans == []:
                                continue
                            
                            # if check_array[0] < 2 or check_array[1] < 2:
                                # continue
                            
                            
                            
                            if min(len(rw_crans), len(stor_crans)) < 3:
                                crans1 = stor_crans[0:min(len(rw_crans), len(stor_crans))]
                                crans2 = rw_crans[0:min(len(rw_crans), len(stor_crans))]
                            else:
                                crans1 = stor_crans[0:3]
                                crans2 = rw_crans[0:3]
                                
                            
                            # рассчет производительности
                            used_crans = []
                            tmp_cr_list = []
                            tmp_cr_list2 = []
                            # Краны склада. Берем производительность крана с подвозом. Т.к. подвозить можно только уголь - берем в формулу только
                            # performance_coal_2   в списке [0][4]
                            for cr1 in crans1:
                                c_t = CranType()
                                c = c_t.find(cr1[2])
                                used_crans.append(cr1[1])
                                tmp_cr_list.append(int(c[0][4]))
                                
                            # Краны жд пути. Берем производительность при работе с ЖД составом. Т.к. подвозить можно только уголь - берем в формулу
                            # только performance_coal_3   в списке [0][6]    
                            for cr2 in crans2:
                                c_t = CranType()
                                c = c_t.find(cr2[2])
                                used_crans.append(cr2[1])
                                tmp_cr_list2.append(int(c[0][6]))
                            
                            Pnorm = min(sum(tmp_cr_list), sum(tmp_cr_list2))
                            
                            workers = (3 * len(crans1)) 
                            tech = (3 * len(crans1)) 
                            if check_array[0] < (3 * len(crans1)) or check_array[1] < (3 * len(crans1)):
                                workers = check_array[0]
                                tech = check_array[1]
                                tmp_pnorm = Pnorm
                                Pnorm = min((workers / (3 * len(crans1))), (tech / (3 * len(crans1)))) * tmp_pnorm
                                
                            # нужно 3 человека, 3 техники и 2 крана
                            
                            loaded = 0
                            if stor_left >= (int(train[0][2]) - int(already_loaded)):
                                loaded = (int(train[0][2]) - int(already_loaded))
                                already_loaded = already_loaded + (int(train[0][2]) - int(already_loaded))
                            else:
                                loaded = int(stor_left)
                                already_loaded = already_loaded + int(stor_left)
                            
                            time = loaded / Pnorm * 43200
                            if self.meteo != []:
                                for meteo in self.meteo:
                                    k = 1
                                    # if meteo.precipitation == 1:
                                        # if train[0][1] == 26:
                                            # k = 0
                                    
                                    if meteo.windV > 10.7 and meteo.windV <= 13.8:
                                        k = 0.95
                                    
                                    if meteo.windV > 13.8 and meteo.windV <= 15:
                                        k = 0.9
                                    
                                    if meteo.windV > 15 and meteo.windV <= 20:
                                        k = 0.8
                                        
                                    if meteo.windV > 20:
                                        k = 0
                                        
                                    if int(meteo.windStart) > oper_time_start and int(meteo.windEnd) < (oper_time_start + time):
                                        
                                        dt = meteo.windEnd - meteo.windStart
                                        if k != 0:
                                            new_time = time - dt + dt / k
                                        else:
                                            new_time = time + dt
                                    
                                    if int(meteo.windStart) > oper_time_start and int(meteo.windEnd) >= (oper_time_start + time):
                                        
                                        dt = (oper_time_start + time) - meteo.windStart
                                        if k != 0:
                                            new_time = time - dt + dt / k
                                        else:
                                            new_time = time + dt
                                    
                                    if int(meteo.windStart) <= oper_time_start and int(meteo.windEnd) < (oper_time_start + time):
                                        
                                        dt = meteo.windEnd - oper_time_start
                                        if k != 0:
                                            new_time = time - dt + dt / k
                                        else:
                                            new_time = time + dt
                                    
                                    if int(meteo.windStart) < oper_time_start and int(meteo.windEnd) > (oper_time_start + time):
                                        new_time = time / k
                                        time = new_time
                                    
                        
                            
                            total_time += time
                            time_start = oper_time_start + time
                            amount = str(int(storage[4]) + int(loaded))
                            storage_instance.setQuery("update expeditor_storage_link set cargo_amount = '" + amount + "' WHERE id = " + str(storage[0]))
                            self.time_lines.append([oper_time_start, time_start, 1, train[0][0], train[0][8], 3, storage_id, None, train[0][1], loaded, used_crans, workers, tech])
                        else:
                            continue
        
        if already_loaded != train[0][2]:
            storages = storage_instance.getAll()
            # st_arr = []
            # for sto in storages:
                # storage_exps = storage_instance.getExpeditors(sto[0])
                # st_arr.append(storage_exps)
            # sorted = self.sortStoragesByCongestion(storages)
            
            sorted = []
            for st_id in prior_storages:
                for s_t in storages:
                    if s_t[0] == st_id:
                        sorted.append(s_t)
                        storages.remove(s_t)
                        
            sorted = sorted + storages
            
            for storage in sorted:
                storage_id = int(storage[0])
                if self.getStorageCongestion(storage_id) > 98:
                    continue
                
                
                # Если есть приоритетные склады с этим же грузом этого же экспедитора
                if storage_id in prior_storages:
                    if already_loaded != train[0][2]:
                        stor_left = self.getStorageCongestionLeft(train[0][1], storage_id)
                        oper_time_start = train[0][3]
                        if time_start != train[0][3]:
                            oper_time_start = time_start
                        
                        check_array = self.checkTime(oper_time_start)
                        
                        if check_array[0] < 1 or check_array[1] < 1:
                            continue
                            
                            
                        additional_ids = ""
                        if check_array[2] != []:
                            additional_ids = " and num NOT IN ("
                            for cr in check_array[2]:
                                additional_ids += "'" + str(cr) + "', "
                                
                            additional_ids = additional_ids[:-2] + ")"
                        stor_crans = cran.getBy('object_id', '=', str(storage_id) + " and type=1" + additional_ids)
                        
                        if stor_crans == []:
                            continue
                        
                        # Pnorm кранов
                        Pnorm = 0
                        workers_per_cran = 1
                        if int(train[0][1]) == 26:
                            workers_per_cran = 2
                        tech_per_cran = 1
                        
                        if len(stor_crans) > 3:
                            stor_crans = stor_crans[0:3]
                          
                        workers = workers_per_cran * len(stor_crans)
                        tech = tech_per_cran * len(stor_crans)
                        tmp_cr_list = []
                        used_crans = []
                        for cr1 in stor_crans:
                            used_crans.append(cr1[1])
                            c_t = CranType()
                            c = c_t.find(cr1[2])
                            if int(train[0][1]) == 1:
                                tmp_cr_list.append(int(c[0][6]))
                            else:
                                tmp_cr_list.append(int(c[0][7]))
                        
                        Pnorm = sum(tmp_cr_list)
                        if check_array[0] < workers or check_array[1] < tech:
                            tmp_pnorm = Pnorm
                            Pnorm = min((check_array[0] / workers), (check_array[1] / tech)) * tmp_pnorm
                            workers = check_array[0]
                            tech = check_array[1]
                        
                           
                        # нужно 3 человека, 3 техники и 2 крана
                        loaded = 0
                        if stor_left >= (int(train[0][2]) - int(already_loaded)):
                            loaded = (int(train[0][2]) - int(already_loaded))
                            already_loaded = already_loaded + (int(train[0][2]) - int(already_loaded))
                        else:
                            loaded = int(stor_left)
                            already_loaded = already_loaded + int(stor_left)
                        
                        time = loaded / Pnorm * 43200
                        
                        if self.meteo != []:
                            for meteo in self.meteo:
                                k = 1
                                # if meteo.precipitation == 1:
                                    # if train[0][1] == 26:
                                        # k = 0
                                
                                if meteo.windV > 10.7 and meteo.windV <= 13.8:
                                    k = 0.95
                                
                                if meteo.windV > 13.8 and meteo.windV <= 15:
                                    k = 0.9
                                
                                if meteo.windV > 15 and meteo.windV <= 20:
                                    k = 0.8
                                    
                                if meteo.windV > 20:
                                    k = 0
                                    
                                if int(meteo.windStart) > oper_time_start and int(meteo.windEnd) < (oper_time_start + time):
                                    
                                    dt = meteo.windEnd - meteo.windStart
                                    if k != 0:
                                        new_time = time - dt + dt / k
                                    else:
                                        new_time = time + dt
                                
                                if int(meteo.windStart) > oper_time_start and int(meteo.windEnd) >= (oper_time_start + time):
                                    
                                    dt = (oper_time_start + time) - meteo.windStart
                                    if k != 0:
                                        new_time = time - dt + dt / k
                                    else:
                                        new_time = time + dt
                                
                                if int(meteo.windStart) <= oper_time_start and int(meteo.windEnd) < (oper_time_start + time):
                                    
                                    dt = meteo.windEnd - oper_time_start
                                    if k != 0:
                                        new_time = time - dt + dt / k
                                    else:
                                        new_time = time + dt
                                
                                if int(meteo.windStart) < oper_time_start and int(meteo.windEnd) > (oper_time_start + time):
                                    new_time = time / k
                                    time = new_time
                                
                                
                                # print(time, meteo.precipitation,meteo.windV,meteo.windStart,meteo.windEnd)
                        # return False
                        
                        total_time += time
                        time_start = oper_time_start + time
                        new_exp = storage_instance.addExpeditor(str(storage_id), str(train[0][5]),str(train[0][1]),str(loaded))
                        self.time_lines.append([oper_time_start, time_start, 1, train[0][0], train[0][8], 3, storage_id, None, train[0][1], loaded, used_crans, workers, tech])
                else:
                    if already_loaded != train[0][2]:
                        # Только уголь может быть таким подвозом
                        if int(train[0][1]) == 1:
                            stor_left = self.getStorageCongestionLeft(train[0][1], storage_id)
                            oper_time_start = train[0][3]
                            if time_start != train[0][3]:
                                oper_time_start = time_start
                            
                            check_array = self.checkTime(oper_time_start)
                            additional_ids = ""
                            if check_array[2] != []:
                                additional_ids = " and num NOT IN ("
                                for cr in check_array[2]:
                                    additional_ids += "'" + str(cr) + "', "
                                    
                                additional_ids = additional_ids[:-2] + ")"
                            stor_crans = cran.getBy('object_id', '=', str(storage_id) + " and type=1" + additional_ids)
                            rw_crans = cran.getBy('object_id', '=', str(train[0][8]) + " and type=3" + additional_ids)
                            
                            if stor_crans == [] or rw_crans == []:
                                continue
                            
                            # if check_array[0] < 2 or check_array[1] < 2:
                                # continue
                            
                            
                            
                            if min(len(rw_crans), len(stor_crans)) < 3:
                                crans1 = stor_crans[0:min(len(rw_crans), len(stor_crans))]
                                crans2 = rw_crans[0:min(len(rw_crans), len(stor_crans))]
                            else:
                                crans1 = stor_crans[0:3]
                                crans2 = rw_crans[0:3]
                                
                            
                            # рассчет производительности
                            used_crans = []
                            tmp_cr_list = []
                            tmp_cr_list2 = []
                            # Краны склада. Берем производительность крана с подвозом. Т.к. подвозить можно только уголь - берем в формулу только
                            # performance_coal_2   в списке [0][4]
                            for cr1 in crans1:
                                c_t = CranType()
                                c = c_t.find(cr1[2])
                                used_crans.append(cr1[1])
                                tmp_cr_list.append(int(c[0][4]))
                                
                            # Краны жд пути. Берем производительность при работе с ЖД составом. Т.к. подвозить можно только уголь - берем в формулу
                            # только performance_coal_3   в списке [0][6]    
                            for cr2 in crans2:
                                c_t = CranType()
                                c = c_t.find(cr2[2])
                                used_crans.append(cr2[1])
                                tmp_cr_list2.append(int(c[0][6]))
                            
                            Pnorm = min(sum(tmp_cr_list), sum(tmp_cr_list2))
                            
                            workers = (3 * len(crans1)) 
                            tech = (3 * len(crans1)) 
                            if check_array[0] < (3 * len(crans1)) or check_array[1] < (3 * len(crans1)):
                                workers = check_array[0]
                                tech = check_array[1]
                                tmp_pnorm = Pnorm
                                Pnorm = min((workers / (3 * len(crans1))), (tech / (3 * len(crans1)))) * tmp_pnorm
                                
                            # нужно 3 человека, 3 техники и 2 крана
                            
                            loaded = 0
                            if stor_left >= (int(train[0][2]) - int(already_loaded)):
                                loaded = (int(train[0][2]) - int(already_loaded))
                                already_loaded = already_loaded + (int(train[0][2]) - int(already_loaded))
                            else:
                                loaded = int(stor_left)
                                already_loaded = already_loaded + int(stor_left)
                            
                            time = loaded / Pnorm * 43200
                            
                            if self.meteo != []:
                                for meteo in self.meteo:
                                    k = 1
                                    # if meteo.precipitation == 1:
                                        # if train[0][1] == 26:
                                            # k = 0
                                    
                                    if meteo.windV > 10.7 and meteo.windV <= 13.8:
                                        k = 0.95
                                    
                                    if meteo.windV > 13.8 and meteo.windV <= 15:
                                        k = 0.9
                                    
                                    if meteo.windV > 15 and meteo.windV <= 20:
                                        k = 0.8
                                        
                                    if meteo.windV > 20:
                                        k = 0
                                        
                                    if int(meteo.windStart) > oper_time_start and int(meteo.windEnd) < (oper_time_start + time):
                                        
                                        dt = meteo.windEnd - meteo.windStart
                                        if k != 0:
                                            new_time = time - dt + dt / k
                                        else:
                                            new_time = time + dt
                                    
                                    if int(meteo.windStart) > oper_time_start and int(meteo.windEnd) >= (oper_time_start + time):
                                        
                                        dt = (oper_time_start + time) - meteo.windStart
                                        if k != 0:
                                            new_time = time - dt + dt / k
                                        else:
                                            new_time = time + dt
                                    
                                    if int(meteo.windStart) <= oper_time_start and int(meteo.windEnd) < (oper_time_start + time):
                                        
                                        dt = meteo.windEnd - oper_time_start
                                        if k != 0:
                                            new_time = time - dt + dt / k
                                        else:
                                            new_time = time + dt
                                    
                                    if int(meteo.windStart) < oper_time_start and int(meteo.windEnd) > (oper_time_start + time):
                                        new_time = time / k
                                        time = new_time
                            
                            total_time += time
                            time_start = oper_time_start + time
                            new_exp = storage_instance.addExpeditor(str(storage_id), str(train[0][5]),str(train[0][1]),str(loaded))
                            self.time_lines.append([oper_time_start, time_start, 1, train[0][0], train[0][8], 3, storage_id, None, train[0][1], loaded, used_crans, workers, tech])
                        else:
                            continue
                            
        # s = Storage()
        # for id in self.exp_stor_link_meta:
            # s.deleteExpeditor(str(id))
        
        
            
        
        if already_loaded != train[0][2]:
            if oper_time_start == 0:
                oper_time_start = train[0][3]
            self.time_lines.append([oper_time_start, 0, 1, train[0][0], train[0][8], 0, 0, None, train[0][1], 0, [], 0, 0])
        else:
            self.calculated_trains.append(train[0][0])
        
        if self.time_lines != []:
            for row in self.time_lines:
                if row[1] == 0 and row[5] == 0 and row[6] == 0:
                    if row[2] == 1:
                        print(row)
                        return False
                        tmp_total_loaded = 0
                        for r in self.time_lines:
                            if row[1] == 1 and row[2] == r[2]:
                                tmp_total_loaded += r[9]
                        t = train_inst.find(row[3])
                        t[0] = list(t[0])
                        t[0][8] = row[8]
                        t[0][2] = int(t[0][2]) - tmp_total_loaded
                        t[0] = tuple(t[0])
                        self.calculateTrain(t)
                        return False
                    
                # if row[1] == 0 and row[2] == 2:
                    # print(train,row)
                    # self.calculateShip(row)
                    # return False
            
        if from_ship_func == None:
            self.getNextObject()
                    
    def checkTime(self, time = None):
        workers = 0
        tech = 0
        used_crans = []
        for arr in self.time_lines:
            if time > arr[0] and time < arr[1]:
                workers += arr[11]
                tech += arr[12]
                if arr[10] != []:
                    for cr in arr[10]:
                        used_crans.append(cr)
        
        return [(self.workers_resource - workers), (self.tech_resource - tech), used_crans]
    
    
    def setShipDoc(self, arrival_time = None, ship = None):
        tmp_free_doc = 0
        s = Ship()
        ships = s.getByQuery("SELECT * FROM ships WHERE (doc != '' AND doc != 0)")
        used_dcs = []
        sh_ids = []
        all_docs = [2,3,4,5,6]
        if ships != []:
            for sh in ships:
                sh_ids.append(sh[0])
                used_dcs.append(sh[8])
        
        
        if self.time_lines != []:
            for arr in self.time_lines:
                if arr[2] == 2:
                    if arrival_time > arr[0] and arrival_time < arr[1]:
                        if arr[4] not in used_dcs:
                            used_dcs.append(arr[4])
                            continue
                            
                            
                    if arrival_time > arr[1] :
                        if arr[3] in sh_ids:
                            if arr[4] in used_dcs:
                                used_dcs.remove(arr[4])
                                
                if arr[5] == 2:
                    if arrival_time > arr[0] and arrival_time < arr[1]:
                        if arr[7] not in used_dcs:
                            used_dcs.append(arr[7])
                            continue
                            
                            
                    if arrival_time > arr[1] :
                        if arr[6] in sh_ids:
                            if arr[7] in used_dcs:
                                used_dcs.remove(arr[7])
                
        if used_dcs != []:
            for doc__ in used_dcs:
                if doc__ in all_docs:
                    all_docs.remove(doc__)
        
        
        if all_docs != []:
            for doc in all_docs:
                d = DocChar()
                doc_char = d.getBy('num', '=', str(doc))
                
                if doc_char[0][2] > ship[0][3] and doc_char[0][3] > ship[0][4]:
                    tmp_free_doc = doc
                    break
                    
        
        
        return tmp_free_doc
    

    def calculateShip(self, ship_id, from_train_func = None, train_id = None):
        global train
        train_inst = Train()
        ship_instance = Ship()
        storage_instance = Storage()
        cran = Cran()
        already_loaded = 0
        total_load = 0
        total_time = 0
        oper_time_start = 0
        short_stor = 0
        direct_stor = 0
        ship = []
        if ship_id != None:
            if isinstance(ship_id, list):
                ship = ship_instance.find(ship_id[3])
                ship[0] = list(ship[0])
                ship[0][5] = int(ship_id[0]) + 50
                if train_id != None:
                    tmp_tr = train_inst.find(train_id)
                    ship[0][5] = int(tmp_tr[0][3]) + 50
                ship[0][8] = int(ship_id[4])
                ship[0] = tuple(ship[0])
            else:
                ship = ship_instance.find(ship_id)
        
        
        time_start = int(ship[0][5])
        ship_exps = []
        if ship_id != None:
            if isinstance(ship_id, list):
                tmp_s_exps = ship_instance.getExpeditors(ship_id[3])
                for r_s in tmp_s_exps:
                    for tl in self.time_lines:
                        if tl[5] == 2 and tl[6] == ship[0][0]:
                            if r_s[3] == tl[8]:
                                if r_s[4] != tl[9]:
                                    val = r_s[4] - tl[9]
                                    ship_exps.append((r_s[0],r_s[1],r_s[2],r_s[3],val))
                                    
                                
            else:
                ship_exps = ship_instance.getExpeditors(ship_id)
        
        if ship_exps != []:
            for tmp_rw in ship_exps:
                total_load += tmp_rw[4]
        
        if str(ship[0][8]).lower() == 'null' or str(ship[0][8]).lower() == 'none' or ship[0][8] == '' or ship[0][8] == '0' or ship[0][8] == None:
            ship[0] = list(ship[0])
            ship[0][8] = self.setShipDoc(time_start, ship)
            ship[0] = tuple(ship[0])
        
        if ship[0][8] == 2:
            short_stor = 1
        if ship[0][8] == 4:
            short_stor = 8
        if ship[0][8] == 5:
            short_stor = 8
            direct_stor = 9
        if ship[0][8] == 6:
            short_stor = 10
            direct_stor = 11     
        
        
        trains = []
        train_expeditor = []
        docs_for_direct_way = [2,3,5,6]
        
        if ship[0][8] != None:
            trains = []
            trains = train_inst.getByQuery("SELECT * FROM trains WHERE ship_id = " + str(ship[0][0]))
            if trains == []:
                trains_all = train_inst.getAllClean()
                if trains_all != []:
                    for tr in trains_all:
                        if tr[0] in self.calculated_trains:
                            continue
                            
                        for sh_ex in ship_exps:
                            if int(ship[0][5]) < (int(tr[3]) + 86400) and int(ship[0][5]) > int(tr[3]) and sh_ex[2] == tr[5] and sh_ex[3] == tr[1]:
                                
                                
                                train_expeditor.append(sh_ex)
                                train = [tr]
                                trains.append(tr)
            
            
            if trains != []:
                iter = -1
                
                for train in trains:
                    iter += 1
                    tmp = []
                    tmp = train
                    train = []
                    train.append(tmp)
                    
                    tr = train[0]
                    if tr[8] == "" or tr[8] == "0" or tr[8] == "None" or str(tr[8]).lower() == "null" or tr[8] == None:
                        train[0] = list(train[0])
                        train[0][8] = self.setTrainRailway(train[0][3], ship)
                        train[0] = tuple(train[0])
                    
                    # Отдельная операция погрузки с состава
                    oper_time_start = int(ship[0][5])
                    if time_start != int(ship[0][5]):
                        oper_time_start = time_start
                    
                    check_array = self.checkTime(oper_time_start)
                    
                    if check_array[0] > 0 and check_array[1] > 0:
                        
                            
                        additional_ids = ""
                        if check_array[2] != []:
                            additional_ids = " and num NOT IN ("
                            for cr in check_array[2]:
                                additional_ids += "'" + str(cr) + "', "
                                
                            additional_ids = additional_ids[:-2] + ")"
                        stor_crans = cran.getBy('object_id', '=', str(ship[0][8]) + " and type=2" + additional_ids)
                        if stor_crans != []:
                            
                        
                            # Pnorm кранов
                            Pnorm = 0
                            workers_per_cran = 2
                            tech_per_cran = 1
                            
                            if len(stor_crans) > 3:
                                stor_crans = stor_crans[0:3]
                              
                            workers = workers_per_cran * len(stor_crans)
                            tech = tech_per_cran * len(stor_crans)
                            tmp_cr_list = []
                            used_crans = []
                            for cr1 in stor_crans:
                                used_crans.append(cr1[1])
                                c_t = CranType()
                                c = c_t.find(cr1[2])
                                if int(train[0][1]) == 1:
                                    tmp_cr_list.append(int(c[0][6]))
                                else:
                                    tmp_cr_list.append(int(c[0][7]))
                            
                            Pnorm = sum(tmp_cr_list)
                            if check_array[0] < workers or check_array[1] < tech:
                                tmp_pnorm = Pnorm
                                Pnorm = min((check_array[0] / workers), (check_array[1] / tech)) * tmp_pnorm
                                workers = check_array[0]
                                tech = check_array[1]
                            
                            
                            
                            loaded = 0
                            if train_expeditor[iter][4] > train[0][2]:
                                loaded = (int(train[0][2]))
                                already_loaded = already_loaded + int(train[0][2])
                            else:
                                loaded = int(train_expeditor[iter][4])
                                already_loaded = already_loaded + int(train_expeditor[iter][4])
                            
                            # train_expeditor[iter] = list(train_expeditor[iter])
                            # train_expeditor[iter][4] = train_expeditor[iter][4] - loaded
                            # train_expeditor[iter] = tuple(train_expeditor[iter])
                            
                            time = loaded / Pnorm * 43200
                            if self.meteo != []:
                                for meteo in self.meteo:
                                    k = 1
                                    # if meteo.precipitation == 1:
                                        # if train[0][1] == 26:
                                            # k = 0
                                    
                                    if meteo.windV > 10.7 and meteo.windV <= 13.8:
                                        k = 0.95
                                    
                                    if meteo.windV > 13.8 and meteo.windV <= 15:
                                        k = 0.9
                                    
                                    if meteo.windV > 15 and meteo.windV <= 20:
                                        k = 0.8
                                        
                                    if meteo.windV > 20:
                                        k = 0
                                        
                                    if int(meteo.windStart) > oper_time_start and int(meteo.windEnd) < (oper_time_start + time):
                                        
                                        dt = meteo.windEnd - meteo.windStart
                                        if k != 0:
                                            new_time = time - dt + dt / k
                                        else:
                                            new_time = time + dt
                                    
                                    if int(meteo.windStart) > oper_time_start and int(meteo.windEnd) >= (oper_time_start + time):
                                        
                                        dt = (oper_time_start + time) - meteo.windStart
                                        if k != 0:
                                            new_time = time - dt + dt / k
                                        else:
                                            new_time = time + dt
                                    
                                    if int(meteo.windStart) <= oper_time_start and int(meteo.windEnd) < (oper_time_start + time):
                                        
                                        dt = meteo.windEnd - oper_time_start
                                        if k != 0:
                                            new_time = time - dt + dt / k
                                        else:
                                            new_time = time + dt
                                    
                                    if int(meteo.windStart) < oper_time_start and int(meteo.windEnd) > (oper_time_start + time):
                                        new_time = time / k
                                        time = new_time
                                    
                            
                            
                            
                            tmp_e = []
                            for e in ship_exps:
                                if e[2] == train_expeditor[iter][2]:
                                    tmp_e = e
                                    tmp_e = list(e)
                                    tmp_e[4] = e[4] - loaded
                                    tmp_e = tuple(tmp_e)
                                    ship_exps.remove(e)
                                    
                            if tmp_e != []:        
                                if tmp_e[4] > 0:
                                    ship_exps.append(tmp_e)
                            
                            
                            
                            
                            
                            total_time += time
                            time_start = oper_time_start + time
                            self.time_lines.append([oper_time_start, time_start, 1, train[0][0], train[0][8], 2, ship[0][0], ship[0][8], train[0][1], loaded, used_crans, workers, tech])
                            
                            changed_start_time = 0
                            if loaded != train[0][2]:
                                train[0] = list(train[0])
                                train[0][2] = train[0][2] - loaded
                                train[0][3] = time_start
                                train[0] = tuple(train[0])
                                self.calculateTrain(train, 1)
                                changed_start_time = self.time_lines[-1][1]
                            else:
                                self.calculated_trains.append(train[0][0])
                                
                            if changed_start_time != 0:
                                time_start = changed_start_time
                            
        
        # Продолжение операции, если на судне еще есть место
        if already_loaded != total_load:
    
            all_exps = []
            for e in ship_exps:
                stor_exps = storage_instance.getByExpCargo(str(e[2]),str(e[3]))
                if stor_exps != []:
                    for stor_exp in stor_exps:
                        all_exps.append(stor_exp)
                        
            tmp_stor_exp = []
            
            if direct_stor != 0:
                if all_exps != []:
                    for all_row in all_exps:
                        if all_row[2] == direct_stor:
                            tmp_stor_exp.append(all_row)
                            all_exps.remove(all_row)
            
            if short_stor != 0:
                if all_exps != []:
                    for all_row in all_exps:
                        if all_row[2] == short_stor:
                            tmp_stor_exp.append(all_row)
                            all_exps.remove(all_row)
            
            all_exps = tmp_stor_exp + all_exps
            
            
            
            if all_exps != []:
                for exp in all_exps:
                    if ship_exps != []:
                        current_exp = ()
                        for sh_e in ship_exps:
                            if sh_e[2] == exp[1]:
                                current_exp = sh_e
                        oper_time_start = int(ship[0][5])
                        if time_start != int(ship[0][5]):
                            oper_time_start = time_start
                        
                        check_array = self.checkTime(oper_time_start)
                        
                        if check_array[0] > 0 and check_array[1] > 0:
                            tech_lines_left = 3    
                            additional_ids = ""
                            if check_array[2] != []:
                                additional_ids = " and num NOT IN ("
                                for cr in check_array[2]:
                                    additional_ids += "'" + str(cr) + "', "
                                    
                                additional_ids = additional_ids[:-2] + ")"
                            
                            
                            ship_crans = cran.getBy('object_id', '=', str(ship[0][8]) + " and type=2" + additional_ids)
                            if ship_crans != []:
                                if exp[2] == short_stor:
                                    Pnorm = 0
                                    workers_per_cran = 3
                                    tech_per_cran = 2
                                    
                                    if len(ship_crans) > 3:
                                        ship_crans = ship_crans[0:3]
                                      
                                    workers = workers_per_cran * len(ship_crans)
                                    tech = tech_per_cran * len(ship_crans)
                                    tmp_cr_list = []
                                    used_crans = []
                                    for cr1 in ship_crans:
                                        used_crans.append(cr1[1])
                                        c_t = CranType()
                                        c = c_t.find(cr1[2])
                                        if int(train[0][1]) == 1:
                                            tmp_cr_list.append(int(c[0][4]))
                                        else:
                                            tmp_cr_list.append(int(c[0][5]))
                                        
                                    
                                    Pnorm = sum(tmp_cr_list)
                                elif exp[2] == direct_stor:
                                    Pnorm = 0
                                    workers_per_cran = 3
                                    tech_per_cran = 2
                                    
                                    if len(ship_crans) > 3:
                                        ship_crans = ship_crans[0:3]
                                      
                                    workers = workers_per_cran * len(ship_crans)
                                    tech = tech_per_cran * len(ship_crans)
                                    tmp_cr_list = []
                                    used_crans = []
                                    for cr1 in ship_crans:
                                        used_crans.append(cr1[1])
                                        c_t = CranType()
                                        c = c_t.find(cr1[2])
                                        if int(train[0][1]) == 1:
                                            tmp_cr_list.append(int(c[0][2]))
                                        else:
                                            tmp_cr_list.append(int(c[0][3]))
                                        
                                    
                                    Pnorm = sum(tmp_cr_list)
                                else:
                                    
                                    Pnorm = 0
                                    workers_per_cran = 4
                                    tech_per_cran = 3
                                    if exp[3] == 27:
                                        workers_per_cran = 5
                                        tech_per_cran = 2
                                    sec_crans = cran.getBy('object_id', '=', str(exp[2]) + " and type=1" + additional_ids)
                                    if min(len(sec_crans), len(ship_crans)) < 3:
                                        crans1 = ship_crans[0:min(len(sec_crans), len(ship_crans))]
                                        crans2 = sec_crans[0:min(len(sec_crans), len(ship_crans))]
                                    else:
                                        crans1 = ship_crans[0:3]
                                        crans2 = sec_crans[0:3]
                                        
                                    workers = workers_per_cran * len(ship_crans)
                                    tech = tech_per_cran * len(ship_crans)
                                    # рассчет производительности
                                    used_crans = []
                                    tmp_cr_list = []
                                    tmp_cr_list2 = []
                                    # Краны склада. Берем производительность крана с подвозом. Т.к. подвозить можно только уголь - берем в формулу только
                                    # performance_coal_2   в списке [0][4]
                                    for cr1 in crans1:
                                        c_t = CranType()
                                        c = c_t.find(cr1[2])
                                        used_crans.append(cr1[1])
                                        tmp_cr_list.append(int(c[0][4]))
                                        
                                    # Краны жд пути. Берем производительность при работе с ЖД составом. Т.к. подвозить можно только уголь - берем в формулу
                                    # только performance_coal_3   в списке [0][6]    
                                    for cr2 in crans2:
                                        c_t = CranType()
                                        c = c_t.find(cr2[2])
                                        used_crans.append(cr2[1])
                                        tmp_cr_list2.append(int(c[0][6]))
                                    
                                    Pnorm = min(sum(tmp_cr_list), sum(tmp_cr_list2))     
                                            
                                
                                 
                                
                                if check_array[0] < workers or check_array[1] < tech:
                                    tmp_pnorm = Pnorm
                                    Pnorm = min((check_array[0] / workers), (check_array[1] / tech)) * tmp_pnorm
                                    workers = check_array[0]
                                    tech = check_array[1]        
                                            
                                
                                    
                                loaded = 0
                                if exp[4] >= current_exp[4]:
                                    loaded = current_exp[4]
                                    already_loaded = already_loaded + int(loaded)
                                else:
                                    loaded = exp[4]
                                    already_loaded = already_loaded + int(loaded)
                                
                                time = loaded / Pnorm * 43200
                                if self.meteo != []:
                                    for meteo in self.meteo:
                                        k = 1
                                        # if meteo.precipitation == 1:
                                            # if train[0][1] == 26:
                                                # k = 0
                                        
                                        if meteo.windV > 10.7 and meteo.windV <= 13.8:
                                            k = 0.95
                                        
                                        if meteo.windV > 13.8 and meteo.windV <= 15:
                                            k = 0.9
                                        
                                        if meteo.windV > 15 and meteo.windV <= 20:
                                            k = 0.8
                                            
                                        if meteo.windV > 20:
                                            k = 0
                                            
                                        if int(meteo.windStart) > oper_time_start and int(meteo.windEnd) < (oper_time_start + time):
                                            
                                            dt = meteo.windEnd - meteo.windStart
                                            if k != 0:
                                                new_time = time - dt + dt / k
                                            else:
                                                new_time = time + dt
                                        
                                        if int(meteo.windStart) > oper_time_start and int(meteo.windEnd) >= (oper_time_start + time):
                                            
                                            dt = (oper_time_start + time) - meteo.windStart
                                            if k != 0:
                                                new_time = time - dt + dt / k
                                            else:
                                                new_time = time + dt
                                        
                                        if int(meteo.windStart) <= oper_time_start and int(meteo.windEnd) < (oper_time_start + time):
                                            
                                            dt = meteo.windEnd - oper_time_start
                                            if k != 0:
                                                new_time = time - dt + dt / k
                                            else:
                                                new_time = time + dt
                                        
                                        if int(meteo.windStart) < oper_time_start and int(meteo.windEnd) > (oper_time_start + time):
                                            new_time = time / k
                                            time = new_time
                                        
                        
                                
                                tmp_e = []
                                for e in ship_exps:
                                    if e[2] == exp[1]:
                                        tmp_e = e
                                        tmp_e = list(e)
                                        tmp_e[4] = e[4] - loaded
                                        tmp_e = tuple(tmp_e)
                                        ship_exps.remove(e)
                                if tmp_e != []:        
                                    if tmp_e[4] > 0:
                                        ship_exps.append(tmp_e)
                                
                                if (int(exp[4]) - loaded) < 1:
                                    storage_instance.setQuery("delete from expeditor_storage_link where id = " + str(exp[0]))
                                else:
                                    storage_instance.setQuery("UPDATE expeditor_storage_link set cargo_amount = '" + str(int(exp[4]) - loaded) + "' where id = " + str(exp[0]))
                                
                                total_time += time
                                time_start = oper_time_start + time
                                self.time_lines.append([oper_time_start, time_start, 3, exp[2], None, 2, ship[0][0], ship[0][8], exp[3], loaded, used_crans, workers, tech])
                                            
                                            
                                          
                            # cran_nums = "("
                            # for sh_cr in ship_crans:
                                # cran_nums += str(sh_cr[1]) + ", "
                            # cran_nums = cran_nums[:-2] + ")"
                            # direct_crans = []    
                            # if exp[2] == prior_storage:
                                # direct_crans = cran.getBy('object_id', '=', str(prior_storage) + " and type=1 and num IN " + cran_nums)
                                # tech_lines_left = tech_lines_left - len(direct_crans)
                            
                            # if direct_crans != []:
                                
                                
                                
                                
                                # нужно 3 человека, 3 техники и 2 крана
                                
                    
                    
            else:
                if isinstance(ship_id, list):
                    self.getNextObject()
                    return False    
                    
                oper_time_start = int(ship[0][5])
                if time_start != int(ship[0][5]):
                    oper_time_start = time_start
                    
                self.time_lines.append([oper_time_start, 0, 2, ship[0][0], ship[0][8], 0, 0, 0, 0, 0, 0, 0, 0])
        else:
            t = 0
        
        # print(self.time_lines)
        # if already_loaded == total_load:
        self.calculated_ships.append(ship[0][0])  
        if from_train_func == None:
            self.getNextObject()        
        
    def start(self):
        meta = Meta()
        meta.prepare()
        
        self.getNextObject()
        
        meta.returnValues()
        return self.time_lines
        
    def getStorageCongestionLeft(self,cargo, storage_id):
        perc_left = 100 - self.getStorageCongestion(storage_id)
        sdv = StorageDefVal()
        storage_params = sdv.getBy('storage', '=' , str(storage_id))
        capW = 0
        for p in storage_params:
            if int(cargo) == int(p[2]):
                capW = p[4]
        
        val = capW * perc_left / 100
        
        return val
    
    def getStorageCongestion(self, storage_id):
        total_perc = 0
        storage = Storage() 
        exps = storage.getExpeditors(storage_id)
        st_d_v = StorageDefVal()
        default_values = st_d_v.getBy('storage', '=' , str(storage_id))
        if default_values != []:
            for r in exps:
                capW = 0
                for p in default_values:
                    if int(r[3]) == int(p[2]):
                        capW = p[4]
                        
                v = str(capW)
                capW = float(v.replace(',', '.'))
                v = str(r[4])
                cap = float(v.replace(',', '.'))
                total_perc = total_perc + (cap * 100 / capW )
                
        return total_perc
        
class Meta():
    def __init__(self):
        self.data = None
        
    def prepare(self):
        c = db_connection.cursor()
        c.execute("select * from expeditor_storage_link")
        res = c.fetchall()
        c.execute("DELETE FROM meta_exp_stor")
        if res != []:
            for row in res:
                c.execute("insert into meta_exp_stor (id,expeditor_id, storage_id, cargo, cargo_amount) VALUES('" + str(row[0]) + "','" + str(row[1]) + "','" + str(row[2]) + "','" + str(row[3]) + "','" + str(row[4]) + "')")
        db_connection.commit()
        
    def returnValues(self):
        c = db_connection.cursor()
        c.execute("select * from meta_exp_stor")
        res = c.fetchall()
        c.execute("DELETE FROM expeditor_storage_link")
        if res != []:
            for row in res:
                c.execute("insert into expeditor_storage_link (id,expeditor_id, storage_id, cargo, cargo_amount) VALUES('" + str(row[0]) + "','" + str(row[1]) + "','" + str(row[2]) + "','" + str(row[3]) + "','" + str(row[4]) + "')")
        db_connection.commit()
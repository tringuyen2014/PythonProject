import sys
import os
import sqlite3
from contextlib import closing

from business import Product
from business import LineItem

conn = None

def connect():
    global conn
    if not conn:
        if sys.platform == "win32":
            DB_FILE = "C:\\Users\\Tri Nguyen\\Desktop\\shoppingCart\\shopping_cart.sqlite"
        else:
            HOME = os.environ["HOME"]
            DB_FILE = HOME + "C:\\Users\\Tri Nguyen\\Desktop\\shoppingCart\\shopping_cart.sqlite"
            
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
    enableForeignKey()

def close():
    if conn:
        conn.close()

def enableForeignKey():
    sql = '''PRAGMA foreign_keys = ON'''
    with closing(conn.cursor()) as c:
        c.execute(sql)
    conn.commit()
    

def addItemtoDB(item):
    sql = '''INSERT INTO Inventory(name, price, discount) VALUES (?, ?, ?)'''
    with closing(conn.cursor()) as c:
        c.execute(sql, (item.name, item.price, item.discountPercent))
    conn.commit()

def deleteIteminDB(item):
    sql = '''DELETE FROM Inventory WHERE name = ?'''
    with closing(conn.cursor()) as c:
        c.execute(sql, (item,))
    conn.commit()
    

def makeItemObject(row):
    return Product(row["name"], row["price"], row["discount"])

def showItem():
    query = '''SELECT * FROM Inventory'''
    with closing(conn.cursor()) as c:
        c.execute(query)
        results = c.fetchall()

    item = []
    for row in results:
        item.append(makeItemObject(row))
    return item


def modifyItemDB(name, newName, newPrice, newDiscountPercent):
    with closing(conn.cursor()) as c:
        c.execute("UPDATE Inventory set name = ?, price = ?, discount = ? WHERE name = ?",
          (newName, newPrice, newDiscountPercent, name))
    conn.commit()
    

def register(username,password):
    if uniqueUsername(username) == 0:
        sql = '''INSERT INTO User(username, password, role) VALUES (?, ?, ?)'''
        with closing(conn.cursor()) as c:
            c.execute(sql, (username, password, "reg"))
        conn.commit()
        return 1
    else:
        return 0


def uniqueUsername(username):
    query = '''SELECT * FROM User WHERE username = ?'''
    with closing(conn.cursor()) as c:
        c.execute(query, (username,))
        row = c.fetchone()
        if row:
            return 1
        else:
            return 0

def login(username,password):
    query = '''SELECT * FROM User WHERE username = ?'''
    with closing(conn.cursor()) as c:
        c.execute(query, (username,))
        result = c.fetchone()
        
        if result:
            if result["password"]== password:
               return result["role"]
            else:
               return 1 
        else:
            return 0
        
def getUserRole(username):
    query = '''SELECT * FROM User WHERE username = ?'''
    with closing(conn.cursor()) as c:
        c.execute(query, (username,))
        result = c.fetchone()
        
    return result["role"]


def getItemCount (username):
    query = '''SELECT count()
                FROM Cart ct
                INNER JOIN User ut ON ut.userid = ct.userid
                LEFT OUTER JOIN Inventory it ON it.itemid = ct.itemid
                WHERE ut.username = ?'''
    with closing(conn.cursor()) as c:
        c.execute(query, (username,))
        result = c.fetchone()
        if result:
               return result["count()"]
        else:
            return 0

    
def makeLineItemObject(row):
    return LineItem(row["itemid"],row["quantity"])

def getCartItem(username):
    query = '''SELECT  it.itemid , ct.quantity
            FROM Cart ct
            INNER JOIN User ut ON ut.userid = ct.userid
            LEFT OUTER JOIN Inventory it ON it.itemid = ct.itemid
            WHERE ut.username = ?'''
    with closing(conn.cursor()) as c:
        c.execute(query, (username,))
        results = c.fetchall()

    item = []
    for row in results:
        item.append(makeLineItemObject(row))
    return item

def getProductDetail(itemid):
    query = '''SELECT * FROM Inventory Where itemid = ?'''
    with closing(conn.cursor()) as c:
        c.execute(query, (itemid,))
        result = c.fetchone()

    return Product(result["name"], result["price"], result["discount"])

def getItemid(name):
    query = '''SELECT * FROM Inventory Where name = ?'''
    with closing(conn.cursor()) as c:
        c.execute(query, (name,))
        result = c.fetchone()
    return result["itemid"]

def getUserid(username):
    query = '''SELECT * FROM User Where username = ?'''
    with closing(conn.cursor()) as c:
        c.execute(query, (username,))
        result = c.fetchone()
    return result["userid"]


def addItemtoCart(username,name,quantity):
    itemid = getItemid(name)
    userid = getUserid(username)
    sql = '''INSERT INTO Cart(itemid, userid, quantity) VALUES (?, ?, ?)'''
    with closing(conn.cursor()) as c:
        c.execute(sql, (itemid, userid, quantity))
    conn.commit()

def deleteItemCart(username,itemid,quantity):
    with closing(conn.cursor()) as c:
        c.execute("DELETE FROM Cart WHERE userid = ? AND itemid = ? AND quantity = ?",
          (getUserid(username), itemid, quantity))
    conn.commit()
    
def modifyItemCart(username,itemid,quantity, mod):
    with closing(conn.cursor()) as c:
        c.execute("UPDATE Cart set quantity = ? WHERE userid = ? AND itemid = ? AND quantity = ?",
          (mod, getUserid(username), itemid, quantity))
    conn.commit()

def checkOut(username):
    with closing(conn.cursor()) as c:
        c.execute("DELETE FROM Cart WHERE userid = ?",
          (getUserid(username),))
    conn.commit()


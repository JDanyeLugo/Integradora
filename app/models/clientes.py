from .db import get_connection

mydb = get_connection()

class clientes:

    def __init__(self, Nombre, Direccion, Telefono, Email, ID_Cliente=None):
        self.ID_Cliente = ID_Cliente
        self.Nombre = Nombre
        self.Direccion = Direccion
        self.Telefono = Telefono
        self.Email = Email

    def save(self):
        # Create a New Object in DB
        if self.ID_Cliente is None:
            with mydb.cursor() as cursor:
                sql = "INSERT INTO clientes(Nombre, Direccion, Telefono, Email) VALUES(%s, %s, %s, %s)"
                val = (self.Nombre, self.Direccion, self.Telefono, self.Email)
                cursor.execute(sql, val)
                mydb.commit()
                self.id = cursor.lastrowid
                return self.ID_Cliente
        # Update an Object
        else:
            with mydb.cursor() as cursor:
                sql = "UPDATE clientes SET Nombre = %s, Direccion = %s , Telefono = %s , Email = %s WHERE ID_Cliente = %s"
                val = (self.Nombre, self.Direccion, self.Telefono, self.Email, self.ID_Cliente)
                cursor.execute(sql, val)
                mydb.commit()
                return self.ID_Cliente
            
    def delete(self):
        with mydb.cursor() as cursor:
            sql = f"DELETE FROM clientes WHERE ID_Clientes = { self.ID_Cliente }"
            cursor.execute(sql)
            mydb.commit()
            return self.ID_Cliente
            
    @staticmethod
    def get(id):
        with mydb.cursor(dictionary=True) as cursor:
            sql = f"SELECT category, description FROM categories WHERE id = { id }"
            cursor.execute(sql)
            result = cursor.fetchone()
            print(result)
            category = Category(result["category"], result["description"], id)
            return category
        
    @staticmethod
    def get_all():
        categories = []
        with mydb.cursor(dictionary=True) as cursor:
            sql = f"SELECT id, category, description FROM categories"
            cursor.execute(sql)
            result = cursor.fetchall()
            for item in result:
                categories.append(Category(item["category"], item["description"], item["id"]))
            return categories
    
    @staticmethod
    def count_all():
        with mydb.cursor() as cursor:
            sql = f"SELECT COUNT(id) FROM categories"
            cursor.execute(sql)
            result = cursor.fetchone()
            return result[0]
        
    def __str__(self):
        return f"{ self.id } - { self.category }"
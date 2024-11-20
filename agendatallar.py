import mysql.connector
from datetime import datetime

class DatabaseManager:
    """Clase para gestionar la conexión con MySQL."""
    def __init__(self, host="localhost", user="root", password="", database="agenda"):
        self.config = {
            "host": host,
            "user": user,
            "password": password,
            "database": database
        }
        self.connect()
        self.initialize_db()

    def connect(self):
        self.conn = mysql.connector.connect(**self.config)
        self.cursor = self.conn.cursor()

    def initialize_db(self):
        # Se asume que las tablas ya están creadas en phpMyAdmin
        pass

    def execute_query(self, query, params=None, fetch=False):
        self.cursor.execute(query, params or ())
        if fetch:
            return self.cursor.fetchall()
        else:
            self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()


class Categoria:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def crear(self, nombre):
        self.db_manager.execute_query("INSERT INTO categorias (nombre) VALUES (%s)", (nombre,))
        print(f"Categoría '{nombre}' creada con éxito.")

    def leer(self):
        categorias = self.db_manager.execute_query("SELECT * FROM categorias", fetch=True)
        if categorias:
            print("\n--- Categorías ---")
            for categoria in categorias:
                print(f"ID: {categoria[0]}, Nombre: {categoria[1]}")
        else:
            print("No hay categorías registradas.")

    def eliminar(self, categoria_id):
        self.db_manager.execute_query("DELETE FROM categorias WHERE id = %s", (categoria_id,))
        print(f"Categoría con ID {categoria_id} eliminada con éxito.")


class Contacto:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def crear(self, nombre, telefono, email, categoria_id):
        self.db_manager.execute_query('''
            INSERT INTO contactos (nombre, telefono, email, categoria_id) 
            VALUES (%s, %s, %s, %s)
        ''', (nombre, telefono, email, categoria_id))
        print(f"Contacto '{nombre}' creado con éxito.")

    def leer(self):
        contactos = self.db_manager.execute_query('''
            SELECT c.id, c.nombre, c.telefono, c.email, cat.nombre
            FROM contactos c
            LEFT JOIN categorias cat ON c.categoria_id = cat.id
        ''', fetch=True)
        if contactos:
            print("\n--- Contactos ---")
            for contacto in contactos:
                print(f"ID: {contacto[0]}, Nombre: {contacto[1]}, Teléfono: {contacto[2]}, Email: {contacto[3]}, Categoría: {contacto[4]}")
        else:
            print("No hay contactos registrados.")

    def actualizar(self, contacto_id, nombre, telefono, email, categoria_id):
        self.db_manager.execute_query('''
            UPDATE contactos
            SET nombre = %s, telefono = %s, email = %s, categoria_id = %s
            WHERE id = %s
        ''', (nombre, telefono, email, categoria_id, contacto_id))
        print(f"Contacto con ID {contacto_id} actualizado con éxito.")

    def eliminar(self, contacto_id):
        self.db_manager.execute_query("DELETE FROM contactos WHERE id = %s", (contacto_id,))
        print(f"Contacto con ID {contacto_id} eliminado con éxito.")


class Evento:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def crear(self, contacto_id, fecha, descripcion):
        self.db_manager.execute_query('''
            INSERT INTO eventos (contacto_id, fecha, descripcion) 
            VALUES (%s, %s, %s)
        ''', (contacto_id, fecha, descripcion))
        print("Evento creado con éxito.")

    def leer(self):
        eventos = self.db_manager.execute_query('''
            SELECT e.id, e.fecha, e.descripcion, c.nombre
            FROM eventos e
            LEFT JOIN contactos c ON e.contacto_id = c.id
        ''', fetch=True)
        if eventos:
            print("\n--- Eventos ---")
            for evento in eventos:
                print(f"ID: {evento[0]}, Fecha: {evento[1]}, Descripción: {evento[2]}, Contacto: {evento[3]}")
        else:
            print("No hay eventos registrados.")

    def eliminar(self, evento_id):
        self.db_manager.execute_query("DELETE FROM eventos WHERE id = %s", (evento_id,))
        print(f"Evento con ID {evento_id} eliminado con éxito.")


class Nota:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def crear(self, titulo, contenido):
        fecha_creacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.db_manager.execute_query('''
            INSERT INTO notas (titulo, contenido, fecha_creacion)
            VALUES (%s, %s, %s)
        ''', (titulo, contenido, fecha_creacion))
        print(f"Nota '{titulo}' creada con éxito.")

    def leer(self):
        notas = self.db_manager.execute_query("SELECT * FROM notas", fetch=True)
        if notas:
            print("\n--- Notas ---")
            for nota in notas:
                print(f"ID: {nota[0]}, Título: {nota[1]}, Contenido: {nota[2]}, Fecha: {nota[3]}")
        else:
            print("No hay notas registradas.")

    def actualizar(self, nota_id, titulo, contenido):
        self.db_manager.execute_query('''
            UPDATE notas
            SET titulo = %s, contenido = %s
            WHERE id = %s
        ''', (titulo, contenido, nota_id))
        print(f"Nota con ID {nota_id} actualizada con éxito.")

    def eliminar(self, nota_id):
        self.db_manager.execute_query("DELETE FROM notas WHERE id = %s", (nota_id,))
        print(f"Nota con ID {nota_id} eliminada con éxito.")


class Menu:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.categorias = Categoria(self.db_manager)
        self.contactos = Contacto(self.db_manager)
        self.eventos = Evento(self.db_manager)
        self.notas = Nota(self.db_manager)

    def mostrar_menu(self):
        while True:
            print("\n--- Menú Principal ---")
            print("1. Contactos")
            print("2. Categorías")
            print("3. Eventos")
            print("4. Notas")
            print("5. Salir")
            
            opcion = input("Selecciona una opción: ")
            
            if opcion == "1":
                self.menu_contactos()
            elif opcion == "2":
                self.menu_categorias()
            elif opcion == "3":
                self.menu_eventos()
            elif opcion == "4":
                self.menu_notas()
            elif opcion == "5":
                self.db_manager.close()
                break
            else:
                print("Opción no válida. Intente de nuevo.")

    def menu_contactos(self):
        while True:
            print("\n--- Menú de Contactos ---")
            print("1. Crear Contacto")
            print("2. Leer Contactos")
            print("3. Actualizar Contacto")
            print("4. Eliminar Contacto")
            print("5. Volver al Menú Principal")
            
            opcion = input("Selecciona una opción: ")
            
            if opcion == "1":
                self.categorias.leer()
                nombre = input("Nombre: ")
                telefono = input("Teléfono: ")
                email = input("Email: ")
                categoria_id = int(input("ID de Categoría: "))
                self.contactos.crear(nombre, telefono, email, categoria_id)
            elif opcion == "2":
                self.contactos.leer()
            elif opcion == "3":
                contacto_id = int(input("ID del Contacto: "))
                nombre = input("Nuevo Nombre: ")
                telefono = input("Nuevo Teléfono: ")
                email = input("Nuevo Email: ")
                categoria_id = int(input("Nuevo ID de Categoría: "))
                self.contactos.actualizar(contacto_id, nombre, telefono, email, categoria_id)
            elif opcion == "4":
                contacto_id = int(input("ID del Contacto a eliminar: "))
                self.contactos.eliminar(contacto_id)
            elif opcion == "5":
                break
            else:
                print("Opción no válida. Intente de nuevo.")

    def menu_categorias(self):
        while True:
            print("\n--- Menú de Categorías ---")
            print("1. Crear Categoría")
            print("2. Leer Categorías")
            print("3. Eliminar Categoría")
            print("4. Volver al Menú Principal")
            
            opcion = input("Selecciona una opción: ")
            
            if opcion == "1":
                nombre = input("Nombre de la Categoría: ")
                self.categorias.crear(nombre)
            elif opcion == "2":
                self.categorias.leer()
            elif opcion == "3":
                categoria_id = int(input("ID de la Categoría a eliminar: "))
                self.categorias.eliminar(categoria_id)
            elif opcion == "4":
                break
            else:
                print("Opción no válida. Intente de nuevo.")

    def menu_eventos(self):
        while True:
            print("\n--- Menú de Eventos ---")
            print("1. Crear Evento")
            print("2. Leer Eventos")
            print("3. Eliminar Evento")
            print("4. Volver al Menú Principal")
            
            opcion = input("Selecciona una opción: ")
            
            if opcion == "1":
                self.contactos.leer()
                contacto_id = int(input("ID del Contacto: "))
                fecha = input("Fecha del Evento (YYYY-MM-DD): ")
                descripcion = input("Descripción del Evento: ")
                self.eventos.crear(contacto_id, fecha, descripcion)
            elif opcion == "2":
                self.eventos.leer()
            elif opcion == "3":
                evento_id = int(input("ID del Evento a eliminar: "))
                self.eventos.eliminar(evento_id)
            elif opcion == "4":
                break
            else:
                print("Opción no válida. Intente de nuevo.")

    def menu_notas(self):
        while True:
            print("\n--- Menú de Notas ---")
            print("1. Crear Nota")
            print("2. Leer Notas")
            print("3. Actualizar Nota")
            print("4. Eliminar Nota")
            print("5. Volver al Menú Principal")
            
            opcion = input("Selecciona una opción: ")
            
            if opcion == "1":
                titulo = input("Título de la Nota: ")
                contenido = input("Contenido de la Nota: ")
                self.notas.crear(titulo, contenido)
            elif opcion == "2":
                self.notas.leer()
            elif opcion == "3":
                nota_id = int(input("ID de la Nota a actualizar: "))
                titulo = input("Nuevo Título: ")
                contenido = input("Nuevo Contenido: ")
                self.notas.actualizar(nota_id, titulo, contenido)
            elif opcion == "4":
                nota_id = int(input("ID de la Nota a eliminar: "))
                self.notas.eliminar(nota_id)
            elif opcion == "5":
                break
            else:
                print("Opción no válida. Intente de nuevo.")


if __name__ == "__main__":
    Menu().mostrar_menu()
class Menu:
    def _init_(self):
        self.db_manager = DatabaseManager()
        self.models = {
            "1": ("Contactos", Contacto(self.db_manager)),
            "2": ("Categorías", Categoria(self.db_manager)),
            "3": ("Eventos", Evento(self.db_manager)),
            "4": ("Notas", Nota(self.db_manager)),
        }

    def mostrar_menu(self):
        while True:
            print("\n--- Menú Principal ---")
            for key, (name, _) in self.models.items():
                print(f"{key}. {name}")
            print("5. Salir")

            opcion = input("Selecciona una opción: ")
            if opcion in self.models:
                self.mostrar_submenu(opcion)
            elif opcion == "5":
                self.db_manager.close()
                print("¡Hasta luego!")
                break
            else:
                print("Opción no válida. Intente de nuevo.")

    def mostrar_submenu(self, opcion):
        name, model = self.models[opcion]
        while True:
            print(f"\n--- Menú de {name} ---")
            print("1. Crear")
            print("2. Leer")
            print("3. Actualizar")
            print("4. Eliminar")
            print("6. Volver")

            subopcion = input("Selecciona una opción: ")
            if subopcion == "1":
                pass  # Implementar lógica
            elif subopcion == "2":
                model.leer()
            elif subopcion == "6":
                break

if _name_ == "_main_":
    Menu().mostrar_menu()

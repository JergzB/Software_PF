from flet import *
import flet as ft
import sqlite3
import os

# Colores de letras
col_letters = {"text": "black", "button": "white"}

# Colores de fondos
col_bg = {"txt_field": "#f0f3f6", "bg": "white"}

# Nombre del archivo de la base de datos
db_name = "clientes.db"

# Si la base de datos no existe, se crea y se inicializa con las tablas necesarias
if not os.path.exists(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Creación de la tabla 'clientes'
    cursor.execute("""CREATE TABLE IF NOT EXISTS clientes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        apellido TEXT NOT NULL,
        celular TEXT UNIQUE,
        correo TEXT,
        cedula TEXT UNIQUE
        )""")

    conn.commit()

    # Creación de la tabla 'vehiculos'
    cursor.execute("""CREATE TABLE IF NOT EXISTS vehiculos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        marca TEXT NOT NULL,
        modelo TEXT NOT NULL,
        año TEXT,
        placa TEXT UNIQUE,
        tipo_vehiculo TEXT,
        traccion TEXT
        )""")

    conn.commit()
    conn.close()

# Función para agregar un cliente a la base de datos
def add_client(nombre: str, apellido: str, celular: str, correo: str, cedula: str):
    # Imprimir datos recibidos para debug
    print(nombre, apellido, celular, correo, cedula)
    try:
        conn = sqlite3.connect(db_name, check_same_thread=False)
        cursor = conn.cursor()

        # Insertar datos del cliente en la tabla 'clientes'
        cursor.execute("INSERT INTO clientes (nombre, apellido, celular, correo, cedula) VALUES (?,?,?,?,?)",
                       (nombre, apellido, celular, correo, cedula))

        conn.commit()

    except sqlite3.Error as e:
        print("Hubo un error: ", e)

    finally:
        conn.close()

# Función para eliminar un cliente de la base de datos
def remove_client(id, **kwargs):
    # Construcción de la cláusula WHERE para la eliminación
    where_clause = '=(?) AND '.join([f'{key}' for key in kwargs])
    where_clause_f = where_clause + "=(?)"
    values = list(kwargs.values())

    sql = f"DELETE FROM clientes WHERE {where_clause_f} OR id = {id}"

    try:
        conn = sqlite3.connect(db_name, check_same_thread=False)
        cursor = conn.cursor()

        # Ejecutar la eliminación del cliente
        cursor.execute(sql, values)
        conn.commit()

    except sqlite3.Error as e:
        print("Hubo un fallo: ", e)

    finally:
        conn.close()

# Función para actualizar los datos de un cliente
def update_client(id, **kwargs):
    # Construcción de la cláusula SET para la actualización
    set_clause = '=(?), '.join([f'{key}' for key in kwargs])
    set_clause_f = set_clause + '=(?)'
    values = list(kwargs.values())

    sql = f'UPDATE clientes SET {set_clause_f} WHERE id={id}'

    print(set_clause_f)

    try:
        conn = sqlite3.connect(db_name, check_same_thread=False)
        cursor = conn.cursor()

        # Ejecutar la actualización del cliente
        cursor.execute(sql, values)
        conn.commit()
    except sqlite3.Error as e:
        print("Ha surgido un error: ", e)

    finally:
        conn.close()

# Función para leer los datos de un cliente específico
def read_client(id, **kwargs):
    
    # Construcción de la cláusula WHERE para la selección
    
    where_clause = '=(?),'.join([f'{key}' for key in kwargs])
    where_clause_f = where_clause + '=(?)'
    values = list(kwargs.values())

    sql = f"SELECT * FROM clientes WHERE {where_clause_f} OR id ={id}"

    try:
        conn = sqlite3.connect(db_name, check_same_thread=False)
        cursor = conn.cursor()

        # Ejecutar la selección del cliente
        cursor.execute(sql, values)
        cliente = cursor.fetchone()
        conn.commit()

        return cliente

    except sqlite3.Error as e:
        print("Hubo un error: ", e)

    finally:
        conn.close()

# Función para seleccionar todos los clientes de la base de datos
def select_all():
    try:
        conn = sqlite3.connect(db_name, check_same_thread=False)
        cursor = conn.cursor()

        # Ejecutar la selección de todos los clientes
        cursor.execute("SELECT * FROM clientes")
        clientes = cursor.fetchall()
        conn.commit()

    except sqlite3.Error as e:
        print("Hubo un error: ", e)

    finally:
        conn.close()
        return clientes

# Función principal que define la interfaz de la aplicación
def main(page: Page):
    page.title = "Clientes"
    page.bgcolor = "white"

    # Definición de campos de entrada (TextField)
    nombre = TextField(
        height=20,
        width=200,
        hint_text="Marcelo",
        hint_style=TextStyle(
            size=12,
            color="black"
        )
    )
    apellido = TextField(
        height=20,
        width=200,
        hint_text="Oleas",
        hint_style=TextStyle(
            size=12,
            color="black"
        )
    )
    celular = TextField(
        height=20,
        width=200,
        hint_text="0992564584",
        hint_style=TextStyle(
            size=12,
            color="black"
        )
    )
    correo = TextField(
        height=20,
        width=200,
        hint_text="maoleascu@uide.edu.ec",
        hint_style=TextStyle(
            size=12,
            color="black"
        )
    )
    cedula = TextField(
        height=20,
        width=200,
        hint_text="2351157231",
        hint_style=TextStyle(
            size=12,
            color="black"
        )
    )

    # Función para manejar el evento de agregar cliente
    def add_client_main(e):
        add_client(nombre.value, apellido.value, celular.value, correo.value, cedula.value)
        page.update()

    def eliminate_client_main(e):
        remove_client()

    def read_client_main(e):
        read_client()

    def view_pop(e: ViewPopEvent):
        page.views.pop()
        top_view: View = page.views[-1]
        page.go(top_view)

    # Función para manejar el cambio de ruta
    def route_change(event):
        page.views.clear()
        page.views.append(
            View(
                route="/clientes",
                controls=page.controls,
            )
        )

        items = select_all()
        # Definición de la tabla para mostrar los clientes
        tabla = DataTable(
            columns=[
                DataColumn(Text("Nombre")),
                DataColumn(Text("Apellido")),
                DataColumn(Text("Celular"), numeric=True),
                DataColumn(Text("Correo")),
                DataColumn(Text("Cedula"), numeric=True),
            ],
            rows=[
                DataRow(
                    cells=[
                        DataCell(Text(f"{item[1]}")),
                        DataCell(Text(f"{item[2]}")),
                        DataCell(Text(f"{item[3]}")),
                        DataCell(Text(f"{item[4]}")),
                        DataCell(Text(f"{item[5]}")),
                    ]
                ) for item in items
            ]
        )

        # Ventana secundaria para mostrar la tabla
        ventana_secundaria = Window(
            title="Registro de la Base de Datos",
            vertical_alignment=MainAxisAlignment.CENTER,
            horizontal_alignment=CrossAxisAlignment.CENTER,
            content=Column([tabla]),
        )

        ventana_secundaria.show()

    # Agregar los controles a la página principal
    page.add(
        Column(
            horizontal_alignment="center",
            controls=[
                Container(padding=15),
                Container(
                    content=Text(
                        value="Clientes",
                        size=30,
                        color="black",
                        weight="bold"
                    )
                ),
                Container(padding=15),
                Row(
                    alignment=MainAxisAlignment.CENTER,
                    vertical_alignment="center",
                    controls=[
                        Container(
                            content=Text(
                                value="Número:"
                            ),
                            padding=5
                        ),
                        TextField(
                            height=20,
                            width=100,
                            hint_text="0992564584",
                            hint_style=TextStyle(
                                size=12,
                                color="black"
                            )
                        ),
                        ElevatedButton(
                            text="Buscador",
                            on_click=None  # Aquí se agregará la función para buscar un cliente
                        ),
                        ElevatedButton(
                            text="Ver todos",
                            on_click=route_change  # Llama a la función que muestra todos los clientes
                        )
                    ]
                ),
                Container(padding=20),
                Column(
                    controls=[
                        Container(
                            content=Text(
                                value="Datos Cliente",
                                weight="bold",
                                size=15
                            )
                        ),
                        Row(
                            vertical_alignment="left",
                            alignment=MainAxisAlignment.START,
                            controls=[
                                Container(
                                    content=Text(
                                        value="Nombre:",
                                        size=12,
                                        color="black"
                                    )
                                ),
                                nombre
                            ]
                        ),
                        Row(
                            vertical_alignment="left",
                            alignment=MainAxisAlignment.START,
                            controls=[
                                Container(
                                    content=Text(
                                        value="Apellido:",
                                        size=12,
                                        color="black"
                                    )
                                ),
                                apellido
                            ]
                        ),
                        Row(
                            vertical_alignment="left",
                            alignment=MainAxisAlignment.START,
                            controls=[
                                Container(
                                    content=Text(
                                        value="Celular:",
                                        size=12,
                                        color="black"
                                    )
                                ),
                                celular
                            ]
                        ),
                        Row(
                            vertical_alignment="left",
                            alignment=MainAxisAlignment.START,
                            controls=[
                                Container(
                                    content=Text(
                                        value="Correo:",
                                        size=12,
                                        color="black"
                                    )
                                ),
                                correo
                            ]
                        ),
                        Row(
                            vertical_alignment="left",
                            alignment=MainAxisAlignment.START,
                            controls=[
                                Container(
                                    content=Text(
                                        value="Cédula:",
                                        size=12,
                                        color="black"
                                    )
                                ),
                                cedula
                            ]
                        )
                    ],
                ),
                Row(
                    alignment=MainAxisAlignment.CENTER,
                    vertical_alignment="center",
                    controls=[
                        ElevatedButton(
                            text="Agregar",
                            on_click=add_client_main  # Llama a la función que agrega un cliente
                        ),
                        ElevatedButton(
                            text="Editar"
                        ),
                        ElevatedButton(
                            text="Eliminar"
                        ),
                        ElevatedButton(
                            text="Limpiar",
                            on_click=None  # Aquí se puede agregar una función para limpiar los campos
                        )
                    ]
                )
            ]
        )
    )

    page.on_view_pop = view_pop

# Inicia la aplicación llamando a la función 'main'
if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.FLET_APP)

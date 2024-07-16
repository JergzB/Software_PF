import flet as ft
from flet import *
from flet_core.control_event import ControlEvent
import pyrebase

config = {
  "apiKey": "AIzaSyAjlsCCSdhvKWgKB4RSRO8GLMASA3vNIks",
  "authDomain": "prueba01-84f1b.firebaseapp.com",
  "projectId": "prueba01-84f1b",
  "storageBucket": "prueba01-84f1b.appspot.com",
  "messagingSenderId": "493477933625",
  "appId": "1:493477933625:web:cd24784d25c9e1707653e8",
  "measurementId": "G-BYZDWJ19VJ",
  "databaseURL": "",
} 

# Código para inicializar la base de datos de Firebase
firebase = pyrebase.initialize_app(config=config)
firebase.auth()

class UIControl(UserControl):
    def __init__(self, titulo:str, subtitulo:str, btn_name:str) -> None:
        self.titulo = titulo
        self.subtitulo = subtitulo
        self.btn_name = btn_name
        super().__init__()
        #self.build()
    
    def textField(self, text:str, hide:bool):
        return Container(
            alignment=alignment.center,
            content=TextField(
                height=50,
                width=255,
                bgcolor="f0f3f6",
                border_radius=10,
                hint_text= text,
                color="black",
                text_size=12,
                filled=True,
                cursor_color="black",
                border_color="transparent",
                hint_style=TextStyle(
                    size=11,
                    color="black"
                ),
                password=hide
            )
        )
    
    def sign_in_func(self, name:str):
        print("You have signed in by: "+ name)
    
    def sign_in_opt(self, text:str, path:str):
        return Container(
            alignment=alignment.center,
            content=ElevatedButton(
                on_click=lambda:self.sign_in_func("facebook"),
                height=40,
                width = 255,
                content=Row(
                    alignment="center",
                    controls=[
                        Image(
                            src=path,
                            width=30,
                            height=30
                            ),
                        Text(
                            text,
                            text_align="center",
                            color="black"
                        ),
                        
                    ]
                    ),  
                style=ButtonStyle(
                    shape={
                        "":RoundedRectangleBorder(radius=8)
                    },
                    bgcolor={"":"#f0f3f6"},
                )
            )
        )
    
    def build(self):
        
        self._titulo = Container(
            alignment=alignment.center,
            content=Text(
                self.titulo,
                size = 15,
                text_align="center",
                weight="bold",
                color="black"
            )
        )
        
        self._subtitulo = Container(
            alignment=alignment.center,
            content=Text(
                self.subtitulo, 
                color="black",
                size=10,
                text_align="center",
            )
        )
        
        self._sign_btn = Container(
            alignment=alignment.center,
            content=ElevatedButton(
                on_click=None,
                content=Text(
                    self.btn_name,
                    size=12,
                    weight="bold",
                    color="white"
                ),
                style=ButtonStyle(
                    shape={
                        "":RoundedRectangleBorder(radius=8)
                    },
                    bgcolor={"":"black"},
                ),
                height=48,
                width=255
            )
        )
        
        return Column(
            horizontal_alignment="center",
            controls=[
                Container(padding = 10),
                self._titulo,
                self._subtitulo,
                Column(
                    spacing=20,
                    controls = [
                        self.textField("Email", False),
                        self.textField("Password", True)    
                    ]
                ),
                Container(padding=15),
                self._sign_btn,
                Container(padding=15),
                Column(
                    horizontal_alignment = "center",
                    spacing=20,
                    controls=[
                        Container(
                            content=Text(
                                "Or continue with",
                                size=10,
                                color="black"),
                            ),
                        self.sign_in_opt("facebook", "assets/facebook-logo-0.png"),   
                    ]
                )
            ]
        )

def main(page:Page):
    
    page.title = "Flet with Firebase"
    page.bgcolor = "#f0f3f6"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    
    def _main_column_():
        return Container(
            width=280,
            height=600,
            bgcolor="#ffffff",
            padding=10,
            content=Column(
                spacing=20,
                horizontal_alignment="center"
            )
        )

            
        
    sign_in = UIControl("Ingresar", "Bienvenido de nuevo!","Ingresar")
    reg = UIControl("Regístrate!", "Holiwis", "Registrarse")
    
    sign_in_main = _main_column_()
    sign_in_main.content.controls.append(Container(padding=15))
    sign_in_main.content.controls.append(sign_in)
    
    
    
    reg_in_main = _main_column_()
    reg_in_main.content.controls.append(Container(padding=15))
    reg_in_main.content.controls.append(reg)
    
    page.add(
        Row(
            alignment="center",
            spacing=25,
            controls={
                sign_in_main,
                reg_in_main
            }
        )
    )
    

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
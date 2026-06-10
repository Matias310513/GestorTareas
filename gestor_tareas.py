from io import open
import tkinter as tk
from tkinter import messagebox
from datetime import datetime


class Tarea:
    def __init__(self, titulo, descripcion):
        self.__titulo = titulo
        self.__descripcion = descripcion
        self.__estado = 'Pendiente'
        self.__fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def get_titulo(self):
        return self.__titulo

    def get_descripcion(self):
        return self.__descripcion

    def get_estado(self):
        return self.__estado

    def get_fecha(self):
        return self.__fecha

    def set_estado(self, estado):
        self.__estado = estado

    def set_fecha(self, fecha):
        self.__fecha = fecha

    def mostrar_info(self):
        return self.__titulo + ' | ' + self.__descripcion + ' | ' + self.__estado + ' | ' + self.__fecha

    def __str__(self):
        return self.mostrar_info()
    

class TareaUrgente(Tarea):
    def mostrar_info(self):
        return 'URGENTE | ' + self.get_titulo() + ' | ' + self.get_descripcion() + ' | ' + self.get_estado() + ' | ' + self.get_fecha()


class GestorTareas:
    def __init__(self):
        self.tareas = []
        self.archivo = 'tareas.txt'
        self.cargar_tareas()

    def crear_linea(self, tarea):
        if isinstance(tarea, TareaUrgente):
            tipo = 'URGENTE'
        else:
            tipo = 'NORMAL'

        return tipo + '|' + tarea.get_titulo() + '|' + tarea.get_descripcion() + '|' + tarea.get_estado() + '|' + tarea.get_fecha() + '\n'

    def agregar_tarea(self, tarea):
        self.tareas.append(tarea)

        try:
            archivo = open(self.archivo, 'a', encoding='utf-8')
            archivo.write(self.crear_linea(tarea))
            archivo.close()
        except Exception as e:
            messagebox.showerror('Error', 'No se pudo agregar la tarea.\n' + str(e))

    def eliminar_tarea(self, indice):
        del self.tareas[indice]
        self.guardar_tareas()

    def marcar_completada(self, indice):
        self.tareas[indice].set_estado('Completada')
        self.guardar_tareas()

    def guardar_tareas(self):
        try:
            archivo = open(self.archivo, 'w', encoding='utf-8')

            for tarea in self.tareas:
                archivo.write(self.crear_linea(tarea))

            archivo.close()
        except Exception as e:
            messagebox.showerror('Error', 'No se pudo guardar el archivo.\n' + str(e))

    def cargar_tareas(self):
        try:
            archivo = open(self.archivo, 'r', encoding='utf-8')
            contenido = archivo.read()
            archivo.close()

            for linea in contenido.split('\n'):
                if linea != '':
                    datos = linea.split('|')

                    if len(datos) == 5:
                        if datos[0] == 'URGENTE':
                            tarea = TareaUrgente(datos[1], datos[2])
                        else:
                            tarea = Tarea(datos[1], datos[2])

                        tarea.set_estado(datos[3])
                        tarea.set_fecha(datos[4])
                        self.tareas.append(tarea)

        except FileNotFoundError:
            archivo = open(self.archivo, 'w', encoding='utf-8')
            archivo.write('')
            archivo.close()
        except Exception as e:
            messagebox.showerror('Error', 'No se pudo cargar el archivo.\n' + str(e))


gestor = GestorTareas()


def actualizar_lista():
    lista.delete(0, tk.END)

    for tarea in gestor.tareas:
        lista.insert(tk.END, tarea.mostrar_info())


def agregar_tarea():
    try:
        titulo = entry_titulo.get()
        descripcion = entry_descripcion.get()

        if titulo == '':
            raise ValueError('Debe ingresar el titulo de la tarea.')

        if descripcion == '':
            raise ValueError('Debe ingresar la descripcion de la tarea.')

        if urgente.get():
            tarea = TareaUrgente(titulo, descripcion)
        else:
            tarea = Tarea(titulo, descripcion)

        gestor.agregar_tarea(tarea)
        entry_titulo.delete(0, tk.END)
        entry_descripcion.delete(0, tk.END)
        urgente.set(False)
        actualizar_lista()

    except Exception as e:
        messagebox.showerror('Error', str(e))


def marcar_completada():
    try:
        seleccion = lista.curselection()

        if not seleccion:
            raise ValueError('Debe seleccionar una tarea.')

        gestor.marcar_completada(seleccion[0])
        actualizar_lista()

    except Exception as e:
        messagebox.showerror('Error', str(e))


def eliminar_tarea():
    try:
        seleccion = lista.curselection()

        if not seleccion:
            raise ValueError('Debe seleccionar una tarea.')

        gestor.eliminar_tarea(seleccion[0])
        actualizar_lista()

    except Exception as e:
        messagebox.showerror('Error', str(e))


ventana = tk.Tk()
ventana.title('Gestor de Tareas')
ventana.geometry('800x500')

tk.Label(ventana, text='Titulo').pack()
entry_titulo = tk.Entry(ventana, width=50)
entry_titulo.pack()

tk.Label(ventana, text='Descripcion').pack()
entry_descripcion = tk.Entry(ventana, width=50)
entry_descripcion.pack()

urgente = tk.BooleanVar()
tk.Checkbutton(ventana, text='Tarea urgente', variable=urgente).pack(pady=5)

lista = tk.Listbox(ventana, width=120, height=15)
lista.pack(pady=10)

tk.Button(ventana, text='Agregar tarea', command=agregar_tarea).pack(pady=3)
tk.Button(ventana, text='Marcar como completada', command=marcar_completada).pack(pady=3)
tk.Button(ventana, text='Eliminar tarea', command=eliminar_tarea).pack(pady=3)

actualizar_lista()
ventana.mainloop()

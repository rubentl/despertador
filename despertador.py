#! /usr/bin/env python3
# -*- coding: utf-8 -*-

'''Básicamente se trata de despertar el ordenador a una hora y que suene
tu música favorita, usando el programa rtcwake y smplayer'''

import tkinter.ttk as ttk
import tkinter as tk
from tkinter.filedialog import FileDialog
import plastik_theme
# import sys
import os
import re
import datetime as dt
from lenguaje import _

# Expresión regular para 1d5h23m.
re_intervalo = r"""(?:(?P<d>[0-9]+)d){0,1}(?:(?P<h>[0-2]*[0-9])h){0,1}(?:(?P<m>[0-5]*[0-9])m){0,1}"""

# Expresión regular para hora y fecha: 22:45 19/01/2013
re_hora_dia = r"""(?P<hora>([01][0-9]|2[0-3])):(?P<minuto>[0-5][0-9]) +(?P<dia>(0[1-9]|[12][0-9]|3[01]))(/|-)(?P<mes>(0[1-9]|1[12]))(/|-)(?P<anio>[12][0-9]{3})"""

rtcwake = 'gksudo "rtcwake -m mem -s {0}"'
reproductor = 'mplayer {0}'

# Pon aquí tu música predeterminada
comandos = ('',)


class Despertador:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title(_('Despertador'))
        self.root.geometry('474x163+230+129')
        # cargar el tema visual
        plastik_theme.install('tile-themes/plastik/plastik')
        style = ttk.Style()
        theme = style.theme_use()
        default = style.lookup(theme, 'background')
        self.root.configure(background=default)
        self.root.resizable(width=False, height=False)
        self.root.bind('<Escape>', self.root.quit)
        self.root.protocol('WM_DELETE_WINDOW', self.root.quit)
        self.combobox = tk.StringVar()
        self.combobox.set(comandos[0])
        self.entry = tk.StringVar()
        self.ayuda()

        self.tLa34 = ttk.Labelframe(self.root)
        self.tLa34.place(relx=0.06, rely=0.06, relheight=0.4, relwidth=0.66)
        self.tLa34.configure(text=_("Tiempo"))
        self.tLa34.configure(width="315")
        self.tLa34.configure(height="65")

        self.hora = ttk.Entry(self.tLa34)
        self.hora.place(relx=0.16, rely=0.36, relheight=0.42, relwidth=0.68)

        self.hora.configure(takefocus="")
        self.hora.configure(textvariable=self.entry)
        self.hora.configure(width="214")
        self.hora.configure(cursor="xterm")

        self.tLa36 = ttk.Labelframe(self.root)
        self.tLa36.place(relx=0.06, rely=0.49, relheight=0.4, relwidth=0.91)
        self.tLa36.configure(text=_("Archivo a reproducir"))

        self.ButFile = ttk.Button(self.tLa36)
        self.ButFile.place(relx=0.82, rely=0.32, relheight=0.5, relwidth=0.15)
        self.ButFile.configure(takefocus="")
        self.ButFile.configure(command=self.archivo)
        self.ButFile.configure(text="...")

        self.comando = ttk.Combobox(self.tLa36)
        self.comando.place(relx=0.05, rely=0.36, relheight=0.42, relwidth=0.7)
        self.comando.configure(height="19")
        self.comando.configure(takefocus="")
        self.comando.configure(textvariable=self.combobox)
        self.comando.configure(values=comandos)
        self.comando.configure(width="217")

        self.tBu38 = ttk.Button(self.root)
        self.tBu38.place(relx=0.78, rely=0.1)
        self.tBu38.configure(takefocus="")
        self.tBu38.configure(command=self.aceptar)
        self.tBu38.configure(text=_("Aceptar"))

        self.cpd39 = ttk.Button(self.root)
        self.cpd39.place(relx=0.78, rely=0.3)
        self.cpd39.configure(takefocus="")
        self.cpd39.configure(command=self.cancelar)
        self.cpd39.configure(text=_("Cancelar"))

    def cancelar(self):
        self.root.quit()

    def ayuda(self):
        self.entry.set(_('ejemplo: 1d5h23m ó 14:45 12/02/2013'))

    def aceptar(self):
        segundos = None
        if self.entry.get() != '':
            match_interval = re.search(re_intervalo, self.entry.get())
            dia = match_interval.group('d')  # día
            hora = match_interval.group('h')  # hora
            minuto = match_interval.group('m')  # minuto
            dia = int(dia) if dia is not None else 0
            hora = int(hora) if hora is not None else 0
            minuto = int(minuto) if minuto is not None else 0
            segundos = dt.timedelta(days=dia, hours=hora, minutes=minuto)
            if segundos.total_seconds() != 0:
                self.ejecutar(segundos)
                return
            else:
                match_fecha = re.search(re_hora_dia, self.entry.get())
                hora = match_fecha.group('hora')  # hora
                minuto = match_fecha.group('minuto')  # minuto
                dia = match_fecha.group('dia')
                mes = match_fecha.group('mes')
                anio = match_fecha.group('anio')
                hora = int(hora) if hora is not None else 0
                minuto = int(minuto) if minuto is not None else 0
                dia = int(dia) if dia is not None else 0
                mes = int(mes) if mes is not None else 0
                anio = int(anio) if anio is not None else 0
                segundos = dt.datetime(
                    anio, mes, dia, hora, minuto) - dt.datetime.now()
                self.ejecutar(segundos)
                return
        else:
            self.ayuda()

    def ejecutar(self, segundos):
        if segundos is not None:
            if segundos.total_seconds() < 0:
                self.entry.set(_('La hora solicitada está pasada.'))
            else:
                os.system(';'.join((rtcwake.format(segundos.seconds),
                                   reproductor.format(self.combobox.get()))))
                self.root.quit()
        else:
            self.ayuda()

    def archivo(self):
        dialogo = FileDialog(self.root)
        # directorio inicial de la música
        fname = dialogo.go(dir_or_file='/home/ruben/Música')
        if fname is None:
            return
        else:
            lista = list(self.comando['values'])
            lista.append(fname)
            self.comando['values'] = tuple(lista)
            self.combobox.set(fname)


if __name__ == '__main__':
    ventana = Despertador()
    ventana.hora.focus_set()
    ventana.root.mainloop()

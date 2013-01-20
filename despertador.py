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
re_str = r"""^(?:(?P<d>[0-9]+)d){0,1}(?:(?P<h>[0-2]*[0-9])h){0,1}(?:(?P<m>[0-5]*[0-9])m){0,1}$"""

# Expresión regular para hora y fecha: 22:45 19/01/2013
re_str_hora = r"""^(?:(?P<h>[0-2]*[0-9]):?)(?:(?P<m>[0-5]*[0-9])?) +(?:(?P<dia>[0-3]*[0-9]):?)[/,-](?:(?P<mes>[0-1]*[0-2]):?)[/,-](?:(?P<ano>20[1-9][0-9]):?)$"""

rtcwake = 'gksudo "rtcwake -m mem -s {0}";'
reproductor = 'smplayer {0}'


class Despertador:
    def __init__(self, master=None):
        style = ttk.Style()
        theme = style.theme_use()
        default = style.lookup(theme, 'background')
        master.configure(background=default)
        master.bind('<Escape>', master.quit)
        master.protocol('WM_DELETE_WINDOW', master.quit)

        self.tLa34 = ttk.Labelframe(master)
        self.tLa34.place(relx=0.06, rely=0.06, relheight=0.4, relwidth=0.66)
        self.tLa34.configure(text=_("Tiempo"))
        self.tLa34.configure(width="315")
        self.tLa34.configure(height="65")

        self.hora = ttk.Entry(self.tLa34)
        self.hora.place(relx=0.16, rely=0.36, relheight=0.42, relwidth=0.68)

        self.hora.configure(takefocus="")
        self.hora.configure(textvariable=entry)
        self.hora.configure(width="214")
        self.hora.configure(cursor="xterm")

        self.tLa36 = ttk.Labelframe(master)
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
        self.comando.configure(textvariable=combobox)
        self.comando.configure(values=comandos)
        self.comando.configure(width="217")

        self.tBu38 = ttk.Button(master)
        self.tBu38.place(relx=0.78, rely=0.1)
        self.tBu38.configure(takefocus="")
        self.tBu38.configure(command=self.aceptar)
        self.tBu38.configure(text=_("Aceptar"))

        self.cpd39 = ttk.Button(master)
        self.cpd39.place(relx=0.78, rely=0.3)
        self.cpd39.configure(takefocus="")
        self.cpd39.configure(command=self.cancelar)
        self.cpd39.configure(text=_("Cancelar"))

    def cancelar(self):
        root.quit()

    def aceptar(self):
        def ayuda():
            entry.set(_('ejemplo de uso: 1d5h23m o 14:45 12/02/2013'))
        hora = entry.get()
        segundos = None
        if (hora != ''):
            comando = combobox.get()
            match_obj = re.search(re_str, hora)
            if (match_obj is not None):  # un intervalo
                d = match_obj.group('d')  # día
                h = match_obj.group('h')  # hora
                m = match_obj.group('m')  # minuto
                if (d is not None):
                    d = int(d)
                else:
                    d = 0
                if (h is not None):
                    h = int(h)
                else:
                    h = 0
                if (m is not None):
                    m = int(m)
                else:
                    m = 0
                segundos = dt.timedelta(days=d, hours=h, minutes=m)
            else:
                match_obj = re.search(re_str_hora, hora)
                if (match_obj is not None):  # a una hora concreta
                    h = match_obj.group('h')  # hora
                    m = match_obj.group('m')  # minuto
                    dia = match_obj.group('dia')
                    mes = match_obj.group('mes')
                    ano = match_obj.group('ano')
                    if (h is not None):
                        h = int(h)
                    else:
                        h = 0
                    if (m is not None):
                        m = int(m)
                    else:
                        m = 0
                    if (dia is not None):
                        dia = int(dia)
                    else:
                        dia = 0
                    if (mes is not None):
                        mes = int(mes)
                    else:
                        mes = 0
                    if (ano is not None):
                        ano = int(ano)
                    else:
                        ano = 0
                    segundos = dt.datetime(ano, mes, dia, h, m) - dt.datetime.now()
                else:
                    ayuda()
        else:
            ayuda()
        if (segundos is not None):
            if (segundos.total_seconds() < 0):
                entry.set(_('La hora solicitada está pasada.'))
            else:
                os.system(''.join((rtcwake.format(segundos.total_seconds()),
                                   reproductor.format(comando))))
                root.quit()

    def archivo(self):
        d = FileDialog(root)
        # directorio inicial de la música
        fname = d.go(dir_or_file='/home/ruben/Música')
        if fname is None:
            return
        else:
            lista = list(comandos)
            lista.append(fname)
            w.comando['values'] = lista
            combobox.set(fname)


if __name__ == '__main__':
    global val, w, root
    root = tk.Tk()
    root.title(_('Despertador'))
    root.geometry('474x163+230+129')
    # cargar el tema visual
    plastik_theme.install('tile-themes/plastik/plastik')
    combobox = tk.StringVar()
    entry = tk.StringVar()
    # se pueden poner archivos de música predeterminados
    comandos = ()
    # combobox.set(comandos[0])  #descomentar esta línea si comandos != ()
    w = Despertador(root)
    w.hora.focus_set()
    root.mainloop()

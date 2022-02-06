import hashlib
import requests
import pandas as pd
import time
import tkinter as tk
import sqlite3
from pandastable import Table, TableModel

class Tareas:
    
    def encriptar_sha1(self, key):
        sha1 = hashlib.sha1()
        sha1.update(key.encode('utf-8'))
        return sha1.hexdigest()

    def countries_service(self):
        print("Solicitando Lenguajes......")
        url = 'https://restcountries.com/v2/all'
        data = requests.get(url)
        data = data.json()
        return data

    def languages_to_string(self, langs):
        l_text = ''
        for l in langs:
            l_text += l['name'] + ','
        return l_text[:-1]       

    def fill_dataframe(self, c):
        print("Llenando Dataframe con Data......")
        pd.set_option('display.width',800)
        df_countries = pd.DataFrame()
        df_countries.style.set_table_styles([{'selector': '',
                                            'props':[('border','2px solid green')]
                                            }])
        
        for country in c:
            start = time.perf_counter_ns()
            df_countries = df_countries.append(
                {
                    'Region': country['region'],
                    'City_Name': (country['name'][:40]+'..') if len(country['name'])>40 else country['name'],
                    'Language': self.encriptar_sha1(key = self.languages_to_string(country['languages'])),
                    'Time': (time.perf_counter_ns() - start) / 1000000
                }, ignore_index=True
            )
        
        return df_countries

    def store_db(self, df : pd.DataFrame):
        print("Creando Base de Datos......")
        con = sqlite3.connect('generate/dataframe_test.db')
        print("Llenando Base de Datos de Paises......")
        df.to_sql('countries', con, if_exists='replace', index=False)
        print("Llenando Tabla de Resultado de Funciones de Panda......")
        sql_table = "create table results( \
                tiempo_total text, \
                tiempo_promedio text, \
                tiempo_maximo text, \
                tiempo_minimo text \
            )"
        try:
            con.execute(sql_table)
            sql_insert = "insert into results(tiempo_total, \
                tiempo_promedio, tiempo_maximo, tiempo_minimo) \
                values (?,?,?,?)"
            con.execute(sql_insert, (df['Time'].sum(),df['Time'].mean(),
                    df['Time'].min(), df['Time'].max()))
            con.commit()        
        except sqlite3.OperationalError:
            con.execute("""DELETE FROM results""")
        cursor = con.execute("select * from results")
        for c in cursor:
            print(c)    
        con.close()    

        
    def dataframe_to_json(self, df : pd.DataFrame):
        print("Guardando en archivo JSON la Data......")
        df.to_json('generate/df_to_json.json', orient = 'records')     

    def show_data(self, df : pd.DataFrame):
        print("Mostra en pantalla la Data......")
        root = tk.Tk()
        root.geometry('900x600')
        data_pandas = u'Tiempo total: {}  |  Tiempo Promedio: {}  |  ' \
            u'Tiempo Minimo: {}  |  Tiempo Maximo: {}'.format(
                    df['Time'].sum(),
                    df['Time'].mean(),
                    df['Time'].min(),
                    df['Time'].max()
                )
        tk.Label(root, text='Prueba Python ZINOBE - Urley Said Rey Velandia',
                font = ('Helvetica', 14, 'bold'),
                ).pack()        
        tk.Label(root, text=data_pandas,
                font = ('Helvetica', 10),
                anchor='e',
                justify = tk.LEFT).pack()
        
        table = DataFrameTable(root, df)
        root.mainloop()    


class DataFrameTable(tk.Frame):
    def __init__(self, parent=None, df=pd.DataFrame()):
        super().__init__()
        self.parent = parent
        self.pack(fill=tk.BOTH, expand=True)
        self.table = Table(
            self, dataframe=df,
            showtoolbar=False,
            showstatusbar=True,
            editable=False)
        self.table.show()
                
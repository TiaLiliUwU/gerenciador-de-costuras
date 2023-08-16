import sqlite3
from datetime import datetime

class GetDds:

    @staticmethod
    def get_dds():
        
        conexao = sqlite3.connect('remessas.db')
        cursor = conexao.cursor()
        cursor.execute('SELECT data FROM quantidades')
        data = [data[0] for data in cursor.fetchall()][-1]
        cursor.execute('SELECT quantidade FROM quantidades')
        quantidade = [quantidade[0] for quantidade in cursor.fetchall()][-1]
        conexao.close()

        conexao = sqlite3.connect('feitas.db')
        cursor = conexao.cursor()
        cursor.execute('SELECT quantidade FROM quantidades WHERE prof = ?', ("Lucia",))
        acumuladas_lucia = [quantidade[0] for quantidade in cursor.fetchall()][-1]
        cursor.execute('SELECT quantidade FROM quantidades WHERE prof = ?', ("Mimus",))
        acumuladas_mimus = [quantidade[0] for quantidade in cursor.fetchall()][-1]
        conexao.close()

        conexao = sqlite3.connect('dinheiro.db')
        cursor = conexao.cursor()

        lucro_lucia = 0
        lucro_mimus = 0
        prof = ['Lucia', 'Mimus']
        for nome in prof:
            cursor.execute('SELECT dinheiro FROM valor WHERE prof = ?', (nome,))
            din = [dinheiro[0] for dinheiro in cursor.fetchall()]
            if nome == 'Lucia':
                if din:
                    lucro_lucia = din[-1]
            else:
                if din:
                    lucro_mimus = din[-1]

        conexao.close()

        return data, quantidade, acumuladas_lucia, acumuladas_mimus, lucro_lucia, lucro_mimus

class Feitas:

    @staticmethod
    def create():

        conexao = sqlite3.connect('feitas.db')
        cursor = conexao.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS quantidades (
                id INTEGER PRIMARY KEY,
                data TEXT,
                prof TEXT,
                quantidade INTEGER
            )
        ''')

        conexao.commit()
        conexao.close()
    
    @staticmethod
    def write_feitas(quant, data, prof):

        Feitas.create()

        conexao = sqlite3.connect('feitas.db')
        cursor = conexao.cursor()

        cursor.execute('SELECT quantidade FROM quantidades WHERE prof = ?', (prof,))
        quantidade = [quantidade[0] for quantidade in cursor.fetchall()]
        if quantidade and quant > 0:
            quant = quantidade[-1] + quant

        cursor.execute('INSERT INTO quantidades (data, prof, quantidade) VALUES (?, ?, ?)', (data, prof, quant))

        conexao.commit()
        conexao.close()

class Remessas:
    
    @staticmethod
    def create():

        conexao = sqlite3.connect('remessas.db')
        cursor = conexao.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS quantidades (
                id INTEGER PRIMARY KEY,
                data TEXT,
                quantidade INTEGER
            )
        ''')

        conexao.commit()
        conexao.close()

    @staticmethod
    def write_remessas(quant, data):

        Remessas.create()

        conexao = sqlite3.connect('remessas.db')
        cursor = conexao.cursor()

        cursor.execute('INSERT INTO quantidades (data, quantidade) VALUES (?, ?)', (data, quant))

        conexao.commit()
        conexao.close()

class Dinheiro:

    @staticmethod
    def create():

        conexao = sqlite3.connect('dinheiro.db')
        cursor = conexao.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS valor (
                id INTEGER PRIMARY KEY,
                prof TEXT,
                data TEXT,
                dinheiro INTEGER
            )
        ''')

        conexao.commit()
        conexao.close()

    @staticmethod
    def write_receber(data, prof, dinheiro, pag):

        Dinheiro.create()

        conexao = sqlite3.connect('dinheiro.db')
        cursor = conexao.cursor()

        cursor.execute('SELECT dinheiro FROM valor WHERE prof = ?', (prof,))
        din = [dinheiro[0] for dinheiro in cursor.fetchall()]
        if din:
            dinheiro = din[-1] + dinheiro - pag

        cursor.execute('INSERT INTO valor (prof, data, dinheiro) VALUES (?, ?, ?)', (prof, data, dinheiro))

        conexao.commit()
        conexao.close()
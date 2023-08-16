from cc import CustomConsole as cc
import questionary
import ntplib
from tqdm import tqdm
from datetime import datetime
import time as t
import pytz
from banco import Remessas as r, Feitas as f, GetDds as g, Dinheiro as p

class GetDate():

    @staticmethod
    def get_date():

        op_data = [
        {"name": "Sim", "value": "1"},
        {"name": "Não", "value": "2"},
        ]

        op_cad_data = int(questionary.select("Deseja cadastrar a data de hoje? \n", choices=op_data, instruction=' ', qmark='*').ask())

        if op_cad_data == 1:
            ntp_server = 'pool.ntp.org'   
            fuso_horario_sp = pytz.timezone('America/Sao_Paulo')
            client = ntplib.NTPClient()

            while True:
                try:
                    response = client.request(ntp_server, version=3)
                except:
                    print("Não conseguimos conectar ao servidor de data, aguarde")
                    with tqdm(total=60, desc='Aguardando', unit='s') as progress_bar:
                        for _ in range(60):
                            t.sleep(1)
                            progress_bar.update(1)
                    print('Tentando reconectar')   
                break
            
            cc.clear()
            ntp_time = datetime.fromtimestamp(response.tx_time, tz=fuso_horario_sp)

            data = ntp_time.strftime('%d/%m/%Y')
        
        elif op_cad_data == 2:
            data = input('Digite a data a ser cadastrada (DD/MM/AAAA): ')
        
        cc.clear()
        return data

class Menu():

    quant = ''
    data = ''
    prof = ['Lucia', 'Mimus']

    @staticmethod
    def stats():

        cc.clear()

        dds = g.get_dds()
        ult_remessa, quant_remessa, quant_lucia, quant_mimus, lucro_lucia, lucro_mimus = dds
        quant_restante = quant_remessa - (quant_lucia + quant_mimus)

        print('*** Estatísticas ***\n')
        print(f'Remessa do dia {ult_remessa}: {quant_remessa} costuras.\n')
        print(f'Foram feitas {quant_lucia + quant_mimus} costuras')
        print(f'Restam {quant_restante} costuras.\n')
        print(f'Costuras feitas por Lucia: {quant_lucia}')
        print(f'Costuras feitas por Mimus: {quant_mimus}\n')
        print(f'Dinheiro a receber por Lucia: R$ {lucro_lucia}')
        print(f'Dinheiro a receber por Mimus: R$ {lucro_mimus}')

        cc.enter()

    @staticmethod
    def cad_pag():

        cc.clear()

        print('***Cadastro de pagamentos***\n')
        dds = g.get_dds()
        receber_lucia = dds[4]
        receber_mimus = dds[5]

        print(f'Lucia tem R$ {receber_lucia} a receber.')
        print(f'Mimus tem R$ {receber_mimus} a receber.\n')

        data = GetDate.get_date()
        print('***Cadastro de pagamentos***\n')
        print(f'Data cadastrada: {data}')

        for nome in Menu.prof:

            pag = int(input(f'Digite o valor do pagamento de {nome}: R$ '))
            p.write_receber(data, nome, 0, pag)

        print('\nPagamentos cadastrados com sucesso!')
        cc.enter()



    @staticmethod
    def cad_remessa():

        op_cad = [
        {"name": "Sim", "value": "0"},
        {"name": "Não", "value": "1"},
        ]
            
        cc.clear()
        print('***Cadastro de remessas***\n')

        data = GetDate.get_date()
        print('***Cadastro de remessas***\n')
        print(f'Data cadastrada: {data}')

        Menu.quant = int(input(f'\nDigite o número de costuras pegas no dia {data}: '))
        Menu.data = data

        op_reset = int(questionary.select("\nTem certeza que deseja continuar? Isso irá zerar as costuras feitas... \n", choices=op_cad, instruction=' ', qmark='*').ask())
        if op_reset == 0:
            r.write_remessas(Menu.quant, Menu.data)
            for prof in Menu.prof: 
                f.write_feitas(0, Menu.data, prof)
            print(f'\nForam cadastradas {Menu.quant} novas costuras no dia {Menu.data}.\nBom trabalho :)')
        else:
            print('\nNão Foram cadastradas nenhuma nova remessa.\nBom trabalho :)')
        cc.enter()

    @staticmethod
    def cad_cost():

        op_prof = [
        {"name": "Lucia", "value": "0"},
        {"name": "Mimus", "value": "1"},
        ]
        
        cc.clear()
        print('*** Cadastro de costuras ***\n')
        data = GetDate.get_date()
        print('*** Cadastro de costuras ***\n')
        print(f'Data cadastrada: {data}')

        op_cad_prof = int(questionary.select("Qual costureiro deseja cadastrar? \n", choices=op_prof, instruction=' ', qmark='*').ask())
        prof = Menu.prof[op_cad_prof]

        Menu.quant = int(input(f'\n>>> Cadastre as costuras feitas por {prof} em {data}: '))
        Menu.data = data

        f.write_feitas(Menu.quant, Menu.data, prof)
        p.write_receber(Menu.data, prof, (Menu.quant * 0.5), 0)

        print(f'\n{prof} fez {Menu.quant} costuras no dia {Menu.data}.\nParabéns :)')
        cc.enter()
    
    @staticmethod
    def menu_principal():

        opcoes = [
        {"name": "Cadastrar costuras", "value": "1"},
        {"name": "Cadastrar remessas", "value": "2"},
        {"name": "Cadastrar pagamentos", "value": "3"},
        {"name": "Estatísticas", "value": "4"},
        {"name": "Sair", "value": '5'},
        ]

        while True:
            cc.clear()
            print('*** Gerenciador de costura ***\n')   
            op = int(questionary.select("O que deseja fazer? \n", choices=opcoes, instruction=' ', qmark='*').ask())
            if op == 1:
                Menu.cad_cost()
            elif op == 2:
                Menu.cad_remessa()
            elif op == 3:
                Menu.cad_pag()
            elif op == 4:
                Menu.stats()
            elif op == 5:
                cc.clear()
                break

cc.clear()

Menu.menu_principal()
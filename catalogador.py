from datetime import datetime, timedelta
import enum
import time
import random
import telebot
import iqoptionAccount
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from iqoptionapi.stable_api import IQ_Option
import horarios as HorariosDoBot
import mensagens
import pandas as pd
import numpy as np
import mplfinance as mpl
import secrets
import os
from colorama import Fore, init
import pymongo
init(autoreset=True, convert=True)

# $ COMMAND TELEGRAM(/machinelearning): Gerar Gráfico CandlesTick
def grafico_candlestick(telegram, velas, titulo, subtitulo):
    for vela in velas:
        print(datetime.fromtimestamp(vela['from']).strftime(
            '%d/%m/%Y %H:%M:%S'), 'max: {}'.format(vela['max']), 'min: {}'.format(vela['min']))

    data = {'open': [],
            'close': [],
            'high': [],
            'low': [],
            'volume': []}
    data_range = []

    for vela in velas:
        data['open'].append(vela['open'])
        data['close'].append(vela['close'])
        data['high'].append(vela['max'])
        data['low'].append(vela['min'])
        data['volume'].append(vela['volume'])
        data_range.append(datetime.fromtimestamp(
            vela['from']).strftime('%d/%m/%Y %H:%M:%S'))

    # create DataFrame
    prices = pd.DataFrame(data,
                          index=data_range)

    """"""
    # display DataFrame
    prices.index = pd.DatetimeIndex(prices.index)

    # $ Markup
    signal = [np.nan for i in range(len(velas)-1)]
    signal.append(velas[-1]['min']-0.00008 if velas[-1]['open'] < velas[-1]['close'] else velas[-1]
                  ['max']+0.00008 if velas[-1]['open'] > velas[-1]['close'] else velas[-1]['max']+0.00008)
    apd = mpl.make_addplot(signal, type='scatter', markersize=100, marker='^' if velas[-1]['open'] < velas[-1]['close'] else 'v' if velas[-1]['open'] > velas[-1]
                           ['close'] else '.', color='#19b76f' if velas[-1]['open'] < velas[-1]['close'] else '#fd4446' if velas[-1]['open'] > velas[-1]['close'] else 'gray')

    # $ create fig
    fig, axlist = mpl.plot(
        prices,
        type="candle",
        title=titulo,
        ylabel='',
        ylabel_lower='',
        volume=True,
        style="yahoo",
        returnfig=True,
        datetime_format='%H:%M:%S',
        addplot=apd
    )

    # add a new suptitle
    fig.suptitle(titulo, y=1.05, fontsize=20, fontfamily='Arial', x=0.59)

    # add a title the the correct axes
    # print('\n\nSUBTITULO[Candlestick]:',subtitulo,'\n\n')
    axlist[0].set_title(subtitulo, fontsize=15,
                        fontfamily='Arial', loc='center')

    # annoted

    # save the figure
    nome_da_imagem = str(telegram['id'])+'-token-'+secrets.token_hex(25)
    while True:
        if os.path.isfile('machinelearning/temporary images/{}.png'.format(nome_da_imagem)):
            nome_da_imagem = str(telegram['id']) + \
                '-token-'+secrets.token_hex(25)
        else:
            break

    fig.savefig(
        'machinelearning/temporary images/{}.png'.format(nome_da_imagem), bbox_inches='tight')
    return nome_da_imagem+'.png'


# $ CODDING: </Class "Catalogador de Operações Pra Iq Option">
class Catalogador:
    def __init__(self, botManager): 
        self.botManager = botManager
        self.api_iqoption = botManager.api_iqoption
        self.api_telegram = botManager.api_telegram
        self.wins = 0
        self.losses = 0
        self.lista_de_imagens = []

    
    def verificarConexaoDaIqOption(self):
        if not self.api_iqoption.check_connect():
            self.api_iqoption = self.botManager.reconectar_iqoption() 

    


    # gerar configurações
    def definir_configuracoes_automaticas_para_operacoes_rapidas(self,configuracoes, timeframe=None):
        """
        Função Responsavel por definir configurações da machine learning automaticamente(tipo de catalogação, timeframe...)
        """
        configuracoes["tipo de catalogação"] = "agressivo"
        configuracoes["timeframe"] = random.choice(
            ['1 minuto', '5 minutos', '15 minutos']) if timeframe is None else timeframe
        configuracoes["periodo de catalogação em dias"] = random.choice(
            ['5 dias', '6 dias', '7 dias', '8 dias', '9 dias', '10 dias'])
        configuracoes["martingale"] = random.choice(
            ['1 martingale', '2 martingale', ''])
        configuracoes["porcentagem de assertividade(nenhum martingale)"] = random.choice(
            ['90%', '91%', '92%', '93%', '94%', '95%', '96%', '97%', '98%', '99%', '100%'])
        configuracoes["porcentagem de assertividade(1 martingale)"] = random.choice([
            '60%', '70%', '80%'])
        configuracoes["porcentagem de assertividade(2 martingale)"] = configuracoes[
            "porcentagem de assertividade(1 martingale)"]
        configuracoes['quantidade de operações que a Machine Learning ira filtrar'] = 20
        return configuracoes

    def checar_placar_pra_reinicar_as_meia_noite(self):
        global WINS, LOSSES

   
    def filtrar_operacoes(self, catalogacao, configuracoes, quantidade_de_operacoes):
        """

            "tipo de catalogação":"",
            "periodo de catalogação em dias":"",
            "timeframe":"",
            "martingale":"",
            "porcentagem de assertividade(nenhum martingale)":"",
            "porcentagem de assertividade(1 martingale)":"",
            "porcentagem de assertividade(2 martingale)":"",
            "quantidade de operações que a machine learning ira filtrar":""

        """
        periodo_em_minutos = 120  # $ "tipo de catalogação":"agressivo",
        logging_operacoes_filtradas = ''
        lista = []
        for par in catalogacao:
            for horario in sorted(catalogacao[par]):
                if configuracoes['tipo de catalogação'].lower() == 'normal':
                    if configuracoes['martingale'] == '':
                        if catalogacao[par][horario]['%'] >= int(configuracoes['porcentagem de assertividade(nenhum martingale)'].replace('%', '')) and datetime.strptime(datetime.fromtimestamp(datetime.utcnow().timestamp() - 10800).strftime('%d/%m/%Y')+' {}:00'.format(horario), '%d/%m/%Y %H:%M:%S') > datetime.fromtimestamp(datetime.utcnow().timestamp() - 10800):
                            # if datetime.strptime(datetime.fromtimestamp(datetime.utcnow().timestamp() - 10800).strftime('%d/%m/%Y ')+' {}:00'.format(horario),'%d/%m/%Y %H:%M:%S') > datetime.fromtimestamp(datetime.utcnow().timestamp() - 10800):
                            lista.append(
                                {par: {horario: catalogacao[par][horario]}})
                            logging_operacoes_filtradas += '{}, {}%, M{}, {}\n'.format(
                                par, horario, catalogacao[par][horario]['%'], configuracoes['timeframe'].split(' ')[0].strip(), catalogacao[par][horario]['dir'])
                            # print(par, horario, str(catalogacao[par][horario]['%'])+'%')
                    if configuracoes['martingale'] == '1 martingale':
                        if catalogacao[par][horario]['%'] >= int(configuracoes['porcentagem de assertividade(nenhum martingale)'].replace('%', '')) and catalogacao[par][horario]['mg1']['%'] >= int(configuracoes['porcentagem de assertividade(1 martingale)'].replace('%', '')) and datetime.strptime(datetime.fromtimestamp(datetime.utcnow().timestamp() - 10800).strftime('%d/%m/%Y')+' {}:00'.format(horario), '%d/%m/%Y %H:%M:%S') > datetime.fromtimestamp(datetime.utcnow().timestamp() - 10800):
                            # if datetime.strptime(datetime.fromtimestamp(datetime.utcnow().timestamp() - 10800).strftime('%d/%m/%Y ')+' {}:00'.format(horario),'%d/%m/%Y %H:%M:%S') > datetime.fromtimestamp(datetime.utcnow().timestamp() - 10800):
                            lista.append(
                                {par: {horario: catalogacao[par][horario]}})
                            logging_operacoes_filtradas += '{}, {}%, {}%, M{}, {}\n'.format(
                                par, horario, catalogacao[par][horario]['%'], catalogacao[par][horario]['mg1']['%'], configuracoes['timeframe'].split(' ')[0].strip(), catalogacao[par][horario]['dir'])
                            # print(par, horario, str(catalogacao[par][horario]['%'])+'%', str(catalogacao[par][horario]['mg1']['%'])+'%')
                    if configuracoes['martingale'] == '2 martingale':
                        if catalogacao[par][horario]['%'] >= int(configuracoes['porcentagem de assertividade(nenhum martingale)'].replace('%', '')) and catalogacao[par][horario]['mg1']['%'] >= int(configuracoes['porcentagem de assertividade(1 martingale)'].replace('%', '')) and catalogacao[par][horario]['mg2']['%'] >= int(configuracoes['porcentagem de assertividade(2 martingale)'].replace('%', '')) and datetime.strptime(datetime.fromtimestamp(datetime.utcnow().timestamp() - 10800).strftime('%d/%m/%Y')+' {}:00'.format(horario), '%d/%m/%Y %H:%M:%S') > datetime.fromtimestamp(datetime.utcnow().timestamp() - 10800):
                            # if datetime.strptime(datetime.fromtimestamp(datetime.utcnow().timestamp() - 10800).strftime('%d/%m/%Y ')+' {}:00'.format(horario),'%d/%m/%Y %H:%M:%S') > datetime.fromtimestamp(datetime.utcnow().timestamp() - 10800):
                            lista.append(
                                {par: {horario: catalogacao[par][horario]}})
                            logging_operacoes_filtradas += '{}, {}%, {}%, {}%, M{}, {}\n'.format(par, horario, catalogacao[par][horario]['%'], catalogacao[par][horario][
                                                                                                'mg1']['%'], catalogacao[par][horario]['mg2']['%'], configuracoes['timeframe'].split(' ')[0].strip(), catalogacao[par][horario]['dir'])
                            # print(par, horario, str(catalogacao[par][horario]['%'])+'%', str(catalogacao[par][horario]['mg1']['%'])+'%', str(catalogacao[par][horario]['mg2']['%'])+'%')
                else:
                    # $ "tipo de catalogação":"agressivo",
                    if configuracoes['martingale'] == '':
                        if catalogacao[par][horario]['%'] >= int(configuracoes['porcentagem de assertividade(nenhum martingale)'].replace('%', '')) and datetime.strptime(datetime.fromtimestamp(datetime.utcnow().timestamp() - 10800).strftime('%d/%m/%Y')+' {}:00'.format(horario), '%d/%m/%Y %H:%M:%S') > datetime.fromtimestamp(datetime.utcnow().timestamp() - 10800) and datetime.strptime(datetime.fromtimestamp(datetime.utcnow().timestamp() - 10800).strftime('%d/%m/%Y')+' {}:00'.format(horario), '%d/%m/%Y %H:%M:%S') < datetime.fromtimestamp(datetime.utcnow().timestamp() - 10800)+timedelta(minutes=periodo_em_minutos):
                            # if datetime.strptime(datetime.fromtimestamp(datetime.utcnow().timestamp() - 10800).strftime('%d/%m/%Y ')+' {}:00'.format(horario),'%d/%m/%Y %H:%M:%S') > datetime.fromtimestamp(datetime.utcnow().timestamp() - 10800):
                            lista.append(
                                {par: {horario: catalogacao[par][horario]}})
                            logging_operacoes_filtradas += '{}, {}%, M{}, {}\n'.format(
                                par, horario, catalogacao[par][horario]['%'], configuracoes['timeframe'].split(' ')[0].strip(), catalogacao[par][horario]['dir'])
                            # print(par, horario, catalogacao[par][horario]['%'])
                    if configuracoes['martingale'] == '1 martingale':
                        if catalogacao[par][horario]['%'] >= int(configuracoes['porcentagem de assertividade(nenhum martingale)'].replace('%', '')) and catalogacao[par][horario]['mg1']['%'] >= int(configuracoes['porcentagem de assertividade(1 martingale)'].replace('%', '')) and datetime.strptime(datetime.fromtimestamp(datetime.utcnow().timestamp() - 10800).strftime('%d/%m/%Y')+' {}:00'.format(horario), '%d/%m/%Y %H:%M:%S') > datetime.fromtimestamp(datetime.utcnow().timestamp() - 10800) and datetime.strptime(datetime.fromtimestamp(datetime.utcnow().timestamp() - 10800).strftime('%d/%m/%Y')+' {}:00'.format(horario), '%d/%m/%Y %H:%M:%S') < datetime.fromtimestamp(datetime.utcnow().timestamp() - 10800)+timedelta(minutes=periodo_em_minutos):
                            # if datetime.strptime(datetime.fromtimestamp(datetime.utcnow().timestamp() - 10800).strftime('%d/%m/%Y ')+' {}:00'.format(horario),'%d/%m/%Y %H:%M:%S') > datetime.fromtimestamp(datetime.utcnow().timestamp() - 10800):
                            lista.append(
                                {par: {horario: catalogacao[par][horario]}})
                            logging_operacoes_filtradas += '{}, {}%, {}%, M{}, {}\n'.format(
                                par, horario, catalogacao[par][horario]['%'], catalogacao[par][horario]['mg1']['%'], configuracoes['timeframe'].split(' ')[0].strip(), catalogacao[par][horario]['dir'])
                            # print(par, horario, catalogacao[par][horario]['%'],catalogacao[par][horario]['mg1']['%'])
                    if configuracoes['martingale'] == '2 martingale':
                        if catalogacao[par][horario]['%'] >= int(configuracoes['porcentagem de assertividade(nenhum martingale)'].replace('%', '')) and catalogacao[par][horario]['mg1']['%'] >= int(configuracoes['porcentagem de assertividade(1 martingale)'].replace('%', '')) and catalogacao[par][horario]['mg2']['%'] >= int(configuracoes['porcentagem de assertividade(2 martingale)'].replace('%', '')) and datetime.strptime(datetime.fromtimestamp(datetime.utcnow().timestamp() - 10800).strftime('%d/%m/%Y')+' {}:00'.format(horario), '%d/%m/%Y %H:%M:%S') > datetime.fromtimestamp(datetime.utcnow().timestamp() - 10800) and datetime.strptime(datetime.fromtimestamp(datetime.utcnow().timestamp() - 10800).strftime('%d/%m/%Y')+' {}:00'.format(horario), '%d/%m/%Y %H:%M:%S') < datetime.fromtimestamp(datetime.utcnow().timestamp() - 10800) + timedelta(minutes=periodo_em_minutos):
                            # if datetime.strptime(datetime.fromtimestamp(datetime.utcnow().timestamp() - 10800).strftime('%d/%m/%Y ')+' {}:00'.format(horario),'%d/%m/%Y %H:%M:%S') > datetime.fromtimestamp(datetime.utcnow().timestamp() - 10800):
                            lista.append(
                                {par: {horario: catalogacao[par][horario]}})
                            logging_operacoes_filtradas += '{}, {}%, {}%, {}%, M{}, {}\n'.format(par, horario, catalogacao[par][horario]['%'], catalogacao[par][horario][
                                                                                                'mg1']['%'], catalogacao[par][horario]['mg2']['%'], configuracoes['timeframe'].split(' ')[0].strip(), catalogacao[par][horario]['dir'])
                            # print(par, horario, catalogacao[par][horario]['%'],catalogacao[par][horario]['mg1']['%'],catalogacao[par][horario]['mg2']['%'])

        # $ Formatação dos Sinais
        # $ {'EURUSD': {'04:01': {'verde': 0, 'vermelha': 10, 'doji': 0, '%': 100, 'dir': 'PUT ', 'mg1': {'verde': 6, 'vermelha': 14, 'doji': 0, '%': 70}}}}

        operacoes_filtradas = {}
        horarios_filtrados = []
        if quantidade_de_operacoes > 50:
            quantidade_de_operacoes = 10

        for index in range(quantidade_de_operacoes):
            if len(lista) == 0:
                # print('Lista zerada, nenhuma operação pra filtrar mais {}'.format(lista))
                break
            # $ Escolher Operação Aleatoria da Lista
            operacao = random.choice(lista)
            # $ Pegar ativo do Dicionario de Operação
            ativo = list(operacao.keys())[0]
            # $ Pegar horario do Dicionario de Operação
            horario = list(operacao[ativo].keys())[0]
            if horario not in horarios_filtrados:
                # $ Adicionar Horario Filtrado
                horarios_filtrados.append(horario)
                # $ Adicionar Operação Filtrada No Dicionario
                operacoes_filtradas[horario] = operacao
                # $ Excluir Operacao Filtrada da Lista
                for index, item in enumerate(lista):
                    if item == operacao:
                        del (lista[index])
            else:
                # $ Excluir Operacao da Lista
                # print('Operação Cancelada({}): {}'.format(horario,operacao))
                for index, item in enumerate(lista):
                    if item == operacao:
                        del (lista[index])

        return operacoes_filtradas

    def cataloga(self, par, dias, timeframe):
        data = []
        datas_testadas = []
        time_ = time.time()
        start_timer = time.time() #$ Contagem de Tempo | Inicio
        sair = False
        while sair == False:
            try:
                velas = self.api_iqoption.get_candles(par, (timeframe * 60), 1000, time_)
            except Exception as erro:
                print(f"{Fore.RED}ocorreu um erro ao tentar buscar candles na Iq Option com get_candles(), verifique sua internet....\n| {erro}{Fore.RESET}")
                raise Exception()
            velas.reverse()
            
            for x in velas:
                if datetime.fromtimestamp(x['from']).strftime('%Y-%m-%d') not in datas_testadas:
                    datas_testadas.append(datetime.fromtimestamp(
                        x['from']).strftime('%Y-%m-%d'))

                if len(datas_testadas) <= dias:
                    x.update({'cor': 'verde' if x['open'] < x['close']
                            else 'vermelha' if x['open'] > x['close'] else 'doji'})
                    data.append(x)
                else:
                    sair = True
                    break
            
            


            time_ = int(velas[-1]['from'] - 1)

        analise = {}
        for velas in data:
            horario = datetime.fromtimestamp(velas['from']).strftime('%H:%M')
            if horario not in analise:
                analise.update(
                    {horario: {'verde': 0, 'vermelha': 0, 'doji': 0, '%': 0, 'dir': ''}})
            analise[horario][velas['cor']] += 1

            try:
                analise[horario]['%'] = round(100 * (analise[horario]['verde'] / (
                    analise[horario]['verde'] + analise[horario]['vermelha'] + analise[horario]['doji'])))
            except:
                pass

        for horario in analise:
            if analise[horario]['%'] > 50:
                analise[horario]['dir'] = 'CALL'
            if analise[horario]['%'] < 50:
                analise[horario]['%'], analise[horario]['dir'] = 100 - \
                    analise[horario]['%'], 'PUT '
                    
                    
        end_timer = time.time() #$ Contagem de Tempo | Final
        
        """
        CODDING: Log
        """
        print(f"{Fore.LIGHTBLACK_EX}[LOG]{Fore.RESET}{Fore.GREEN}[CATALOGAÇÃO]{Fore.RESET} "+"{}{}{} ativo catalogado: {} | {} dias{}(demorou {} segundos){}".format(Fore.LIGHTBLACK_EX,HorariosDoBot.data_hora_weekday_str(),Fore.RESET,par, dias, Fore.LIGHTBLACK_EX,abs(end_timer-start_timer),Fore.RESET))
        return analise

    def catalogar_operacoes_rapidas(self, configuracoes):
        print('valor de self.botManager:', self.botManager)
        print('valor de self.api_iqoption:', self.api_iqoption)
        
        ativos = self.api_iqoption.get_all_open_time()
        start_time_all = time.time()
        print('{}[LOG]{}{}[CATALOGAÇÃO]{} {}{}{} Catalogação iniciada pra filtrar novas operações...'.format(
            Fore.LIGHTBLACK_EX, Fore.RESET,Fore.GREEN, Fore.RESET, Fore.LIGHTBLACK_EX, HorariosDoBot.data_hora_weekday_str(), Fore.RESET))

        catalogacao = {}
        for par in ativos['digital']:
            if ativos['digital'][par]['open'] == True:
                

                timer = int(time.time())
                
                try:
                    catalogacao.update({par: self.cataloga(par, int(configuracoes['periodo de catalogação em dias'].split(' ')[0]), int(configuracoes['timeframe'].split(' ')[0]))})
                except Exception as error:
                    #print(f"@Catalogador | @Function catalogar_operacoes_rapidas(try/catch) | ocorreu um erro ao tentar usar catalogacao.update({...}) | @Error {error}")
                    continue
                    #raise Exception(f"@Catalogador | @Function catalogar_operacoes_rapidas(try/catch) | ocorreu um erro ao tentar usar catalogacao.update({...}) | @Error {error}")

                # print('Depois da catalogação Finalizada do ativo {}'.format(par))

                for par in catalogacao:
                    for horario in sorted(catalogacao[par]):
                        if configuracoes['martingale'].strip() != '':
                            # print(horario)
                            mg_time = horario
                            soma = {'verde': catalogacao[par][horario]['verde'], 'vermelha': catalogacao[par]
                                    [horario]['vermelha'], 'doji': catalogacao[par][horario]['doji']}

                            for i in range(int(configuracoes['martingale'].split(' ')[0])):

                                catalogacao[par][horario].update({'mg'+str(i+1): {'verde': 0, 'vermelha': 0, 'doji': 0, '%': 0}})

                                mg_time = str(datetime.strptime((datetime.now()).strftime('%Y-%m-%d ') + str(
                                    mg_time), '%Y-%m-%d %H:%M') + timedelta(minutes=int(configuracoes['timeframe'].split(' ')[0])))[11:-3]

                                if mg_time in catalogacao[par]:
                                    catalogacao[par][horario]['mg'+str(
                                        i+1)]['verde'] += catalogacao[par][mg_time]['verde'] + soma['verde']
                                    catalogacao[par][horario]['mg'+str(
                                        i+1)]['vermelha'] += catalogacao[par][mg_time]['vermelha'] + soma['vermelha']
                                    catalogacao[par][horario]['mg'+str(
                                        i+1)]['doji'] += catalogacao[par][mg_time]['doji'] + soma['doji']

                                    catalogacao[par][horario]['mg'+str(i+1)]['%'] = round(100 * (catalogacao[par][horario]['mg'+str(i+1)]['verde' if catalogacao[par][horario]['dir'] == 'CALL' else 'vermelha'] / (
                                        catalogacao[par][horario]['mg'+str(i+1)]['verde'] + catalogacao[par][horario]['mg'+str(i+1)]['vermelha'] + catalogacao[par][horario]['mg'+str(i+1)]['doji'])))

                                    soma['verde'] += catalogacao[par][mg_time]['verde']
                                    soma['vermelha'] += catalogacao[par][mg_time]['vermelha']
                                    soma['doji'] += catalogacao[par][mg_time]['doji']
                                else:
                                    catalogacao[par][horario]['mg' +
                                                              str(i+1)]['%'] = 'N/A'

        end_time_all = time.time()

        # $ Filtrar Melhores Operações[Machine Learning]
        dicionario_com_operacoes_filtradas = self.filtrar_operacoes(
            catalogacao,  configuracoes, configuracoes['quantidade de operações que a Machine Learning ira filtrar'])
        print('{}[LOG]{}{}[CATALOGAÇÃO FINALIZADA]{} {}{}{} Catalogação finalizada em todos ativos{}(demorou {} segundos){}'.format(
            Fore.LIGHTBLACK_EX, Fore.RESET,Fore.GREEN, Fore.RESET, Fore.LIGHTBLACK_EX, HorariosDoBot.data_hora_weekday_str(), Fore.RESET, Fore.LIGHTBLACK_EX, abs(end_time_all-start_time_all),Fore.RESET))
        return dicionario_com_operacoes_filtradas

    def checar_ativo_aberto_na_iqoption(self, ativo):
        ativos = self.api_iqoption.get_all_open_time()
        try:
            if ativos['digital'][ativo]['open']:
                return True
            else:
                return False
        except:
            return False

    # $ // Enviar Promoções
    def promocoes(self,client):
        pass

    def monitor_operations(self,api_iqoption, api_telegram, lista_de_grupos, dicionario_com_operacoes_filtradas, configuracoes):
        """
        Função responsavel por Acompanhar, Filtrar e Enviar Operações e Imagens de Marketing para Grupos do Telegram

        exemplo da lista retornada na variavel "dicionario_com_operacoes_filtradas":
            [
                {
                    '23:27': {
                        'EURUSD-OTC': {
                            '23:27': {
                                'verde': 9, 
                                'vermelha': 0, 
                                'doji': 0, 
                                '%': 100, 
                                'dir': 'CALL'
                            }
                        }
                    }
                }, 
                {...}, {...}, ...
            ]

        """
        for index, horario in enumerate(sorted(dicionario_com_operacoes_filtradas)):
            api_hash = "7c2ec86e4a4e393e65fc2e193e50b726"

            self.verificarConexaoDaIqOption()

            
            try:
                """
                CODDING: Definindo informações da operação
                """
                operacao = dicionario_com_operacoes_filtradas[horario] # exemplo de operação: {EURUSD:{"23:27": { ... }}}
                ativo_da_operacao = list(operacao.keys())[0] # exemplo: "EURUSD"
                horario_da_operacao = horario # exemplo: "23:27"
                try:
                    timeframe = int(configuracoes['timeframe'].split(' ')[0]) # exemplo: configuracoes['timeframe'] --> '1 minuto' --> '1 minuto'.split(' ')[0] -> '1' --> int('1') --> 1 
                except Exception as error:
                    timeframe = 1
                direcao = operacao[ativo_da_operacao][horario_da_operacao]['dir'].strip() # exemplo: "put" ou "call"
                
                
                
                """
                CODDING: Log
                """
                print(f"{Fore.GREEN}[OPERAÇÃO]{Fore.RESET} {Fore.LIGHTBLACK_EX}{HorariosDoBot.data_hora_weekday_str()}{Fore.RESET} operação {ativo_da_operacao} {horario_da_operacao} {timeframe}M {direcao}\n")

                if self.checar_ativo_aberto_na_iqoption(ativo_da_operacao):
                    if datetime.strptime(datetime.fromtimestamp(datetime.utcnow().timestamp() - 10800).strftime('%d/%m/%Y ')+horario+':00', '%d/%m/%Y %H:%M:%S') > datetime.fromtimestamp(datetime.utcnow().timestamp() - 10800):
                        cor_da_primeira_vela = None
                        cor_da_segunda_vela = None

                        #$ CODDING: Enviar Mensagem de Aguardando Operação | Grupos do Telegram 
                        for grupo in lista_de_grupos:
                            try:
                                mensagem_aguardando_operacao = mensagens.def_mensagem_de_aguardando_operacao(ativo_da_operacao, horario, timeframe, direcao)
                                mensagem_aguardando_operacao = mensagem_aguardando_operacao
                                self.api_telegram.send_message(grupo, mensagem_aguardando_operacao)
                            except Exception as error:
                                print("{Fore.GREEN}[LOG]{Fore.RESET} @Catalogador | @Function monitor_operations(try/exception) | ocorreu um erro ao tentar enviar a mensagem de aguardando operação {} {} {}M {} | @Error {}".format(ativo_da_operacao, horario, timeframe, direcao, error))


                        while True:
                            timestemp_da_operacao = int(datetime.timestamp(datetime.strptime(datetime.fromtimestamp(
                                datetime.utcnow().timestamp() - 10800).strftime('%d/%m/%Y')+' {}:00'.format(horario), '%d/%m/%Y %H:%M:%S')))
                            if int(datetime.fromtimestamp(datetime.utcnow().timestamp() - 10800).timestamp()) >= timestemp_da_operacao:
                                
                                """
                                CODDING: Enviar Mensagem de Operação Realizada | @TeleBot
                                | Nenhum Martingale
                                """ 
                                for grupo in lista_de_grupos:
                                    try:
                                        self.api_telegram.send_message(grupo, mensagens.def_mensagem_de_operacao_realizada(ativo_da_operacao))
                                    except Exception as error:
                                        print("{Fore.GREEN}[LOG]{Fore.RESET} @Catalogador | @Function monitor_operations(try/exception) | ocorreu um erro ao tentar enviar a mensagem de operação realizada | @Operação {} {} {}M {} | @Error {}".format(ativo_da_operacao, horario, timeframe, direcao, error))

                                resultados = ['Nenhum Martingale', '1° Martingale', '2° Martingale']
                                for i, resultado_atual in enumerate(resultados):
                                    # Espera o tempo apropriado
                                    time.sleep(timeframe * 60)

                                    # Calculando timestamp
                                    timestamp = datetime.timestamp(
                                        datetime.strptime(
                                            datetime.fromtimestamp(datetime.utcnow().timestamp() - 10800)
                                            .strftime('%d/%m/%Y') + ' {}:00'.format(horario_da_operacao),
                                            '%d/%m/%Y %H:%M:%S') + timedelta(minutes=timeframe * i)  # Adiciona o deslocamento do martingale (0, +1min, +2min)
                                    )

                                    # Puxando informações de candlesticks
                                    velas = self.api_iqoption.get_candles(ativo_da_operacao, timeframe * 60, 1, timestamp)

                                    # Verificando o resultado da operação
                                    cor = 'vermelha' if velas[0]['open'] > velas[0]['close'] else 'verde' if velas[0]['open'] < velas[0]['close'] else 'doji'

                                    velas = self.api_iqoption.get_candles(ativo_da_operacao, timeframe*60, 15, timestamp)
                                            
                                    if cor != 'doji':
                                        if (cor == 'vermelha' and direcao == 'PUT') or (cor == 'verde' and direcao == 'CALL'):
                                            resultado = 'win'
                                        elif (cor == 'vermelha' and direcao == 'CALL') or (cor == 'verde' and direcao == 'PUT'):
                                            resultado = 'loss'
                                        else:
                                            resultado = ''

                                        if resultado == 'win':
                                            
                                            # 1. gerar imagem
                                            nome_da_imagem = grafico_candlestick(
                                                telegram={'id': api_hash}, velas=velas, titulo=ativo_da_operacao, subtitulo=f'Win +R$({resultado_atual})')
                                            
                                            # 2. enviando mensagem de win(+R$) com imagem e sticker
                                            for grupo in lista_de_grupos:
                                                try:
                                                    self.api_telegram.send_photo(
                                                        chat_id=grupo, 
                                                        photo=open(f'machinelearning/temporary images/{nome_da_imagem}', 'rb'), 
                                                        caption=mensagens.def_mensagem_de_resultado_da_operacao(ativo_da_operacao, horario_da_operacao, timeframe, direcao, f'<b>Win +R$({resultado_atual})</b>', mensagem_de_promocao='win')
                                                    )

                                                    if resultado_atual == 'Nenhum Martingale':
                                                        sticker_path = 'sticks/win-sem-gale.webp'
                                                    else:  # Para '1° Martingale' ou '2° Martingale'
                                                        sticker_path = 'sticks/win-no-gale.webp'
                                                    self.api_telegram.send_sticker(chat_id=grupo, sticker=open(sticker_path, 'rb'))
                                                except Exception as error:
                                                    print(f"[LOG] @Catalogador | @Function monitor_operations | Erro ao enviar mensagem de win (+R$) | {ativo_da_operacao} {horario_da_operacao} {timeframe}M | Erro: {error}")
                                            
                                            # 3. excluir Imagem
                                            try:
                                                self.lista_de_imagens.append(f'machinelearning/temporary images/{nome_da_imagem}')
                                            except Exception as error:
                                                print(f"[LOG] @Catalogador | @Function monitor_operations | Erro ao adicionar imagem a lista de exclusão | {ativo_da_operacao} {horario_da_operacao} {timeframe}M | Erro: {error}")

                                            # Aguardar 20 segundos
                                            time.sleep(20)

                                            # 4. enviar enquete 
                                            for grupo in lista_de_grupos:
                                                try:
                                                    self.api_telegram.send_poll(
                                                        chat_id=grupo, 
                                                        question="Você pegou esse Win(+R$)?", 
                                                        options=["👍 Sim", "👎 Não"], 
                                                        type="quiz", 
                                                        correct_option_id=0, 
                                                        is_anonymous=False
                                                    )
                                                except Exception as error:
                                                    print(f"[LOG] @Catalogador | @Function monitor_operations | Erro ao enviar enquete | {ativo_da_operacao} {horario_da_operacao} {timeframe}M | Erro: {error}")
                                            
                                            # Aguardar 20 segundos
                                            time.sleep(20)

                                            # 5. atualizar o placar no banco de dados
                                            placar = self.botManager.addWin()
                                            self.wins = placar["wins"]
                                            self.losses = placar["losses"]
                                            
                                            # 6. enviar mensagem do placar
                                            for grupo in lista_de_grupos:
                                                try:
                                                    url = "https://wa.me/5531997711921"
                                                    button_text = "👉 SINAIS VIP"
                                                    markup = InlineKeyboardMarkup()
                                                    button = InlineKeyboardButton(text=button_text, url=url)
                                                    markup.add(button)
                                                    """client.send_message(chat_id=grupo["id do grupo(telegram)"], text=mensagens.def_mensagem_do_placar(WINS, LOSSES), reply_markup=markup)"""
                                                    self.api_telegram.send_message(chat_id=grupo, text=mensagens.def_mensagem_do_placar(self.wins, self.losses), reply_markup=markup)
                                                except Exception as error:
                                                    print(f"[LOG] @Catalogador | @Function monitor_operations | Erro ao enviar placar | {ativo_da_operacao} {horario_da_operacao} {timeframe}M | Erro: {error}")
                                            
                                            
                                            break  # Parar o loop se o resultado for 'win'

                                        elif resultado == 'loss':
                                            # 1. gerar imagem
                                            nome_da_imagem = grafico_candlestick(
                                                telegram={'id': api_hash}, velas=velas, titulo=ativo_da_operacao, subtitulo=f'Loss -R$({resultado_atual})')
                                            
                                            # 2. enviar mensagem de loss(-R$) com a imagem gerada
                                            for grupo in lista_de_grupos:
                                                try:
                                                    if resultado_atual == 'Nenhum Martingale':
                                                        self.api_telegram.send_photo(
                                                            chat_id=grupo, 
                                                            photo=open(f'machinelearning/temporary images/{nome_da_imagem}', 'rb'), 
                                                            caption=mensagens.def_mensagem_de_resultado_da_operacao(ativo_da_operacao, horario_da_operacao, timeframe, direcao, f'<b>Loss -R$({resultado_atual})</b>', aguardando_1_martingale=True)
                                                        )
                                                    elif resultado_atual == '1° Martingale':
                                                        self.api_telegram.send_photo(
                                                            chat_id=grupo, 
                                                            photo=open(f'machinelearning/temporary images/{nome_da_imagem}', 'rb'), 
                                                            caption=mensagens.def_mensagem_de_resultado_da_operacao(ativo_da_operacao, horario_da_operacao, timeframe, direcao, f'<b>Loss -R$({resultado_atual})</b>', aguardando_2_martingale=True)
                                                        )
                                                    else:
                                                        self.api_telegram.send_photo(
                                                            chat_id=grupo, 
                                                            photo=open(f'machinelearning/temporary images/{nome_da_imagem}', 'rb'), 
                                                            caption=mensagens.def_mensagem_de_resultado_da_operacao(ativo_da_operacao, horario_da_operacao, timeframe, direcao, f'<b>Loss -R$({resultado_atual})</b>')
                                                        )
                                                        sticker_path = 'sticks/loss.webp'
                                                        self.api_telegram.send_sticker(chat_id=grupo, sticker=open(sticker_path, 'rb'))
                                                    
                                                        


                                                except Exception as error:
                                                    print(f"[LOG] @Catalogador | @Function monitor_operations | Erro ao enviar mensagem de loss | {ativo_da_operacao} {horario_da_operacao} {timeframe}M | Erro: {error}")
                                            
                                            # 3. excluir imagem
                                            try:
                                                self.lista_de_imagens.append(f'machinelearning/temporary images/{nome_da_imagem}')
                                            except Exception as error:
                                                print(f"[LOG] @Catalogador | @Function monitor_operations | Erro ao adicionar imagem a lista de exclusão | {ativo_da_operacao} {horario_da_operacao} {timeframe}M | Erro: {error}")
                                            
                                            # 4. enviar placar atual caso for loss no 2° martingale
                                            if resultado_atual == '2° Martingale':
                                                placar = self.botManager.addLoss()
                                                self.wins = placar["wins"]
                                                self.losses = placar["losses"]

                                                for grupo in lista_de_grupos:
                                                    try:
                                                        self.api_telegram.send_message(chat_id=grupo, text=mensagens.def_mensagem_do_placar(self.wins, self.losses))
                                                    except Exception as error:
                                                        print(f"[LOG] @Catalogador | @Function monitor_operations | Erro ao enviar placar | {ativo_da_operacao} {horario_da_operacao} {timeframe}M | Erro: {error}")
                                                break

                                    else:  # Se for um DOJI
                                        if resultado_atual == '2° Martingale':
                                            # 1. gerar imagem
                                            nome_da_imagem = grafico_candlestick(
                                                telegram={'id': api_hash}, velas=velas, titulo=ativo_da_operacao, subtitulo=f'Loss -R$({resultado_atual})')
                                            
                                            # 2. enviar imagem com a mensagem 
                                            for grupo in lista_de_grupos:
                                                try:
                                                    self.api_telegram.send_photo(
                                                        chat_id=grupo, 
                                                        photo=open(f'machinelearning/temporary images/{nome_da_imagem}', 'rb'), 
                                                        caption=mensagens.def_mensagem_de_resultado_da_operacao(
                                                            ativo_da_operacao, horario_da_operacao, timeframe, direcao, 
                                                            f'<b>Loss -R$({resultado_atual})</b>\n\n\n🔍 <i>DOJI</i> detectado no ativo <i>{ativo_da_operacao}</i>')
                                                    )
                                                    self.api_telegram.send_sticker(chat_id=grupo, sticker=open('sticks/doji.webp', 'rb'))
                                                except Exception as error:
                                                    print(f"[LOG] Erro ao enviar mensagem de DOJI | {ativo_da_operacao} | Erro: {error}")
                                            
                                            try:
                                                self.lista_de_imagens.append(f'machinelearning/temporary images/{nome_da_imagem}')
                                            except Exception as error:
                                                print(f"[LOG] Erro ao adicionar imagem a lista de exclusão | Erro: {error}")
                                            
                                            # 3. enviar placar
                                            placar = self.botManager.addLoss()
                                            self.wins = placar["wins"]
                                            self.losses = placar["losses"]

                                            for grupo in lista_de_grupos:
                                                try:
                                                    self.api_telegram.send_message(chat_id=grupo, text=mensagens.def_mensagem_do_placar(self.wins, self.losses))
                                                except Exception as error:
                                                    print(f"[LOG] @Catalogador | @Function monitor_operations | Erro ao enviar placar | {ativo_da_operacao} {horario_da_operacao} {timeframe}M | Erro: {error}")
                                            
                                            time.sleep(10)

                                            break  # Finalizar porque atingiu o limite de martingale
                                        else:
                                            # Enviar mensagem de DOJI e continuar para o próximo gale
                                            nome_da_imagem = grafico_candlestick(
                                                telegram={'id': api_hash}, velas=velas, titulo=ativo_da_operacao, subtitulo=f'DOJI detectado ({resultado_atual})')
                                            
                                            for grupo in lista_de_grupos:
                                                try:
                                                    self.api_telegram.send_photo(
                                                        chat_id=grupo, 
                                                        photo=open(f'machinelearning/temporary images/{nome_da_imagem}', 'rb'), 
                                                        caption=mensagens.def_mensagem_de_resultado_da_operacao(
                                                            ativo_da_operacao, horario_da_operacao, timeframe, direcao, 
                                                            f'\n🔍 DOJI detectado no ativo <i>{ativo_da_operacao}</i>. continuando operação...')
                                                    )
                                                except Exception as error:
                                                    print(f"[LOG] Erro ao enviar mensagem de DOJI (continuação) | {ativo_da_operacao} | Erro: {error}")
                                            
                                            try:
                                                self.lista_de_imagens.append(f'machinelearning/temporary images/{nome_da_imagem}')
                                            except Exception as error:
                                                print(f"[LOG] Erro ao adicionar imagem a lista de exclusão | Erro: {error}")
                                            
                                            time.sleep(10)
                                            continue  # Continuar para o próximo gale
                                    

                                break
                                
                                
                            else:
                                pass
                            time.sleep(1)
                    else:
                        pass
                else:
                    pass
            except Exception as error:
                print(f"{Fore.LIGHTBLACK_EX}@Catalogador {Fore.RESET}| {Fore.LIGHTBLACK_EX}@Function monitor_operations(try/catch){Fore.RESET} | {Fore.RED}@Error{Fore.RESET} {error}")


        # $ Operações Finalizadas
        print('{}{}{} Sessão de {} operações finalizada, agora iremos buscar novas operações...'.format(
            Fore.GREEN, HorariosDoBot.data_hora_weekday_str(), Fore.RESET, len(dicionario_com_operacoes_filtradas)))

        # $ Excluir Imagens
        total_de_imagens_antes_de_deletar = 0
        for imagem in self.lista_de_imagens:
            try:
                os.remove(imagem)
                total_de_imagens_antes_de_deletar += 1
            except Exception as erro:
                print("{Fore.GREEN}[LOG]{Fore.RESET} @Catalogador | @Function monitor_operations(try/exception) | ocorreu um erro ao tentar excluir a imagem {} | @Error {}".format(imagem, error))
        
        if total_de_imagens_antes_de_deletar > 0:
            print('{}{}{} Foram deletadas {} imagens'.format(
                Fore.GREEN, HorariosDoBot.data_hora_weekday_str(), Fore.RESET, total_de_imagens_antes_de_deletar))

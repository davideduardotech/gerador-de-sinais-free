import os, sys
import pytz
import time
from dotenv import load_dotenv
from datetime import datetime, timedelta
import telebot
from colorama import Fore, init
from iqoptionapi.stable_api import IQ_Option
import pymongo
import random
import horarios as HorariosDoBot
from catalogador import Catalogador
import afiliado

# Inicializações
init(autoreset=True, convert=True)
load_dotenv()

class Horario:
    def __init__(self, timezone="America/Sao_Paulo"):
        self.timezone = pytz.timezone(timezone)

class Catalogadora:
    def __init__(self, botManager):
        self.botManager = botManager
    
    def gerar_configuracao_aleatoria(self,configuracoes, timeframe=None):
        """Define configurações automáticas para catalogação"""
        configuracoes.update({
            "tipo de catalogação": "agressivo",
            "timeframe": timeframe or random.choice(['1 minuto', '5 minutos', '15 minutos']),
            "periodo de catalogação em dias": random.choice(['5 dias', '6 dias', '7 dias', '8 dias', '9 dias', '10 dias']),
            "martingale": "1 martingale",
            "porcentagem de assertividade(nenhum martingale)": random.choice(['78%', '80%']),
            "porcentagem de assertividade(1 martingale)": random.choice(['60%', '70%']),
            "porcentagem de assertividade(2 martingale)": random.choice(['60%', '70%']),  # Evita repetição manual
            "quantidade de operações que a Machine Learning ira filtrar": 20
        })

        return configuracoes
    def is_number(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False
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
        try:
            periodo_em_minutos = 120  # $ "tipo de catalogação":"agressivo",
            logging_operacoes_filtradas = ''
            lista = []
            for par in catalogacao:
                for horario in sorted(catalogacao[par]):
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
                        print(f"valor de % [{par}][{horario}] {catalogacao[par][horario]['%']}")
                        print(f"porcentagem de assertividade [{par}][{horario}] {configuracoes['porcentagem de assertividade(nenhum martingale)']}")
                        print(f"valor mg1 de % [{par}][{horario}] {catalogacao[par][horario]['mg1']['%']}")

                        if (is_number(catalogacao[par][horario]['%']) and 
                            is_number(catalogacao[par][horario]['mg1']['%']) and
                            float(catalogacao[par][horario]['%']) >= int(configuracoes['porcentagem de assertividade(nenhum martingale)'].replace('%', '')) and
                            float(catalogacao[par][horario]['mg1']['%']) >= int(configuracoes['porcentagem de assertividade(1 martingale)'].replace('%', '')) and
                            datetime.strptime(datetime.fromtimestamp(datetime.utcnow().timestamp() - 10800).strftime('%d/%m/%Y') + ' {}:00'.format(horario), '%d/%m/%Y %H:%M:%S') > datetime.fromtimestamp(datetime.utcnow().timestamp() - 10800) and
                            datetime.strptime(datetime.fromtimestamp(datetime.utcnow().timestamp() - 10800).strftime('%d/%m/%Y') + ' {}:00'.format(horario), '%d/%m/%Y %H:%M:%S') < datetime.fromtimestamp(datetime.utcnow().timestamp() - 10800) + timedelta(minutes=periodo_em_minutos)):
                            
                            lista.append({par: {horario: catalogacao[par][horario]}})
                            logging_operacoes_filtradas += '{}, {}%, {}%, M{}, {}\n'.format(
                                par, horario, catalogacao[par][horario]['%'], catalogacao[par][horario]['mg1']['%'], configuracoes['timeframe'].split(' ')[0].strip(), catalogacao[par][horario]['dir'])

                    if configuracoes['martingale'] == '2 martingale':
                        print(f"valor de % [{par}][{horario}] {catalogacao[par][horario]['%']}")
                        print(f"porcentagem de assertividade [{par}][{horario}] {configuracoes['porcentagem de assertividade(nenhum martingale)']}")
                        print(f"valor mg1 de % [{par}][{horario}] {catalogacao[par][horario]['mg1']['%']}")
                        print(f"valor mg2 de % [{par}][{horario}] {catalogacao[par][horario]['mg2']['%']}")

                        if (is_number(catalogacao[par][horario]['%']) and 
                            is_number(catalogacao[par][horario]['mg1']['%']) and
                            is_number(catalogacao[par][horario]['mg2']['%']) and
                            float(catalogacao[par][horario]['%']) >= int(configuracoes['porcentagem de assertividade(nenhum martingale)'].replace('%', '')) and
                            float(catalogacao[par][horario]['mg1']['%']) >= int(configuracoes['porcentagem de assertividade(1 martingale)'].replace('%', '')) and
                            float(catalogacao[par][horario]['mg2']['%']) >= int(configuracoes['porcentagem de assertividade(2 martingale)'].replace('%', '')) and
                            datetime.strptime(datetime.fromtimestamp(datetime.utcnow().timestamp() - 10800).strftime('%d/%m/%Y') + ' {}:00'.format(horario), '%d/%m/%Y %H:%M:%S') > datetime.fromtimestamp(datetime.utcnow().timestamp() - 10800) and
                            datetime.strptime(datetime.fromtimestamp(datetime.utcnow().timestamp() - 10800).strftime('%d/%m/%Y') + ' {}:00'.format(horario), '%d/%m/%Y %H:%M:%S') < datetime.fromtimestamp(datetime.utcnow().timestamp() - 10800) + timedelta(minutes=periodo_em_minutos)):
                            
                            lista.append({par: {horario: catalogacao[par][horario]}})
                            logging_operacoes_filtradas += '{}, {}%, {}%, {}%, M{}, {}\n'.format(
                                par, horario, catalogacao[par][horario]['%'], catalogacao[par][horario]['mg1']['%'], catalogacao[par][horario]['mg2']['%'], configuracoes['timeframe'].split(' ')[0].strip(), catalogacao[par][horario]['dir'])
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
        except Exception as error:
            print('ocorre um erro na função filtrar operações:', error)
    
    def cataloga(self, par, dias, timeframe):
        data = []
        datas_testadas = []
        time_ = time.time()
        start_timer = time.time() #$ Contagem de Tempo | Inicio
        sair = False
        while sair == False:
            try:
                velas = self.botManager.api_iqoption.get_candles(par, (timeframe * 60), 1000, time_)
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
        ativos = self.botManager.api_iqoption.get_all_open_time()
        
        start_time_all = time.time()
        print('{}[LOG]{}{}[CATALOGAÇÃO]{} {}{}{} Catalogação iniciada pra filtrar novas operações...'.format(
            Fore.LIGHTBLACK_EX, Fore.RESET,Fore.GREEN, Fore.RESET, Fore.LIGHTBLACK_EX, HorariosDoBot.data_hora_weekday_str(), Fore.RESET))

        catalogacao = {}
        for par in ativos['digital']:
            if ativos['digital'][par]['open'] == True:
                print('catalogando ativo:', par)

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
        print('indo pra função filtrar sinais')
        print('valor da catalogação:',catalogacao)
        dicionario_com_operacoes_filtradas = self.filtrar_operacoes(
            catalogacao,  configuracoes, configuracoes['quantidade de operações que a Machine Learning ira filtrar'])
        print('saiu da função self.filtrar_operacoes')
        print('{}[LOG]{}{}[CATALOGAÇÃO FINALIZADA]{} {}{}{} Catalogação finalizada em todos ativos{}(demorou {} segundos){}'.format(Fore.LIGHTBLACK_EX, Fore.RESET,Fore.GREEN, Fore.RESET, Fore.LIGHTBLACK_EX, HorariosDoBot.data_hora_weekday_str(), Fore.RESET, Fore.LIGHTBLACK_EX, abs(end_time_all-start_time_all),Fore.RESET))
        return dicionario_com_operacoes_filtradas

    

    



        
class BotManager:
    def __init__(self):
        self.email_iqoption = os.getenv("EMAIL_IQOPTION")
        self.senha_iqoption = os.getenv("SENHA_IQOPTION")
        self.token_telegram_bot = os.getenv("TOKEN_TELEGRAM_BOT")
        self.mongodb_uri = os.getenv("MONGODB_URI")
        self.id_grupo_telegram = int(os.getenv("ID_GRUPO_TELEGRAM", -1))
       
        self.api_telegram = telebot.TeleBot(self.token_telegram_bot, parse_mode='HTML')
        self.api_iqoption = None

        self.horario = Horario()
        self.catalogador = None

        self.mongodb = None
        self.mongodbDatabase = "ClubeDosInvestidores"
        self.mongodbCollection = "Configuracoes"
        self.mongodbDocument = {}

        self.lista_de_grupos = [self.id_grupo_telegram]

    def datetime_and_weekday_in_string(self): 
        days = ['Segunda-Feira','Terça-feira','Quarta-feira','Quinta-feira','Sexta-feira','Sábado','Domingo']
        return '{}, {}'.format(datetime.fromtimestamp(datetime.utcnow().timestamp() - 10800).strftime('%d/%m/%Y %H:%M:%S'),days[datetime.fromtimestamp(datetime.utcnow().timestamp() - 10800).weekday()] )

    def logging(self, info, message):
        print(f"{Fore.LIGHTBLACK_EX}[LOG]{Fore.RESET}{info} {Fore.LIGHTBLACK_EX}{self.datetime_and_weekday_in_string()}{Fore.RESET} {message}")

    def addWin(self):
        """
        Adiciona uma vitória ao placar atual no documento do MongoDB.
        """
        try:
            documento = self.mongodbCollection.find_one({"_id": self.mongodbDocument["_id"]})
            if not documento:
                raise ValueError("Nenhum documento encontrado na coleção.")

            # Obtém o placar atual e incrementa a vitória
            placar_atual = documento.get("placar atual", "0x0")
            wins, losses = map(int, placar_atual.split("x"))
            wins += 1

            # Atualiza o placar no MongoDB
            self.mongodbCollection.update_one(
                {"_id": documento["_id"]},
                {"$set": {"placar atual": f"{wins}x{losses}"}}
            )

            self.mongodbDocument = self.mongodbCollection.find_one({"_id": documento["_id"]})

            return {"wins": wins, "losses": losses, "placar atual": f"{wins}x{losses}"}
        except Exception as erro:
            self.logging(f"{Fore.RED}[MONGODB]{Fore.RESET}", f"Erro ao adicionar win: {erro}")
            return None

    def addLoss(self):
        """
        Adiciona uma derrota ao placar atual no documento do MongoDB.
        """
        try:
            # Busca o documento atual
            documento = self.mongodbCollection.find_one({"_id": self.mongodbDocument["_id"]})
            if not documento:
                raise ValueError("Nenhum documento encontrado na coleção.")

            # Obtém o placar atual e incrementa a derrota
            placar_atual = documento.get("placar atual", "0x0")
            wins, losses = map(int, placar_atual.split("x"))
            losses += 1

            # Atualiza o placar no MongoDB
            self.mongodbCollection.update_one(
                {"_id": documento["_id"]},
                {"$set": {"placar atual": f"{wins}x{losses}"}}
            )

            self.mongodbDocument = self.mongodbCollection.find_one({"_id": documento["_id"]})

            return {"wins": wins, "losses": losses, "placar atual": f"{wins}x{losses}"}
        except Exception as erro:
            self.logging(f"{Fore.RED}[MONGODB]{Fore.RESET}", f"Erro ao adicionar derrota: {erro}")
            return None

    def conectar_mongodb(self):
        """Conecta ao banco de dados MongoDB."""
        while True:
            try:
                self.mongodb = pymongo.MongoClient(self.mongodb_uri)
                self.logging(f"{Fore.GREEN}[MONGODB]{Fore.RESET}", f"Banco de dados conectado")
                
                self.mongodbDatabase = self.mongodb[self.mongodbDatabase]
                self.mongodbCollection = self.mongodbDatabase[self.mongodbCollection]

                 # Busca um documento na coleção
                configuracao = self.mongodbCollection.find_one()
                if configuracao:
                    self.mongodbDocument = configuracao
                    self.logging(f"{Fore.CYAN}[MONGODB]{Fore.RESET}", f"documento de configuração encontrado: {configuracao}")
                else:
                    # Caso a coleção esteja vazia, criar um novo documento
                    self.logging(f"{Fore.YELLOW}[MONGODB]{Fore.RESET}", "nenhum documento encontrado. criando novo...")
                    novo_documento = {"placar_atual": "0x0"}
                    result = self.mongodbCollection.insert_one(novo_documento)
                    configuracao = self.mongodbCollection.find_one({"_id": result.inserted_id})
                    self.mongodbDocument = configuracao
                    self.logging(f"{Fore.GREEN}[MONGODB]{Fore.RESET}", f"novo documento de configuração criado: {configuracao}")
                break
            except Exception as erro:
                self.logging(f"{Fore.RED}[MONGODB]{Fore.RESET}", f"Erro ao conectar ao MongoDB: {erro}{Fore.RESET}")
                sys.exit()
                time.sleep(1)

    def conectar_iqoption(self):
        """Conecta à conta da IQ Option."""
        while True:
            try:
                self.api_iqoption = IQ_Option(self.email_iqoption, self.senha_iqoption)
                self.api_iqoption.connect()
                if self.api_iqoption.check_connect():
                    saldo = self.api_iqoption.get_balance()
                    self.logging(f"{Fore.GREEN}[IQ OPTION]{Fore.RESET}", f"conectada, banca atual R${saldo} (Conta de Treinamento)")
                    return self.api_iqoption
                else:
                    self.logging(f"{Fore.RED}[IQ OPTION]{Fore.RESET}", "Erro ao conectar na IQ Option. Tentando novamente...")
            except Exception as erro:
                self.logging(f"{Fore.RED}[IQ OPTION]{Fore.RESET}", f"Erro ao conectar na IQ Option: {erro}")
                time.sleep(2)

    def reconectar_iqoption(self):
        """Reconecta à conta da IQ Option em caso de desconexão."""
        self.logging(f"{Fore.YELLOW}[IQ OPTION]{Fore.RESET}", "Reconectando na IQ Option...")
        return self.conectar_iqoption()

    def processar_sinais(self):
        """Processa os sinais da IQ Option e envia mensagens para os grupos do Telegram."""
        self.catalogador = Catalogador(self)
        while True:
            try:
                # Verifica a conexão com a IQ Option
                if not self.api_iqoption.check_connect():
                    self.reconectar_iqoption()
                
                configuracoes = self.catalogador.definir_configuracoes_automaticas_para_operacoes_rapidas({}, timeframe='1 minuto')
                dicionario_operacoes = self.catalogador.catalogar_operacoes_rapidas(configuracoes)
                
                self.catalogador.monitor_operations(
                    self.api_iqoption,
                    self.api_telegram,
                    self.lista_de_grupos,

                    dicionario_operacoes,
                    configuracoes
                )
            except Exception as erro:
                print(f"{Fore.RED}Erro no processamento de sinais: {erro}{Fore.RESET}")
                time.sleep(2)

    def iniciar(self):
        """Inicializa o bot."""
        print("| Detalhes")
        print("Desenvolvedor: David Eduardo (https://github.com/davideduardotech)")

        self.conectar_mongodb()
        self.conectar_iqoption()
        self.processar_sinais()


if __name__ == "__main__":
    bot_manager = BotManager()
 
    bot_manager.iniciar()

from datetime import datetime, time, timedelta



def ConverterHorarioPraTimestamp(horario):
    timestamp_sinal = int(datetime.timestamp(datetime.strptime((datetime.fromtimestamp(datetime.utcnow().timestamp() - 10800)).strftime('%d/%m/%Y ') + horario.strip() + ':00', '%d/%m/%Y %H:%M:%S')))



"""
CODDING: Automatizador de lista
"""
def ConverterHorarioDaOperacaoPraTimestemp(horario):
    return int(datetime.timestamp(datetime.strptime(horario, '%d/%m/%Y %H:%M:%S')))




"""
CODDING: Controle de Assinatura
| Biblioteca de Tempo
"""
def verificar_assinatura_na_plataforma(data_de_expiracao):
    data_atual_strptime = datetime.strptime(datetime.fromtimestamp(datetime.utcnow().timestamp() - 10800).strftime('%d/%m/%Y %H:%M:%S'),'%d/%m/%Y %H:%M:%S')
    data_de_expiracao_strptime = datetime.strptime(data_de_expiracao+' 23:59:00','%d/%m/%Y %H:%M:%S')
    return data_atual_strptime <= data_de_expiracao_strptime

def date_diff_in_seconds(dt2, dt1):
  timedelta = dt2 - dt1
  return timedelta.days * 24 * 3600 + timedelta.seconds
def dhms_from_seconds(seconds):
	minutes, seconds = divmod(seconds, 60)
	hours, minutes = divmod(minutes, 60)
	days, hours = divmod(hours, 24)
	return (days, hours, minutes, seconds)
def data_atual_strptime():
    return datetime.strptime(datetime.fromtimestamp(datetime.utcnow().timestamp() - 10800).strftime('%d/%m/%Y %H:%M:%S'),'%d/%m/%Y %H:%M:%S')
def calcular_dias_horas_minutos_segundos_da_licenca(usuario):
    try:
        #$ Format: %d/%m/%Y
        data_de_expiracao = datetime.strptime(usuario['data de expiração']+' 23:59:59','%d/%m/%Y %H:%M:%S')
    except:
        #$ Format: %d/%m/%Y %H:%M:%S
        data_de_expiracao = datetime.strptime(usuario['data de expiração'],'%d/%m/%Y %H:%M:%S')
    return dhms_from_seconds(date_diff_in_seconds(data_de_expiracao,data_atual_strptime()))
    
def CalcularDiasHorasMinutosESegundosDeUmaDataDeExpiracao(DataDeExpiracao):
    if data_atual_strptime() < (datetime.strptime(DataDeExpiracao+' 23:59:59', '%d/%m/%Y 23:59:59')):
        return dhms_from_seconds(date_diff_in_seconds(datetime.strptime(DataDeExpiracao+' 23:59:59','%d/%m/%Y %H:%M:%S'),data_atual_strptime()))
    else:
        return 0,0,0,0

    
def CalcularDiaHorasMinutosESegundosDaPromocao(DataDeExpiracao):
    if data_atual_strptime() < datetime.strptime((datetime.strptime(DataDeExpiracao, '%d/%m/%Y')+timedelta(days=1)).strftime('%d/%m/%Y')+' 23:59:59','%d/%m/%Y %H:%M:%S'):
        return dhms_from_seconds(date_diff_in_seconds(datetime.strptime(DataDeExpiracao+' 23:59:59','%d/%m/%Y %H:%M:%S'),data_atual_strptime()))
    else:
        return 0,0,0,0








""""
CODDING: Catalogador 100% autoomatico
https://davidempreendedor.tech/spacerobot
"""
def week_day_brazil():
    week = ['segunda-feira','terça-feira','quarta-feira','quinta-feira','sexta-feira','sábado','domingo']
    day = datetime.fromtimestamp(datetime.utcnow().timestamp() - 10800).weekday()
    return week[day]

def HorarioQDialogFiltrarOperacoes():
    dia_atual_em_numero = datetime.fromtimestamp(datetime.utcnow().timestamp() - 10800).strftime('%d')
    
    dia_atual_em_texto = week_day_brazil()
    meses = ['Janeiro' ,'Fevereiro' ,'Março', 'Abril' ,'Maio' ,'Junho', 'Julho' ,'Agosto' ,'Setembro', 'Outubro' ,'Novembro' ,'Dezembro']
    mes_atual_em_texto = meses[int(datetime.fromtimestamp(datetime.utcnow().timestamp() - 10800).strftime('%m'))-1]
    return '{} de {}, {}'.format(dia_atual_em_numero, mes_atual_em_texto,dia_atual_em_texto)
    
    
    














"""
CODDING: Controle de Horarios
https://davidempreendedor.tech/spacerobot
"""
def data_hora_weekday_str():
    days = ['Segunda-Feira','Terça-feira','Quarta-feira','Quinta-feira','Sexta-feira','Sábado','Domingo']
    return '{}, {}'.format(datetime.fromtimestamp(datetime.utcnow().timestamp() - 10800).strftime('%d/%m/%Y %H:%M:%S'),days[datetime.fromtimestamp(datetime.utcnow().timestamp() - 10800).weekday()] )

def horario_atual_strftime():
    return datetime.fromtimestamp(datetime.utcnow().timestamp() - 10800).strftime('%d/%m/%Y %H:%M:%S')
def horario_atual_datetime():
    return datetime.fromtimestamp(datetime.utcnow().timestamp() - 10800)

def mes_do_ano(timestamp):
    meses = ['Janeiro' ,'Fevereiro' ,'Março', 'Abril' ,'Maio' ,'Junho', 'Julho' ,'Agosto' ,'Setembro', 'Outubro' ,'Novembro' ,'Dezembro']
    mes = int(datetime.fromtimestamp(timestamp).strftime('%m'))
    return meses[mes-1]

def dia_atual_em_numero(timestemp):
    return datetime.fromtimestamp(timestemp).strftime('%d')

def data_atual_strftime():
    return datetime.fromtimestamp(datetime.utcnow().timestamp() - 10800).strftime('%d/%m/%Y')










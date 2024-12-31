import telebot

def afiliadoDaPlataforma(nomeDoAfiliado,idDoGrupoDoTelegram,numeroDoWhatsapp,urlLandingPage,urlMangoTrader):
    # {"id do grupo(Telegram)":-1001796264233,"nome do afiliado":"David Eduardo","link de afiliado(mango trader)":"","link de afiliado(LandingPage)":""}
    urlDoWhatsapp = f"https://api.whatsapp.com/send?phone={numeroDoWhatsapp}&text=Ol%C3%A1%2C%20quero%20adquirir%20a%20sala%20de%20sinais%20de%20voc%C3%AAs%2C%20pode%20me%20enviar%20as%20informa%C3%A7%C3%B5es%20de%20pagamento%3F"
    
    button_whatsapp = telebot.types.InlineKeyboardButton(
        "🚀 Whatsapp para Adquirir", url=urlDoWhatsapp)
    KEYBOARD_WHATSAPP = telebot.types.InlineKeyboardMarkup()
    KEYBOARD_WHATSAPP.row(button_whatsapp)

    button_website = telebot.types.InlineKeyboardButton(
        "🌐 Acesse nosso Site", url=urlLandingPage)
    KEYBOARD_WEBSITE = telebot.types.InlineKeyboardMarkup()
    KEYBOARD_WEBSITE.row(button_website)
    
    """
    CODDING: Criando KeyBoard com Whatsapp e WebSite
    """
    KEYBOARD_WHATSAPP_E_WEBSITE = telebot.types.InlineKeyboardMarkup(row_width=1) 
    KEYBOARD_WHATSAPP_E_WEBSITE.add(button_whatsapp)
    KEYBOARD_WHATSAPP_E_WEBSITE.add(button_website)

    return {
        "nome do afiliado":nomeDoAfiliado,
        "id do grupo(telegram)":idDoGrupoDoTelegram,
        "link de afiliado(whatsapp)":urlDoWhatsapp,
        "link de afiliado(mango trader)":urlMangoTrader,
        "link de afiliado(landing page)":urlLandingPage,
        "keyboard whatsapp":KEYBOARD_WHATSAPP,
        "keyboard website":KEYBOARD_WEBSITE,
        "keyboard whatsapp e website":KEYBOARD_WHATSAPP_E_WEBSITE
    }
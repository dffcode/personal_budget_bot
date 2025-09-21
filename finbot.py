import telebot
from telebot import types

def load_file(name):
    """
    Load file and return it's content
    Empty strings don't return
    """
    with open(name, "r") as f:
        content = f.read().split("\n")
        return([l for l in content if len(l) != 0])

def save_file(content, name):
    """
    Save content to file with name
    """
    try:
        with open(name, "w") as f:
            f.write(content)
    except Exception as e:
        print(e)

def add_file(content, name):
    """
    Add content to file with name name
    """
    with open(name, "a") as f:
        f.write(content)

def pop_file(content, name):
    """
    Delete string from file name
    """
    tmp = load_file(name)
    tmp1 = [e for e in tmp if content not in e]
    tmp2 = [e + "\n" for e in tmp1]
    tmp3 = ''.join(tmp2)
    save_file(tmp3, name)

def id_file(uid, name):
    tmp = load_file(name)
    content = []
    for e in tmp:
        if e.split(":")[0] == uid:
            content.append(":".join(e.split(":")[1:]))
    return(content)


TOKEN = ""
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def start(message):
    global start_markup
    start_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    about = "Этот бот предназначен для ведения личного бюджета. Внутри - финансовые модели, графики, расчёты. Перед началом работы заполните все необходимые переменные. "
    btn1 = types.KeyboardButton("Помощь")
    btn2 = types.KeyboardButton("Доходы")
    btn3 = types.KeyboardButton("Вклады")
    btn4 = types.KeyboardButton("Расходы")
    btn5 = types.KeyboardButton("Остатки")
    btn6 = types.KeyboardButton("Возраст")
    btn7 = types.KeyboardButton("Отчет")
    btn8 = types.KeyboardButton("Рассчёт доходности")
    start_markup.add(btn1,btn2,btn3,btn4,btn5,btn6,btn7,btn8)
    bot.send_message(message.from_user.id, about, reply_markup=start_markup)

@bot.message_handler(content_types=["text"])
def get_text_messages(message):
    global wait_for
    if message.text == "Помощь":
        help = 'Введите свои источники дохода, вклады, все расходы, остатки на счетах, и возраст. Нажмите кнопку "Рассчёт доходности".'
        bot.send_message(message.from_user.id, help, reply_markup=start_markup)


    elif message.text == "Отчет":
        files = ["age", "deposites", "expenses", "remains", "sources"]
        summary = ""
        for f in files:
            try:
                tmp = load_file(f)
                for e in tmp:
                    if e.split(":")[0] == str(message.from_user.id):
                        summary += ":".join(e.split(":")[1:]) + "\n"
            except:
                if f == "age":
                    summary += "Пусто:0\n"
                if f == "deposites":
                    summary += "Вклады:0:0\n"
                if f == "expenses":
                    summary += "Траты:0\n"
                if f == "remains":
                    summary += "Остатки:0\n"
                if f == "sources":
                    summary += "Источники дохода:0\n"
        bot.send_message(message.from_user.id, summary, reply_markup=start_markup)


    elif message.text == "Рассчёт доходности":
        uid = str(message.from_user.id)
        try:
            age = float(id_file(uid, "age")[0].split(":")[1])
        except:
            age = 0.0
        try:
            deposites = [e.split(":")[1:] for e in id_file(uid, "deposites")]
        except:
            deposites = [[0.0, 0.0]]
        try:
            expenses = sum([float(e.split(":")[1]) for e in id_file(uid, "expenses")])
        except:
            expenses = 0.0
        try:
            remains = float((id_file(uid, "remains")[0]).split(":")[1])
        except:
            remains = 0.0
        try:
            sources = sum([float(e.split(":")[1]) for e in id_file(uid, "sources")])
        except:
            sources = 0.0

        today_money = sum([float(e[0]) for e in deposites]) + remains
        msg = "Текущее состояние: " + str(int(today_money)) + " руб." + "\n"

        if age < 30.0:
            years = 30.0 - age
            months = years * 12.0
            summ = remains
            deposites_30 = []
            # Calc deposites
            for d in deposites:
                rate = float(d[1]) / 100.0
                i = years // 1.0
                tmp = float(d[0])
                while i > 0:
                    tmp = tmp + tmp * rate
                    i = i - 1.0
                tmp = tmp + tmp * rate * (years % 1.0)
                deposites_30.append([tmp, d[1]])
                summ = summ + tmp
            # Calc expenses and sources
            summ = summ - expenses * months
            summ = summ + sources * months
            msg = msg + "Состояние в 30 лет: " + str(int(summ)) + " руб." + "\n"


        if age < 40.0:
            years = 10.0
            months = years * 12.0
            deposites_40 = []
            # Calc depositess
            for d in deposites_30:
                rate = float(d[1]) / 100.0
                i = years // 1.0
                tmp = float(d[0])
                while i > 0:
                    tmp = tmp + tmp * rate
                    i = i - 1.0
                tmp = tmp + tmp * rate * (years % 1.0)
                deposites_40.append([tmp, d[1]])
                summ = summ + tmp
            # Calc expenses and sources
            summ = summ - expenses * months
            summ = summ + sources * months
            msg = msg + "Состояние в 40 лет: " + str(int(summ)) + " руб." + "\n"

        if age < 50.0:
            years = 10.0
            months = years * 12.0
            deposites_50 = []
            # Calc deposites

            for d in deposites_40:
                rate = float(d[1]) / 100.0
                i = years // 1.0
                tmp = float(d[0])

                while i > 0:
                    tmp = tmp + tmp * rate
                    i = i - 1.0

                tmp = tmp + tmp * rate * (years % 1.0)
                deposites_50.append([tmp, d[1]])
                summ = summ + tmp
            # Calc expenses and sources
            summ = summ - expenses * months
            summ = summ + sources * months
            msg = msg + "Состояние в 50 лет: " + str(int(summ)) + " руб." + "\n"

        if age < 60.0:
            years = 10.0
            months = years * 12.0
            deposites_60 = []
            # Calc deposites
            for d in deposites_50:
                rate = float(d[1]) / 100.0
                i = years // 1.0
                tmp = float(d[0])
                while i > 0:
                    tmp = tmp + tmp * rate
                    i = i - 1.0
                tmp = tmp + tmp * rate * (years % 1.0)
                deposites_60.append([tmp, d[1]])
                summ = summ + tmp
            # Calc expenses and sources
            summ = summ - expenses * months
            summ = summ + sources * months
            msg = msg + "Состояние в 60 лет: " + str(int(summ)) + " руб." + "\n"

        if age < 70.0:
            years = 10.0
            months = years * 12.0
            deposites_70 = []
            # Calc deposites
            for d in deposites_60:
                rate = float(d[1]) / 100.0
                i = years // 1.0
                tmp = float(d[0])
                while i > 0:
                    tmp = tmp + tmp * rate
                    i = i - 1.0
                tmp = tmp + tmp * rate * (years % 1.0)
                deposites_70.append([tmp, d[1]])
                summ = summ + tmp
            # Calc expenses and sources
            summ = summ - expenses * months
            summ = summ + sources * months
            msg = msg + "Состояние в 70 лет: " + str(int(summ)) + " руб." + "\n"

        if age < 80.0:
            years = 10.0
            months = years * 12.0
            # Calc deposites
            for d in deposites_70:
                rate = float(d[1]) / 100.0
                i = years // 1.0
                tmp = float(d[0])
                while i > 0:
                    tmp = tmp + tmp * rate
                    i = i - 1.0
                tmp = tmp + tmp * rate * (years % 1.0)
                summ = summ + tmp
            # Calc expenses and sources
            summ = summ - expenses * months
            summ = summ + sources * months
            msg = msg + "Состояние в 80 лет: " + str(int(summ)) + " руб." + "\n"

        bot.send_message(message.from_user.id, msg, reply_markup = start_markup)


    elif message.text == "Назад":
        bot.send_message(message.from_user.id, "Главное меню", reply_markup=start_markup)


    elif message.text == "Доходы":
        global sources_markup
        sources_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Новый доход")
        btn2 = types.KeyboardButton("Все доходы")
        btn3 = types.KeyboardButton("Удалить доход")
        btn4 = types.KeyboardButton("Назад")
        sources_markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.from_user.id, "Меню доходов", reply_markup=sources_markup)


    elif message.text == "Новый доход":
        wait_for = "Доход"
        help = 'Введите доход в формате "Название:рублей в месяц"'
        bot.send_message(message.from_user.id, help, reply_markup=sources_markup)


    elif message.text == "Все доходы":
        answer = ["Пусто"]
        try:
            tmp = load_file("sources")
            tmp1 = [e for e in tmp if e.split(":")[0] == str(message.from_user.id)]
            answer = []
            for e in tmp1:
                tmp2 = e.split(":")[1:]
                tmp3 = ":".join(tmp2)
                if len(tmp3) > 4:
                    answer.append(tmp3)
            if len(answer) == 0:
                answer = ["Пусто"]
        except:
            pass
        bot.send_message(message.from_user.id, "\n".join(answer), reply_markup=sources_markup)


    elif message.text == "Удалить доход":
        wait_for = "Удалить доход"
        help = 'Введите доход для удаления в формате "Название:рублей в месяц"'
        bot.send_message(message.from_user.id, help, reply_markup=sources_markup)


    elif message.text == "Вклады":
        global deposites_markup
        deposites_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Новый вклад")
        btn2 = types.KeyboardButton("Все вклады")
        btn3 = types.KeyboardButton("Удалить вклад")
        btn4 = types.KeyboardButton("Назад")
        deposites_markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.from_user.id, "Меню вкладов", reply_markup=deposites_markup)


    elif message.text == "Новый вклад":
        wait_for = "Вклад"
        help = 'Введите вклад в формате "Название:рублей:процентная ставка в год". Пример: "Втб:14.5"'
        bot.send_message(message.from_user.id, help, reply_markup=deposites_markup)


    elif message.text == "Все вклады":
        answer = ["Пусто"]
        try:
            tmp = load_file("deposites")
            tmp1 = [e for e in tmp if e.split(":")[0] == str(message.from_user.id)]
            answer = []
            for e in tmp1:
                tmp2 = e.split(":")[1:]
                tmp3 = ":".join(tmp2)
                if len(tmp3) > 4:
                    answer.append(tmp3)
            if len(answer) == 0:
                answer = ["Пусто"]
        except:
            pass
        bot.send_message(message.from_user.id, "\n".join(answer), reply_markup=deposites_markup)


    elif message.text == "Удалить вклад":
        wait_for = "Удалить вклад"
        help = 'Введите вклад для удаления в формате "Название:рублей:процентная ставка в год"'
        bot.send_message(message.from_user.id, help, reply_markup=deposites_markup)


    elif message.text == "Расходы":
        global expenses_markup
        expenses_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Новый расход")
        btn2 = types.KeyboardButton("Все расходы")
        btn3 = types.KeyboardButton("Удалить расход")
        btn4 = types.KeyboardButton("Назад")
        expenses_markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.from_user.id, "Меню расходов", reply_markup=expenses_markup)


    elif message.text == "Новый расход":
        wait_for = "Расход"
        help = 'Введите расход в формате "Название:рублей в месяц"'
        bot.send_message(message.from_user.id, help, reply_markup=expenses_markup)


    elif message.text == "Все расходы":
        answer = ["Пусто"]
        try:
            tmp = load_file("expenses")
            tmp1 = [e for e in tmp if e.split(":")[0] == str(message.from_user.id)]
            answer = []
            for e in tmp1:
                tmp2 = e.split(":")[1:]
                tmp3 = ":".join(tmp2)
                if len(tmp3) > 4:
                    answer.append(tmp3)
            if len(answer) == 0:
                answer = ["Пусто"]
        except:
            pass
        bot.send_message(message.from_user.id, "\n".join(answer), reply_markup=expenses_markup)


    elif message.text == "Удалить расход":
        wait_for = "Удалить расход"
        help = 'Введите расход для удаления в формате "Название:рублей в месяц"'
        bot.send_message(message.from_user.id, help, reply_markup=expenses_markup)


    elif message.text == "Остатки":
        wait_for = "Остатки"
        help = 'Введите остатки на счетах в формате "Название:рублей"'
        bot.send_message(message.from_user.id, help, reply_markup=start_markup)


    elif message.text == "Возраст":
        wait_for = "Возраст"
        help = 'Введите возраст в формате "Имя:Возраст"'
        bot.send_message(message.from_user.id, help, reply_markup=start_markup)


    elif ":" in message.text:
        if wait_for == "Доход":
            content = str(message.from_user.id) + ":" + message.text + "\n"
            add_file(content, "sources")
            wait_for = ""
            bot.send_message(message.from_user.id, "Меню доходов", reply_markup=sources_markup)


        if wait_for == "Вклад":
            content = str(message.from_user.id) + ":" + message.text + "\n"
            add_file(content, "deposites")
            wait_for = ""
            bot.send_message(message.from_user.id, "Меню вкладов", reply_markup=deposites_markup)


        if wait_for == "Расход":
            content = str(message.from_user.id) + ":" + message.text + "\n"
            add_file(content, "expenses")
            wait_for = ""
            bot.send_message(message.from_user.id, "Меню расходов", reply_markup=expenses_markup)


        if wait_for == "Остатки":
            content = str(message.from_user.id) + ":" + message.text + "\n"
            # Check if there is remains
            try:
                tmp = load_file("remains")
                for e in tmp:
                    if e.split(":")[0] == str(message.from_user.id):
                        pop_file(e, "remains")
            except:
                pass
            add_file(content, "remains")
            wait_for = ""
            bot.send_message(message.from_user.id, "Главное меню", reply_markup=start_markup)


        if wait_for == "Возраст":
            content = str(message.from_user.id) + ":" + message.text + "\n"
            # Check if there is age
            try:
                tmp = load_file("age")
                for e in tmp:
                    if e.split(":")[0] == str(message.from_user.id):
                        pop_file(e, "age")
            except:
                pass
            add_file(content, "age")
            wait_for = ""
            bot.send_message(message.from_user.id, "Главное меню", reply_markup=start_markup)


        if wait_for == "Удалить доход":
            content = str(message.from_user.id) + ":" + message.text
            try:
                pop_file(content, "sources")
                wait_for = ""
            except:
                pass
            bot.send_message(message.from_user.id, "Меню доходов", reply_markup=sources_markup)


        if wait_for == "Удалить вклад":
            content = str(message.from_user.id) + ":" + message.text
            try:
                pop_file(content, "deposites")
                wait_for = ""
            except:
                pass
            bot.send_message(message.from_user.id, "Меню вкладов", reply_markup=deposites_markup)



        if wait_for == "Удалить расход":
            content = str(message.from_user.id) + ":" + message.text
            try:
                pop_file(content, "expenses")
                wait_for = ""
            except:
                pass
            bot.send_message(message.from_user.id, "Меню расходов", reply_markup=expenses_markup)


bot.polling(none_stop=True, interval=0)

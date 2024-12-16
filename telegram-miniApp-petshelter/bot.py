from gc import callbacks

import time
import telebot
import os
from dotenv import load_dotenv
load_dotenv()

# import  workbook_master


from db_calls import get_pets_by_type, add_pets, update_pets, get_applications_bot, get_application_bot, \
    set_application_wip, set_application_accepted, set_application_declined
from workbook_master_ng import generate_template, get_pets_data_from_file, get_pets_table_as_file


from telebot import types, TeleBot
from concurrent.futures import ThreadPoolExecutor

bot: TeleBot = telebot.TeleBot(os.getenv('botToken'))

pet_admin_message_sequence=[]

def flush_message_sequence(message_sequence, chat_id):
    def delete_message(message_id):
        try:
            bot.delete_message(chat_id=chat_id, message_id=message_id)
            print(f"Deleted message {message_id}")
        except Exception as e:
            print(f"Failed to delete message {message_id}: {e}")
    with ThreadPoolExecutor(max_workers=6) as executor:
        executor.map(delete_message, message_sequence)

def constract_application_text(application):
    id_user = int(application["id_user"])
    user_data = bot.get_chat(id_user)
    first_name = user_data.first_name
    last_name = user_data.last_name

    application_data = (f"<strong>Заявка №{application['id_application']}</strong>\n\n"
                        f"<strong>Информация о питомце:</strong>\n\n"
                        f"Кличка: {application['name']}\n"
                        f"Возраст: {application['age']}\n"
                        f"Пол: {application['sex']}\n"
                        f"<a href='{application['album_link']}'>Альбом питомца</a>\n\n"
                        f"<strong>Информация о пользователе:</strong>\n\n"
                        f"Фамилия: {last_name}\n"
                        f"Имя: {first_name}\n"
                        f"<a href='tg://user?id={id_user}'>Профиль в телеграмме</a>\n")
    return application_data

def construct_applications_keyboard(applications):
    applicationsKeyboard = types.InlineKeyboardMarkup()
    backButton = types.InlineKeyboardButton(text='Назад', callback_data='BackA1')
    applicationsKeyboard.add(backButton)
    if len(applications) > 0:
        for application in applications:
            appButton = types.InlineKeyboardButton(text=str(application["id"]),
                                                   callback_data='A' + str(application["id"]))
            applicationsKeyboard.add(appButton)
    return  applicationsKeyboard
    pass

def construct_applications_header(stage):
    text_for_keyboard = ""
    if stage == 1:
        text_for_keyboard = "Новые заявки:"
    elif stage == 2:
        text_for_keyboard = "Заявки в работе:"
    elif stage == 3:
        text_for_keyboard = "Завершенные заявки:"
    return text_for_keyboard
    pass

def construct_applications_stages_keyboard():
    applicationsKeyboard = types.InlineKeyboardMarkup()
    newApplicationsKey = types.InlineKeyboardButton(text='Новые заявки', callback_data='WA' + str(1))
    inProgressApplicationsKey = types.InlineKeyboardButton(text='Заявки в работе', callback_data='WA' + str(2))
    doneApplicationsKey = types.InlineKeyboardButton(text='Решенные заявки', callback_data='WA' + str(3))
    applicationsKeyboard.add(newApplicationsKey)
    applicationsKeyboard.add(inProgressApplicationsKey)
    applicationsKeyboard.add(doneApplicationsKey)
    backButton = types.InlineKeyboardButton(text='Назад', callback_data='Back0')
    applicationsKeyboard.add(backButton)
    return applicationsKeyboard
    pass

def construct_main_menu_keyboard(userId):
    mainMenuKeyboard = types.InlineKeyboardMarkup()
    openAppKey = types.InlineKeyboardButton(text='Открыть приложение',
                                            web_app=types.WebAppInfo(url=os.getenv('miniAppUrl')))
    mainMenuKeyboard.add(openAppKey)
    masterUserId = os.getenv('masterUser')
    if str(masterUserId) == str(userId):
        viewApplications = types.InlineKeyboardButton(text='Управление заявками', callback_data='10')
        addPets = types.InlineKeyboardButton(text='Управление питомцами', callback_data='3')
        mainMenuKeyboard.add(viewApplications)
        mainMenuKeyboard.add(addPets)
    return mainMenuKeyboard
    pass

def construct_decision_keyboard(stage, applicationId):
    application_keyboard = types.InlineKeyboardMarkup()
    if stage == 1:
        key = types.InlineKeyboardButton(text='Приступить к работе', callback_data='SPA' + str(applicationId))
        application_keyboard.add(key)
        pass
    elif stage == 2:
        acceptKey = types.InlineKeyboardButton(text='Одобрить', callback_data='AA' + str(applicationId))
        declineKey = types.InlineKeyboardButton(text='Отклонить', callback_data='DA' + str(applicationId))
        application_keyboard.add(acceptKey,declineKey)
        pass
    backButton = types.InlineKeyboardButton(text='Назад', callback_data='BackA2_'+str(stage))
    application_keyboard.add(backButton)
    return application_keyboard
    pass

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id, text='Меню выбора действия:', reply_markup=construct_main_menu_keyboard(message.from_user.id))

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data =='1':
        pass
    elif str(call.data[0:4])=='Back':
        if str(call.data[4:5])=='A':
            level = int(call.data[5:6])
            if level == 1:
                bot.edit_message_text(chat_id=call.message.chat.id,
                                      text='Выберите тип заявки для просмотра:',
                                      message_id=call.message.message_id
                                      )
                bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                              message_id=call.message.message_id,
                                              reply_markup=construct_applications_stages_keyboard())
            elif level == 2:
                stage = int(call.data[7:8])
                bot.edit_message_text(chat_id=call.message.chat.id,
                                      text=construct_applications_header(stage),
                                      message_id=call.message.message_id
                                      )
                bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                              message_id=call.message.message_id,
                                              reply_markup=construct_applications_keyboard(get_applications_bot(stage)))

        else:
            level = int(call.data[4:len(call.data)])

            if level == 0:
                bot.edit_message_text(chat_id=call.message.chat.id,
                                      text='Меню выбора действия:',
                                      message_id=call.message.message_id
                                      )
                bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                              message_id=call.message.message_id,
                                              reply_markup=construct_main_menu_keyboard(call.message.chat.id))
        pass
    elif call.data =='2':
        applicationsKeyboard = types.InlineKeyboardMarkup()
        applications = get_applications_bot(1)
        for application in applications:
            appButton = types.InlineKeyboardButton(text=str(application["id"]), callback_data='A'+str(application["id"]))
            applicationsKeyboard.add(appButton)
        bot.send_message(call.message.chat.id, text='Заявки для обработки:', reply_markup=applicationsKeyboard)
        pass

    elif call.data =='10':


        bot.edit_message_text(chat_id=call.message.chat.id,
                              text='Выберите тип заявки для просмотра:',
                              message_id=call.message.message_id
                              )
        bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      reply_markup=construct_applications_stages_keyboard())
        pass

    # Обработка кнопки для одобрения заявки
    elif str(call.data[0:2])=='AA':
        applicationId = int(call.data[2:len(call.data)])
        set_application_accepted(applicationId)
        pass
    # Обработка кнопки для отклонения заявки
    elif str(call.data[0:2])=='DA':
        applicationId = int(call.data[2:len(call.data)])
        set_application_declined(applicationId)
        pass

    elif str(call.data[0:3])=='SPA':
        applicationId = int(call.data[3:len(call.data)])
        set_application_wip(applicationId)
        application_keyboard = construct_decision_keyboard(2, applicationId)
        bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      reply_markup=application_keyboard)

    elif str(call.data[0:2])=='WA':
        stage = int(call.data[2:len(call.data)])
        applications = get_applications_bot(stage)

        if len(applications)>0:
            text_for_keyboard = construct_applications_header(stage)

            bot.edit_message_text(chat_id=call.message.chat.id,
                                  text=text_for_keyboard,
                                  message_id=call.message.message_id
                                  )
            bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                          message_id=call.message.message_id,
                                          reply_markup=construct_applications_keyboard(applications))
        else:
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  text="Заявок выбранного типа нет!",
                                  message_id=call.message.message_id
                                  )
            bot.send_message(chat_id=call.message.chat.id, text="Выберите тип заявки для просмотра:", reply_markup=construct_applications_stages_keyboard())
        pass

    elif call.data[0] == 'A':
        applicationId=(int(call.data[1:len(call.data)]))
        application = get_application_bot(applicationId)

        bot.edit_message_text(chat_id=call.message.chat.id,
                              text=constract_application_text(application),
                              message_id=call.message.message_id,
                              parse_mode="HTML"
                              )
        bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      reply_markup=construct_decision_keyboard(application['stage'], applicationId))

    elif call.data =='3':
        petsMenuKeyboard = types.InlineKeyboardMarkup()
        addPets = types.InlineKeyboardButton(text='Добавить питомцев', callback_data='4')
        editPets = types.InlineKeyboardButton(text='Обновить информацию о питомцах', callback_data='5')
        backButton = types.InlineKeyboardButton(text='Назад', callback_data='Back0')

        petsMenuKeyboard.add(addPets)
        petsMenuKeyboard.add(editPets)
        petsMenuKeyboard.add(backButton)

        bot.edit_message_text(chat_id=call.message.chat.id,
                              text='Меню управления питомцами:',
                              message_id=call.message.message_id
                              )
        bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      reply_markup=petsMenuKeyboard)
        pet_admin_message_sequence.append(call.message.message_id)

    elif call.data == '4':
        generate_template()
        template_path = 'output/pets-data-template.xlsx'
        msg=bot.send_message(call.message.chat.id,
                         "Заполните информацию о питомцах* в прикрепленном ниже файле.\n\nПосле заполнения, для добавления питомцев, отправьте файл.\n\n*Максимально 10 питомцев за раз")
        pet_admin_message_sequence.append(msg.message_id)
        with open(template_path, 'rb') as template:
            msg=bot.send_document(call.message.chat.id, template)
            pet_admin_message_sequence.append(msg.message_id)
        bot.register_next_step_handler(call.message, receive_modified_file, "add")

    elif call.data == '5':
        get_pets_table_as_file()
        pets_table_path = "output/pets-table-file.xlsx"
        msg=bot.send_message(call.message.chat.id,
                         "После обновления информации о питомцах, отправьте мне файл.")
        pet_admin_message_sequence.append(msg.message_id)
        with open(pets_table_path, 'rb') as pets_table:
            msg=bot.send_document(call.message.chat.id, pets_table)
            pet_admin_message_sequence.append(msg.message_id)
        bot.register_next_step_handler(call.message, receive_modified_file, "edit")
        pass

def receive_modified_file(message, flag):
    pet_admin_message_sequence.append(message.message_id)
    if message.document:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        with open("output/pets-data-file.xlsx", "wb") as pets_data_file:
            pets_data_file.write(downloaded_file)
            msg=bot.send_message(message.chat.id, "Файл был успешно загружен и сохранен! Дождитесь окончания обработки файла!")
            pet_admin_message_sequence.append(msg.message_id)
            pets_data = get_pets_data_from_file()

            allow_database_write = True

            for pet_data in pets_data:
                for i in range(0, len(pet_data)):
                    if i != 6 and not pet_data[i]:
                        allow_database_write = False
                        break
            if allow_database_write:
                if flag == "add":
                    add_pets(pets_data)
                elif flag == "edit":
                    update_pets(pets_data)
                flush_message_sequence(pet_admin_message_sequence, message.chat.id)
                pet_admin_message_sequence.clear()
                bot.send_message(message.from_user.id, text='Меню выбора действия:',
                                 reply_markup=construct_main_menu_keyboard(message.from_user.id))
            else:
                msg=bot.send_message(message.chat.id, "Перед отправкой файла, убедитесь что все поля о питомце, кроме альбома, заполены! И прикрепите файл еще раз.")
                pet_admin_message_sequence.append(msg.message_id)
                bot.register_next_step_handler(message, receive_modified_file, flag)
    else:
        msg=bot.send_message(message.chat.id, "Пожалуйста, прикрепите заполненный файл в формате документа.")
        pet_admin_message_sequence.append(msg.message_id)
        bot.register_next_step_handler(message, receive_modified_file, flag)

while True:
    try:
        bot.infinity_polling(timeout=10, long_polling_timeout=5)
    except Exception as e:
        print(f"Error occurred: {e}")
        time.sleep(15)  # Ждем перед повторным запуском

from pydoc import describe

import db_connector

def get_pets():
    conn = db_connector.connect()
    cursor = conn.cursor()
    cursor.callproc('get_pets', )

    pets = []
    for row in cursor.fetchall():
        pet = {
            "id": row[0],
            "id_type": row[1],
            "name": row[2],
            "age": row[3],
            "sex": row[4],
            "fertility": row[5],
            "img": row[6],
            "type": row[7],
            "status": row[8],
            "description": row[9]
        }
        pets.append(pet)
    cursor.close()
    conn.close()

    return pets

def get_fav_pets(id_user):
    conn = db_connector.connect()
    cursor = conn.cursor()
    cursor.callproc('get_fav_pets', [id_user, ])

    pets = []
    for row in cursor.fetchall():
        pet = {
            "id": row[0],
            "id_type": row[1],
            "name": row[2],
            "age": row[3],
            "sex": row[4],
            "fertility": row[5],
            "img": row[6],
            "type": row[7],
            "status": row[8],
            "description": row[9]
        }
        pets.append(pet)
    cursor.close()
    conn.close()

    return pets

def get_pets_by_type(id_type):
    conn = db_connector.connect()
    cursor = conn.cursor()
    cursor.callproc('get_pets', [id_type, ])

    pets = []
    for row in cursor.fetchall():
        pet = {
            "id": row[0],
            "id_type": row[1],
            "name": row[2],
            "age": row[3],
            "sex": row[4],
            "fertility": row[5],
            "img": row[6]
        }
        pets.append(pet)
    cursor.close()
    conn.close()

    return pets

def get_pet(id_pet):
    conn = db_connector.connect()
    cursor = conn.cursor()
    cursor.callproc('get_pet', [id_pet, ])
    row = cursor.fetchone()
    if row:
        pet = {
            "id": row[0],
            "id_type": row[1],
            "name": row[2],
            "age": row[3],
            "sex": row[4],
            "fertility": row[5],
            "description": row[6],
            "album": row[7],
            "id_status": row[8]
        }
    else:
        pet = None
    cursor.close()
    conn.close()
    return pet

def get_pet_types():
    conn = db_connector.connect()
    cursor = conn.cursor()
    cursor.callproc('get_pet_types', )

    pet_types = []

    for row in cursor.fetchall():
        pet_types.append(row[0])

    cursor.close()
    conn.close()
    return pet_types

def get_pet_statuses():
    conn = db_connector.connect()
    cursor = conn.cursor()
    cursor.callproc('get_pet_statuses', )

    pet_statuses = []

    for row in cursor.fetchall():
        pet_statuses.append(row[0])

    cursor.close()
    conn.close()
    return pet_statuses

def add_pets(pets_data):
    conn = db_connector.connect()
    cursor = conn.cursor()

    for pet_data in pets_data:

         type = pet_data[0]
         status = pet_data[1]
         name = pet_data[2]
         sex = pet_data[3]
         age = pet_data[4]
         fertility = pet_data[5]
        #  if len(pet_data[6])==0:
        #     pet_data[6]=None
         id_album = pet_data[6]
         description = pet_data[7]

         cursor.callproc('add_pet', [type, status, name, sex, age, fertility, id_album, description])
    conn.commit()
    cursor.close()
    conn.close()

def update_pets(pets_data):
    conn = db_connector.connect()
    cursor = conn.cursor()

    for pet_data in pets_data:

        id = pet_data[0]
        type = pet_data[1]
        status = pet_data[2]
        name = pet_data[3]
        sex = pet_data[4]
        age = pet_data[5]
        # if len(pet_data[6]) == 0 or pet_data[6] == None:
            # pet_data[6] = None
        id_album = pet_data[6]
        fertility = pet_data[7]
        description = pet_data[8]

        cursor.callproc('update_pet', [id, type, status, name, sex, age, id_album, fertility, description])
    conn.commit()
    cursor.close()
    conn.close()

    pass

def add_pet_to_favorites(id_pet, id_user):
    conn = db_connector.connect()
    cursor = conn.cursor()
    cursor.callproc('add_pet_to_favorites', [id_pet, id_user])
    conn.commit()
    cursor.close()
    conn.close()
    pass

def remove_pet_from_favorites(id_pet, id_user):
    conn = db_connector.connect()
    cursor = conn.cursor()
    cursor.callproc('remove_pet_from_favorites', [id_pet, id_user])
    conn.commit()
    cursor.close()
    conn.close()
    pass

def is_pet_on_favorites(id_pet, id_user):
    pet_is_on_list = False
    conn = db_connector.connect()
    cursor = conn.cursor()
    cursor.callproc('is_on_favorites', [id_pet, id_user])

    count = cursor.fetchone()
    if count[0] > 0:
        pet_is_on_list = True

    cursor.close()
    conn.close()
    return pet_is_on_list
    pass

def is_there_application(id_pet, id_user):
    there_is_application = False
    conn = db_connector.connect()
    cursor = conn.cursor()
    cursor.callproc('is_there_application', [id_pet, id_user])

    count = cursor.fetchone()
    if count[0] > 0:
        there_is_application = True

    cursor.close()
    conn.close()
    return there_is_application

def is_pet_archived(id_pet):
    pet_archived = False
    conn = db_connector.connect()
    cursor = conn.cursor()
    cursor.callproc('is_pet_archived', [id_pet])

    count = cursor.fetchone()
    if count[0] > 0:
        pet_archived = True

    cursor.close()
    conn.close()
    return pet_archived

def get_applications(id_user):
    conn = db_connector.connect()
    cursor = conn.cursor()
    cursor.callproc('get_aplications', [id_user, ])

    aplications = []
    for row in cursor.fetchall():
        aplication = {
            "id": row[0],
            "id_type": row[1],
            "name": row[2],
            "age": row[3],
            "sex": row[4],
            "fertility": row[5],
            "img": row[6],
            "type": row[7],
            "status": row[8],
            "description": row[9],
            "id_aplication" : row[10],
            "aplication_status" : row[11],
            "aplication_description": row[12],
            "aplication_stage" : row[13]
        }
        aplications.append(aplication)
    cursor.close()
    conn.close()

    return aplications

def get_applications_bot(stage):
    conn = db_connector.connect()
    cursor = conn.cursor()
    cursor.callproc('get_applications_bot', [stage, ])
    applications = []
    for row in cursor.fetchall():
        application = {
            "id": row[0]
        }
        applications.append(application)
    cursor.close()
    conn.close()
    return applications

def get_application_bot(id_application):
    conn = db_connector.connect()
    cursor = conn.cursor()
    cursor.callproc('get_application_bot', [id_application, ])
    row = cursor.fetchone()  # Получаем только одну строку из результата
    if row:
        application = {
            "id_application": row[0],
            "id_pet": row[1],
            "id_user": row[2],
            "name": row[3],
            "age": row[4],
            "sex": row[5],
            "album_link": row[6],
            "stage": row[7]
        }
    else: application = None
    cursor.close()
    conn.close()
    return application

    pass

def create_application(id_pet, id_user):
    conn = db_connector.connect()
    cursor = conn.cursor()
    cursor.callproc('create_application', [id_pet, id_user])
    conn.commit()
    cursor.close()
    conn.close()
    pass

def cancel_application(id_application):
    conn = db_connector.connect()
    cursor = conn.cursor()
    cursor.callproc('cancel_application', [id_application, ])
    conn.commit()
    cursor.close()
    conn.close()
    pass

def set_application_wip(id_application):
    conn = db_connector.connect()
    cursor = conn.cursor()
    cursor.callproc('update_application_stage', [id_application, 2, 2, 2])
    conn.commit()
    cursor.close()
    conn.close()
    pass

def set_application_accepted(id_application):
    conn = db_connector.connect()
    cursor = conn.cursor()
    cursor.callproc('update_application_stage', [id_application, 3, 4, 2])
    conn.commit()
    cursor.close()
    conn.close()
    pass

def set_application_declined(id_application):
    conn = db_connector.connect()
    cursor = conn.cursor()
    cursor.callproc('update_application_stage', [id_application, 3, 5, 1])
    conn.commit()
    cursor.close()
    conn.close()
    pass

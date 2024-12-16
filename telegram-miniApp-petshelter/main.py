from crypt import methods
from concurrent.futures import ThreadPoolExecutor
import load_gallery
from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy

import os
from dotenv import load_dotenv
load_dotenv()

import db_calls
from db_calls import get_pets, get_pet, get_pets_by_type, add_pet_to_favorites, remove_pet_from_favorites, \
    is_pet_on_favorites, get_fav_pets, get_applications, create_application, is_there_application, cancel_application
from load_gallery import get_images

app = Flask(__name__)


@app.route('/add_to_favorites', methods=['POST'])
def add_to_favorites():
    id_pet = request.args.get('id_pet')
    id_user = request.args.get('id_user')
    add_pet_to_favorites(id_pet, id_user)
    pass


@app.route('/remove_from_favorites', methods=['POST'])
def remove_from_favorites():
    id_pet = request.args.get('id_pet')
    id_user = request.args.get('id_user')
    remove_pet_from_favorites(id_pet, id_user)
    pass

@app.route('/create_application', methods=['POST'])
def call_create_application():
    id_pet = request.args.get('id_pet')
    id_user = request.args.get('id_user')

    if not id_pet or not id_user:
        return jsonify({"error": "id_pet and id_user are required"}), 400

    try:
        create_application(id_pet, id_user)
        return jsonify({"success": True, "id_pet": id_pet, "id_user": id_user}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/cancel_application', methods=['POST'])
def call_cancel_application():
    id_application = request.args.get('id_application')
    if not id_application:
        return jsonify({"error": "id_application is required"}), 400
    try:
        cancel_application(id_application)
        return jsonify({"success": True, "id_application": id_application}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Главная страница
@app.route('/')
def index():
    return render_template('base.html')

# API для контента на страницах
@app.route('/content/<page>')
def get_content(page):
    id_pet=request.args.get('id_pet')
    id_pet_type=request.args.get('id_pet_type')
    id_user = request.args.get('id_user')
    page_num = request.args.get('page_num', 1, type=int)
    if page == 'home':
        content = render_template('index.html')
    elif page == 'pets' and id_pet:
        application_status = is_there_application(id_pet, id_user)
        fav_pet = is_pet_on_favorites(id_pet, id_user)
        pet = get_pet(id_pet)
        pet_album=get_images(pet["id_type"], pet["album"])
        content = render_template('pet.html')
        return jsonify(content=content, pet_info=pet, pet_album=pet_album, fav_pet=fav_pet, application_status=application_status)
    elif page == 'pets' and id_pet_type:
        pets = get_pets_by_type(id_pet_type)
        page_num = request.args.get('page_num', 1, type=int)
        items_per_page = 5

        start = (page_num - 1) * items_per_page
        end = start + items_per_page
        paginated_pets = pets[start:end]

        with ThreadPoolExecutor(max_workers=6) as executor:
            futures = [executor.submit(get_images, pet["id_type"], pet["img"])  for pet in paginated_pets]
            for pet, future in zip(paginated_pets, futures):
                pet["img"] = future.result()[0]

        total_pages = len(pets) // items_per_page + (1 if len(pets) % items_per_page > 0 else 0)
        has_prev = page_num > 1
        has_next = page_num < total_pages

        content = render_template('pets.html', pets=paginated_pets)
        return jsonify(
            content=content,
            pagination={
                'page_num': page_num,
                'total_pages': total_pages,
                'has_prev': has_prev,
                'has_next': has_next,
            },
            pets=paginated_pets,
            id_pet_type=id_pet_type
        )

    # Добавляем разбивку на стриницы

    elif page == 'pets':
        pets = get_pets()
        page_num = request.args.get('page_num', 1, type=int)
        items_per_page = 5

        start = (page_num - 1) * items_per_page
        end = start + items_per_page
        paginated_pets = pets[start:end]

        with ThreadPoolExecutor(max_workers=6) as executor:
            futures = [executor.submit(get_images, pet["id_type"], pet["img"])  for pet in paginated_pets]
            for pet, future in zip(paginated_pets, futures):
                pet["img"] = future.result()[0]

        total_pages = len(pets) // items_per_page + (1 if len(pets) % items_per_page > 0 else 0)
        has_prev = page_num > 1
        has_next = page_num < total_pages

        content = render_template('pets.html', pets=paginated_pets)
        return jsonify(
            content=content,
            pagination={
                'page_num': page_num,
                'total_pages': total_pages,
                'has_prev': has_prev,
                'has_next': has_next,
            },
            pets=paginated_pets
        )

    elif page == 'likes' and id_pet:
        application_status = is_there_application(id_pet, id_user)
        fav_pet = is_pet_on_favorites(id_pet, id_user)
        pet = get_pet(id_pet)
        pet_album=get_images(pet["id_type"], pet["album"])
        content = render_template('pet.html')
        return jsonify(content=content, pet_info=pet, pet_album=pet_album, fav_pet=fav_pet, application_status=application_status)

    elif page == 'likes':
        id_user = request.args.get('id_user')
        pets = get_fav_pets(id_user)
        page_num = request.args.get('page_num', 1, type=int)
        items_per_page = 5

        start = (page_num - 1) * items_per_page
        end = start + items_per_page
        paginated_pets = pets[start:end]

        with ThreadPoolExecutor(max_workers=6) as executor:
            futures = [executor.submit(get_images, pet["id_type"], pet["img"])  for pet in paginated_pets]
            for pet, future in zip(paginated_pets, futures):
                pet["img"] = future.result()[0]

        total_pages = len(pets) // items_per_page + (1 if len(pets) % items_per_page > 0 else 0)
        has_prev = page_num > 1
        has_next = page_num < total_pages

        content = render_template('pets.html', pets=paginated_pets)
        return jsonify(
            content=content,
            pagination={
                'page_num': page_num,
                'total_pages': total_pages,
                'has_prev': has_prev,
                'has_next': has_next,
            },
            pets=paginated_pets
        )

    elif page == 'applications' and id_pet:
        application_status = is_there_application(id_pet, id_user)
        fav_pet = is_pet_on_favorites(id_pet, id_user)
        pet = get_pet(id_pet)
        pet_album = get_images(pet["id_type"], pet["album"])
        content = render_template('pet.html')
        return jsonify(content=content, pet_info=pet, pet_album=pet_album, fav_pet=fav_pet, application_status=application_status)

    elif page == 'applications':
        id_user = request.args.get('id_user')
        applications = get_applications(id_user)
        page_num = request.args.get('page_num', 1, type=int)
        items_per_page = 5

        start = (page_num - 1) * items_per_page
        end = start + items_per_page
        paginated_applications = applications[start:end]

        with ThreadPoolExecutor(max_workers=6) as executor:
            futures = [executor.submit(get_images, pet["id_type"], pet["img"]) for pet in paginated_applications]
            for pet, future in zip(paginated_applications, futures):
                pet["img"] = future.result()[0]

        total_pages = len(applications) // items_per_page + (1 if len(applications) % items_per_page > 0 else 0)
        has_prev = page_num > 1
        has_next = page_num < total_pages

        content = render_template('applications.html', pets=paginated_applications)
        return jsonify(
            content=content,
            pagination={
                'page_num': page_num,
                'total_pages': total_pages,
                'has_prev': has_prev,
                'has_next': has_next,
            },
            applications=paginated_applications
        )
    else:

        content = "<h2>Страница не найдена</h2>"

    return jsonify(content=content)

if __name__ == '__main__':
    appDomain = os.getenv('appDomain')
    app.run(ssl_context=(f'/etc/letsencrypt/live/'+appDomain+'/fullchain.pem',
                     f'/etc/letsencrypt/live/'+appDomain+'/privkey.pem'),
        host='0.0.0.0', port=5000)


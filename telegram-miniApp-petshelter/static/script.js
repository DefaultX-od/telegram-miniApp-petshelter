let page_current_num = 0;
let pet_current_type = 0;
let page_current;

function loadContent(page, id_pet = null, id_pet_type = null, page_num = null) {

    if (document.getElementById('page-controls1')) {
        document.getElementById('page-controls1').innerHTML = '';
        document.getElementById('page-controls1').style.display = 'none';
    }
    document.getElementById('content').style.display = 'none';
    document.getElementById('loading').style.display = 'flex';

    updateIcons(page);
    updatePageHeader(page);

    if (id_pet_type !== null) pet_current_type = id_pet_type;
    if (page_num !== null) page_current_num = page_num;

    let url = `/content/${page}`;
    if (id_pet) {
        url += `?id_pet=${id_pet}`;
        url += `&id_user=${window.Telegram.WebApp.initDataUnsafe.user?.id}`;
        console.log(id_pet);
        document.getElementById('page-controls').innerHTML = '';
    }
    else if (page == 'likes') {
        url += `?id_user=${window.Telegram.WebApp.initDataUnsafe.user?.id}`;
        if (page_num) {
            url += `&page_num=${page_num}`;
            console.log(page_num);
        }
    }
    else if (page == 'applications') {
        url += `?id_user=${window.Telegram.WebApp.initDataUnsafe.user?.id}`;
        if (page_num) {
            url += `&page_num=${page_num}`;
            console.log(page_num);
        }
    }
    else if (id_pet_type) {
        url += `?id_pet_type=${id_pet_type}`;
        console.log(id_pet_type);
        const pageTitle = document.getElementById("app-page-title");

        if (id_pet_type == 2) {
            pageTitle.textContent = "Кошки";
        }
        else if (id_pet_type == 3) {
            pageTitle.textContent = "Собаки";
        }
        if (page_num) {
            url += `&page_num=${page_num}`;
            console.log(page_num);
        }
    }

    else if (page_num) {
        url += `?page_num=${page_num}`;
        console.log(page_num);
    }


    console.log(url);

    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Сетевая ошибка: ' + response.statusText); // Если ответ не успешный
            }
            return response.json(); // Пытаемся парсить JSON
        })
        .then(data => {

            document.getElementById('content').innerHTML = data.content;
            document.getElementById('loading').style.display = 'none';
            document.getElementById('content').style.display = 'flex';

            // Инициализация галереи с изображениями
            if (data.pet_info && data.pet_album) {
                document.getElementById('page-controls').innerHTML = '';

                const album = data.pet_album;
                const pet = data.pet_info;
                const fav_pet = data.fav_pet;
                const pet_status = pet.id_status;

                initializeGallery(album);
                console.log(pet);
                loadPetCard(pet);

                const backButton = document.getElementById('header-icon');
                const backButtonIcon = document.getElementById('icon');

                backButtonIcon.src = 'static/img/left-arrow.png';
                backButton.onclick = () => loadContent(page, null, pet_current_type, page_current_num);


                //функция управления избранными питомцами пользователя
                document.getElementById('page-controls1').style.display = 'flex';

                const likeButton = document.createElement('div');
                const btnImg = document.createElement('img');
                const favStatus = data.fav_pet;
                const applicationStatus = data.application_status;

                btnImg.src = favStatus ? 'static/img/like-active.png' : 'static/img/like.png';
                btnImg.className = 'icon';
                likeButton.appendChild(btnImg);

                likeButton.onclick = favStatus
                    ? () => removePetFromFavorites(data.pet_info.id, window.Telegram.WebApp.initDataUnsafe.user?.id)
                    : () => addPetToFavorites(data.pet_info.id, window.Telegram.WebApp.initDataUnsafe.user?.id);

                document.getElementById('page-controls1').appendChild(likeButton);

                if (applicationStatus) {
                    const createApplicationBtn = document.getElementById('create_application');
                    createApplicationBtn.textContent = "Вы уже подали заявку!";
                    createApplicationBtn.onclick = null;
                    createApplicationBtn.style.pointerEvents = 'none';
                    createApplicationBtn.style.opacity = '0.6';
                }
                else if(pet_status === 2){
                    const createApplicationBtn = document.getElementById('create_application');
                    createApplicationBtn.textContent = "Питомец в архиве!";
                    createApplicationBtn.onclick = null;
                    createApplicationBtn.style.pointerEvents = 'none';
                    createApplicationBtn.style.opacity = '0.6';
                }
                else {
                    document.getElementById('create_application').onclick = () => createApplication(data.pet_info.id, window.Telegram.WebApp.initDataUnsafe.user?.id);
                }
            }


            if (data.pets && data.id_pet_type) {
                loadPetCards(data.pets, page);
                updatePaginationControls(data.pagination, page, data.id_pet_type);
            }
            else if (data.pets) {
                loadPetCards(data.pets, page);
                pet_current_type = null;
                updatePaginationControls(data.pagination, page);
            }
            else if (data.applications) {
                loadApplicationsCards(data.applications, page);
                updatePaginationControls(data.pagination, page);
            }
            else {
                document.getElementById('page-controls').innerHTML = '';
            }
        })
        .catch(error => {
            console.error('Ошибка загрузки контента:', error);
            document.getElementById('loading').style.display = 'none';
            document.getElementById('content').style.display = 'flex';
            // Можно отобразить сообщение об ошибке пользователю
            document.getElementById('content').innerHTML = "<h2>Произошла ошибка при загрузке контента. Попробуйте еще раз.</h2>";
        });


}

function updateFavoriteButton(id_pet, id_user, isFavorite) {
    const pageControls = document.getElementById('page-controls1');
    if (pageControls) {
        pageControls.style.display = 'flex';
        pageControls.innerHTML = '';  // Очищаем содержимое перед добавлением новой кнопки

        const likeButton = document.createElement('div');
        const btnImg = document.createElement('img');
        btnImg.src = isFavorite ? 'static/img/like-active.png' : 'static/img/like.png';
        btnImg.className = 'icon';
        likeButton.appendChild(btnImg);

        likeButton.onclick = isFavorite
            ? () => removePetFromFavorites(id_pet, id_user)
            : () => addPetToFavorites(id_pet, id_user);

        pageControls.appendChild(likeButton);
    } else {
        console.error("Element 'page-controls1' not found.");
    }
}

function disableButton(btnName, btnText){
    const btn = document.getElementById(btnName);
    btn.textContent = btnText;
    btn.onclick = null;
    btn.style.pointerEvents = 'none';
    btn.style.opacity = '0.6';
}

function createApplication(id_pet, id_user) {
    disableButton(btnName = 'create_application', btnText = "Вы уже подали заявку!");
    fetch(`/create_application?id_pet=${id_pet}&id_user=${id_user}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
        .then(response => {
            if (!response.ok) {
                const createApplicationBtn = document.getElementById('create_application');
                createApplicationBtn.textContent = "Принять в семью!";
                createApplicationBtn.onclick = createApplication(id_pet, id_user);
                createApplicationBtn.style.opacity = '1';
                return response.json().then(data => {
                    throw new Error(data.error || 'Неизвестная ошибка');                    
                });
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                console.log(`Заявка для пользователя с id: ${id_user} и питомца с id: ${id_pet} успешно создана.`);
                disableButton(btnName = 'create_application', btnText = "Вы уже подали заявку!");
            }
        })
        .catch(error => {
            console.error('Ошибка при создании заявки:', error.message);
            alert(`Ошибка: ${error.message}`);
        });
}


function cancelApplication(id_application) {
    disableButton(btnName=`cancel-btn${id_application}`,btnText='Отмена...');
    fetch(`/cancel_application?id_application=${id_application}`, {
        method: 'POST'
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Ошибка отмены заявки');
            }
            // Убираем заявку из DOM
            const applicationCard = document.querySelector(`#cancel-btn${id_application}`).closest('.application-card');
            if (applicationCard) {
                applicationCard.remove();
            }
            loadContent("applications", null, null, page_current_num)
        })
        .catch(error => {
            console.error('Ошибка отмены заявки:', error);
            alert('Не удалось отменить заявку. Попробуйте снова.');
        });
}

function addPetToFavorites(id_pet, id_user) {
    fetch(`/add_to_favorites?id_pet=${id_pet}&id_user=${id_user}`, {
        method: 'POST'
    })
        .catch(error => console.error('Error:', error));

    console.log(`Для пользователя с id: ${id_user} в избранное будет добавлен питомец с id: ${id_pet}`);
    updateFavoriteButton(id_pet, id_user, true);  // Обновляем кнопку как добавленную в избранное
}

function removePetFromFavorites(id_pet, id_user) {
    fetch(`/remove_from_favorites?id_pet=${id_pet}&id_user=${id_user}`, {
        method: 'POST'
    })
        .catch(error => console.error('Error:', error));

    console.log(`Для пользователя с id: ${id_user} из избранного будет удален питомец с id: ${id_pet}`);
    updateFavoriteButton(id_pet, id_user, false);  // Обновляем кнопку как удаленную из избранного
}

function updatePaginationControls(pagination, page, id_pet_type = null) {
    const pageControls = document.getElementById('page-controls');
    pageControls.innerHTML = '';  // Очищаем текущие кнопки

    // Кнопка "Previous"
    if (pagination.has_prev) {
        const prevButton = document.createElement('div');
        const btnImg = document.createElement('img');
        btnImg.src = 'static/img/left-arrow.png';
        btnImg.className = 'icon';
        prevButton.appendChild(btnImg);
        prevButton.onclick = () => loadContent(page, null, id_pet_type, pagination.page_num - 1);
        pageControls.appendChild(prevButton);
    }

    // Кнопка "Next"
    if (pagination.has_next) {
        const nextButton = document.createElement('div');
        const btnImg = document.createElement('img');
        btnImg.src = 'static/img/right-arrow.png';
        btnImg.className = 'icon';
        nextButton.appendChild(btnImg);
        nextButton.onclick = () => loadContent(page, null, id_pet_type, pagination.page_num + 1);
        pageControls.appendChild(nextButton);
    }

    page_current_num = pagination.page_num;
}

function loadPetCard(pet) {

    const pageTitle = document.getElementById("app-page-title");

    pageTitle.textContent = pet.name;

    const petCard = document.getElementById("pet-card-info");


    const petCardInfoPart1 = document.getElementById("pet-card-info-part1")

    const petInfoPart1 = document.createElement("div");
    petInfoPart1.className = "pet-info";


    petCardInfoPart1.innerHTML = '';


    petInfoPart1.innerHTML = `
                <p><h3>Основная информация</h3></p>
                <p><strong>Кличка:</strong> ${pet.name}</p>
                <p><strong>Возраст:</strong> ${pet.age} года</p>
                <p><strong>Пол:</strong> ${pet.sex}</p>
                <p><strong>Фертильность:</strong> ${pet.fertility}</p>
        `;
    petCardInfoPart1.appendChild(petInfoPart1);

    const petCardInfoPart2 = document.getElementById("pet-card-info-part2")

    const petInfoPart2 = document.createElement("div");
    petInfoPart2.className = "pet-info";
    petCardInfoPart2.innerHTML = '';

    petInfoPart2.innerHTML = `
                <p><h3>Описание:</h3></p>
                <p>${pet.description}</p>
        `;
    petCardInfoPart2.appendChild(petInfoPart2);
}

function loadPetCards(pets, page) {
    const cardsHolder = document.getElementById("cards-holder")
    cardsHolder.innerHTML = '';

    if (pets.length > 0) {
        pets.forEach(pet => {
            const petCard = document.createElement("div");
            petCard.className = "pet-card";

            const petImage = document.createElement("img");
            petImage.src = pet.img;
            petImage.className = "pet-image";
            petImage.referrerPolicy = "no-referrer";

            const petInfo = document.createElement("div");
            petInfo.className = "pet-info";
            petCard.onclick = () => loadContent(page, pet.id);
            petInfo.innerHTML = `
                <p><strong>Кличка:</strong> ${pet.name}</p>
                <p><strong>Возраст:</strong> ${pet.age} года</p>
                <p><strong>Пол:</strong> ${pet.sex}</p>
                <p><strong>Фертильность:</strong> ${pet.fertility}</p>
        `;
            petCard.appendChild(petImage);
            petCard.appendChild(petInfo);
            cardsHolder.appendChild(petCard);
        });
    }
    else {
        cardsHolder.textContent = "Здесь пока пусто!";
    }
}

function loadApplicationsCards(applications, page) {
    const cardsHolder = document.getElementById("cards-holder");
    cardsHolder.innerHTML = ''; // Очищаем контейнер перед загрузкой новых карточек

    if (applications.length > 0) {
        applications.forEach(application => {
            // Создаем карточку заявки
            const applicationCard = document.createElement("div");
            applicationCard.className = "application-card";

            // Верхняя часть карточки с ID и кнопкой отмены
            const applicationInfo = document.createElement("div");
            applicationInfo.className = "application-info";
            applicationInfo.innerHTML = `
                <p><strong>№ ${application.id_aplication}</strong></p>
            `;

            const isRejected = application.aplication_status.toLowerCase() === "отклонена";
            if (!isRejected) {
                const cancelBtn = document.createElement("div");
                cancelBtn.className = "cancel-btn";
                cancelBtn.textContent = "Отменить";
                cancelBtn.id = `cancel-btn${application.id_aplication}`;
                cancelBtn.onclick = () => cancelApplication(application.id_aplication);
                applicationInfo.appendChild(cancelBtn);
            }


            applicationCard.appendChild(applicationInfo);

            // Карточка питомца
            const petCard = document.createElement("div");
            petCard.className = "pet-card";
            petCard.style.cssText = "background-color: #F7F7F7; box-shadow: none;";
            petCard.onclick = () => loadContent(page, application.id); // Обработчик нажатия

            const petImage = document.createElement("img");
            petImage.src = application.img;
            petImage.className = "pet-image";
            petImage.referrerPolicy = "no-referrer";

            const petInfo = document.createElement("div");
            petInfo.className = "pet-info";
            petInfo.innerHTML = `
                <p><strong>Кличка:</strong> ${application.name}</p>
                <p><strong>Возраст:</strong> ${application.age} года</p>
                <p><strong>Пол:</strong> ${application.sex}</p>
                <p><strong>Фертильность:</strong> ${application.fertility}</p>
            `;

            petCard.appendChild(petImage);
            petCard.appendChild(petInfo);

            applicationCard.appendChild(petCard);

            // Детали заявки
            const details = document.createElement("details");
            details.style.cssText = "margin-bottom: 5px; margin-top: 5px;";
            
            const stageIcons = [...Array(3)].map((_, index) => {
                const isPassed = index < application.aplication_stage;
                const isCurrentStage = index === application.aplication_stage; // Текущая стадия
                const isFinalStage = index === 2;

                // Если заявка отклонена, использовать иконку "отклонена" для текущей стадии или финальной
                const iconSrc = isRejected && (isCurrentStage || isFinalStage)
                    ? "static/img/stage-rejected.svg"
                    : isPassed
                        ? "static/img/stage-passed.svg"
                        : "static/img/stage.svg";

                const connector = index < 2
                    ? '<div style="width: 50%; margin-left: -7px; margin-right: -7px; height: 3px; background-color: #B2B2B2;"></div>'
                    : "";

                return `
        <img src="${iconSrc}" class="status-icon">
        ${connector}
    `;
            }).join('');

            details.innerHTML = `
                <summary><strong>${application.aplication_status}</strong></summary>
                <div class="application-info" style="justify-content: center; align-items: center;">
                    ${stageIcons}
                </div>
                <div class="application-info" style="text-align: center;">
                    <p>${application.aplication_stage === 1 ? "<strong>Создана</strong>" : "Создана"}</p>
                    <p>${application.aplication_stage === 2 ? "<strong>Обработка</strong>" : "Обработка"}</p>
                    <p>${application.aplication_stage === 3 ? "<strong>Решение</strong>" : "Решение"}</p>
                </div>
            `;

            applicationCard.appendChild(details);
            cardsHolder.appendChild(applicationCard);
        });
    }
    else {
        cardsHolder.textContent = "Здесь пока пусто!";
    }
}

function updateIcons(activePage) {
    // Сначала сбросим все иконки к неактивному состоянию
    const icons = {
        home: {
            header: "img/home.png",
            footer: "img/home.png"
        },
        pets: {
            header: "img/pets.png",
            footer: "img/pets.png"
        },
        likes: {
            header: "img/likes.png",
            footer: "img/likes.png"
        },
        applications: {
            header: "img/applications.png",
            footer: "img/applications.png"
        }
    };

    // Устанавливаем активную иконку для выбранной страницы
    icons[activePage].header = `img/${activePage}-active.png`;
    icons[activePage].footer = `img/${activePage}-active.png`;

    // Обновляем иконки в header и footer
    document.querySelector(".header-icon img").src = `static/${icons[activePage].header}`;
    document.getElementById("home-icon").src = `static/${icons.home.footer}`;
    document.getElementById("pets-icon").src = `static/${icons.pets.footer}`;
    document.getElementById("likes-icon").src = `static/${icons.likes.footer}`;
    document.getElementById("applications-icon").src = `static/${icons.applications.footer}`;

    document.getElementById("header-icon").onclick = () => null;
}

function updatePageHeader(activePage) {

    const pageTitle = document.getElementById("app-page-title");

    // Устанавливаем текст в зависимости от активной страницы
    if (activePage === "home") {
        pageTitle.textContent = "Главная";
    } else if (activePage === "pets") {
        pageTitle.textContent = "Питомцы";
    } else if (activePage === "likes") {
        pageTitle.textContent = "Избранное";
    } else if (activePage === "applications") {
        pageTitle.textContent = "Заявки";
    }
}

let currentIndex = 0;

function initializeGallery(imageUrls) {
    const gallery = document.getElementById("gallery");
    gallery.innerHTML = ''; // Очистка предыдущего контента

    imageUrls.forEach(url => {
        const galleryItem = document.createElement("div");
        galleryItem.className = "gallery-item"; // Класс контейнера для изображения

        const img = document.createElement("img");
        img.src = url;
        img.className = "gallery-image"; // Класс для изображения
        img.referrerPolicy = "no-referrer";
        img.alt = "Imgur Image";

        galleryItem.appendChild(img);
        gallery.appendChild(galleryItem);
    });

    const totalImages = gallery.children.length;

    // Создаем элемент для отображения текущего индекса и общего числа изображений
    const imageCounter = document.getElementById("image-counter");
    imageCounter.innerText = `1 из ${totalImages}`; // Изначально отображаем "1 из X"

    updateButtonsVisibility();
    currentIndex = 0;
    updateImageCounter();
}

function updateImageCounter() {
    const totalImages = document.querySelector('.gallery').children.length;
    const imageCounter = document.querySelector('.image-counter');
    imageCounter.innerText = `${currentIndex + 1} из ${totalImages}`; // Обновляем текст
}

function updateButtonsVisibility() {
    const prevBtn = document.querySelector('.prev-btn');
    const nextBtn = document.querySelector('.next-btn');
    const totalImages = document.querySelector('.gallery').children.length;

    // Показываем или скрываем кнопки в зависимости от количества изображений
    if (totalImages <= 1) {
        prevBtn.style.display = 'none'; // Скрыть кнопку "Назад"
        nextBtn.style.display = 'none'; // Скрыть кнопку "Вперед"
    } else {
        prevBtn.style.display = 'block'; // Показать кнопку "Назад"
        nextBtn.style.display = 'block'; // Показать кнопку "Вперед"
    }
}

function showImage(index) {
    const gallery = document.querySelector('.gallery');
    const totalImages = gallery.children.length;

    if (index >= totalImages) {
        currentIndex = 0;
    } else if (index < 0) {
        currentIndex = totalImages - 1;
    } else {
        currentIndex = index;
    }
    gallery.style.transform = `translateX(${-currentIndex * 100}%)`;
    updateImageCounter();
}

function nextImage() {
    showImage(currentIndex + 1);

    console.log(currentIndex);
}

function prevImage() {
    showImage(currentIndex - 1);

    console.log(currentIndex);
}

document.addEventListener("DOMContentLoaded", function () {
    if (window.Telegram && window.Telegram.WebApp) {
        const userId = window.Telegram.WebApp.initDataUnsafe.user?.id;
        console.log("Идентификатор пользователя:");
        console.log(userId);
        // document.getElementById('page-controls').innerHTML = userId ? `User ID: ${userId}` : "User ID not available.";
    } else {
        console.error("Telegram Web App not available. Make sure to open the app in Telegram.");
    }
});
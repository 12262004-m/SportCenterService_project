# Разработка микросервисной архитектуры "Администрирование спортивного комплекса"
Дисциплина: "Проектирование информационных систем" <br>
Состав команды: Шабарина М.А, Махоткина Е.Д, Терёшкина Н.А, Гусейнова М.Э, Лазебный В.В

## 📝 Описание: 
Cистема предназначена для администрирования спортивного комплекса, она обеспечивает учет данных о секциях, тренерах, учениках и расписании тренировок. Спортивный комплекс включает в себя залы для разных видов спорта.
Архитектура построена по принципам **микросервисности** и использует **GraphQL** в качестве основного протокола взаимодействия между клиентом и сервисами.

Проект разделён на независимые микросервисы, каждый из которых отвечает за свой домен:
- **Coaches and Sportsmen Service** — управление тренерами и спортсменами
- **Sections Service** — управление секциями, видами спорта, расписанием и спортзалами
- **Schedule Service** — управление расписанием
- **Auth Service** — регистрация и базовая авторизация пользователей
- **GraphQL Gateway** — объединяет все сервисы в единую GraphQL-схему

Также реализован интерфейс администратора для работы с данными, с возможностью добавления, редактирования и фильтрации информации:
- Главная страница (/). Информационный раздел о СШОР. Отображение расписание на сегодняшнюю дату.
- Секции (/sections). Отображение всех спортивных секций, информация о тренерах, количестве мест, списке спортсменов. Возможность добавления спортсмена в секцию и удаления.
- Спортсмены (/sportsmen). Полный список зарегистрированных спортсменов. Возможность добавления нового спортсмена, редактирования данных.
- Тренеры (/coaches). Управление списком тренеров, добавление нового тренера.
- Расписание (/schedule). Интерфейс для просмотра расписания на неделю, опция фильтрации расписания по тренерам.


## 💻 Технологии
- Python
- FastAPI
- Strawberry (GraphQL для Python)
- PostgreSQL
- Vue JS


## 🚀 Запуск проекта
1. Установить зависимости
   ```
   pip install -r requirements.txt
   ```
2. Поднять сервер бэкенда. Доступ к песочнице GraphQL для проверки mutations и query распологается по ссылке ``` http://127.0.0.1:8000/graphql ```
   ```
   python -m uvicorn app.main:app --reload
   ```
3. Запустить фронтенд. Страница сайта доступна по ссылке ``` http://127.0.0.1:8000/graphql ```
   ```
   npm run dev
   ```

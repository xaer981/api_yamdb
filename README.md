# YamDB API 📚🎥🎵
## Описание

Проект YamDB API предоставляет Вам базу данных лучший произведений со всего мира, отсортированных по категориям (например, фильмы, песни, книги и т.д.).
Для того, чтобы просматривать список произведений, узнавать их рейтинг, читать отзывы на них, а также комментарии к отзывам, даже не требуется регистрация!
Зарегистрировавшись, Вы получите ещё больший функционал и сможете оставлять отзывы на произведения с проставлением рейтинга,
а также писать комментарии к отзывам других людей.

## Установка

1. Для начала склонируйте репозиторий к себе на машину:

   ```bash
   git clone https://github.com/xaer981/api_yamdb.git
   ```

   ```bash
   cd api_yamdb
   ```

2. Затем создайте виртуальное окружение и установите зависимости:

   ```bash
   python -m venv venv
   ```

   ```bash
   source venv/Scripts/activate
   ```

   ```bash
   pip install -r requirements.txt
   ```

3. После этого необходимо выполнить миграции:

   ```bash
   cd api_yamdb/
   ```

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
> [!IMPORTANT]
> В случае, если некоторые таблицы не создадутся по тем или иным причинам, после предыдущей команды используйте:
> ```bash
> python manage.py migrate --run-syncdb
> ```

5. Далее можно загрузить в базу данных тестовые данные с помощью следующей команды:

   ```bash
   python manage.py import_data
   ```

6. А теперь запускаем!:

   ```bash
   python manage.py runserver
   ```

## Порядок регистрации:
1. Для начала стоит зарегистрироваться, чтобы получить полный функционал (если полный функционал вам не нужен, то перейдите к ["Примерам запросов"](#Примеры-запросов)):

   ```
   POST http://127.0.0.1:8000/api/v1/auth/signup/
   ```

   В body запроса необходимо указать:
   ```json
       {
           "username": "<username>",
           "email": "<email@email.com>"
       }
   ```

2. Отлично! Теперь нужно получить токен:

   ```
   POST http://127.0.0.1:8000/api/v1/auth/token/
   ```

   В body запроса необходимо указать:
   ```json
       {
           "username": "<username>",
           "confirmation_code": "<confirmation_code, который находится в письме из папки sent_emails>"
       }
   ```

3. Теперь у Вас есть токен! С помощью него начинаем пользоваться сервисом.

4. С помощью данного запроса Вы можете получить информацию о своём аккаунте.
   ```
   GET http://127.0.0.1:8000/api/v1/users/me/
   ```

5. А с помощью такого запроса эту информацию дополнить:
   ```
   PATCH http://127.0.0.1:8000/api/v1/users/me/
   ```
   В body запроса необходимо указать то, поле(я) которое(ые) Вы хотите изменить, например:
   ```json
       {
           "first_name": "<Ваше имя>",
           "last_name": "<Ваша фамилия>"
       }
   ```

## Примеры запросов:

- Получить список всех произведений в БД (на одну страницу выдаётся по 10 произведений):
  ```
  GET http://127.0.0.1:8000/api/v1/titles/
  ```

- Получить список отзывов на данное произведение:
  ```
  GET http://127.0.0.1:8000/api/v1/titles/<title_id>/reviews/
  ```

- Получить список комментариев к данному отзыву:
  ```
  GET http://127.0.0.1:8000/api/v1/titles/<title_id>/reviews/<review_id>/comments/
  ```

- Получить список существующих категорий произведений:
  ```
  GET http://127.0.0.1:8000/api/v1/categories/
  ```

- Получить список существующих жанров произведений:
  ```
  GET http://127.0.0.1:8000/api/v1/genres/
  ```

- Хотите написать отзыв на произведение? Да пожалуйста!:
  ```
  POST http://127.0.0.1:8000/api/v1/titles/<title_id>/reviews/
  ```

  В body запроса необходимо указать следующее:
  ```jsonc
      {
          "text": "<текст вашего отзыва>",
          "score": 5 // <ваша оценка произведения от 1 до 10>
      }
  ```

- Комментарий к отзыву? И так можно:
  ```
  POST http://127.0.0.1:8000/api/v1/titles/<title_id>/reviews/<review_id>/comments/
  ```

  В body запроса необходимо указать следующее:
  ```json
      {
          "text": "<текст вашего комментария>"
      }
  ```

@SGERx
@teehazee
@xaer981

<p align=center>
  <a href="url"><img src="https://github.com/xaer981/xaer981/blob/main/main_cat.gif" align="center" height="40" width="128"></a>
</p>

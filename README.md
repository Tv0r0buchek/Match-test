
# Match Test

A brief description of what this project does and who it's for


##  Libs

pip install django==5.1.1

pip install pymysql

pip install confusable-homoglyphs 

pip install six

pip install Pillow




## secret data
Для работы веб приложения вам необходимо либо изменить файл settings.py под себя, указав в нем ключ django, настройки базы данных, электронную почту и пароль для отправки электронных сообщений и данные админа, либо создать файл secret_data.py в дирректории match_testing и указать следующие переменные

secret_key = 'ваш ключ django'

database_settings = {ваши настройки БД}   #смотрите докумментацию Django

secret_host_user = "something@gmail.com"

secret_host_password = "your_password"

secret_admins = (
  ('Имя пользователя админа на сайте', 'admin_mail@gmail.com'),
)




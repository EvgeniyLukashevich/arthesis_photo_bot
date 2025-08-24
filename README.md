## КОМАНДЫ ТЕРМИНАЛА ДЛЯ РАБОТЫ С БД (CLI)
*Запуск команд указан с учетом терминала, открытого из корневой директории проекта*

### СОЗДАНИЕ БАЗЫ ДАННЫХ

**Команда создания БД:**
```bash
python -m src.cli db init
```

### БЭКАПЫ БАЗЫ ДАННЫХ

**Команда создания бэкапа БД.**  
*По-умолчанию используется сжатие (.zip)*:
```bash
python -m src.cli db backup --name 'backupName'
```
*Без сжатия (.bd)*:
```bash
python -m src.cli db backup --name 'backupName' --no-compress
```
**Команда вывода в терминал списка бэкапов:**  
```bash
python -m src.cli db backups-list
```

## КОМАНДЫ ТЕРМИНАЛА ДЛЯ РАБОТЫ С `РЕГУЛЯРНЫМИ` ПОСТАМИ
*Запуск команд указан с учетом терминала, открытого из корневой директории проекта*

### ДОБАВЛЕНИЕ В БД

**НЕПОСТРЕДСТВЕННО КОМАНДА ДОБАВЛЕНИЯ:**
```bash
python -m src.cli post add
```

**УКАЗАНИЕ ПУТИ ДО ФОТО-ФАЙЛА.**  
ОБЯЗАТЕЛЬНЫЙ ПАРАМЕТР:
```bash
--file ./photos/postPhoto.jpg
```

**УКАЗАНИЕ ЗАГОЛОВКА ПОСТА:**
```bash
--header 'postHeader'
```

**УКАЗАНИЕ НАЗВАНИЯ СНИМКА:**
```bash
--title 'photoTitle'
```

**УКАЗАНИЕ АВТОРА СНИМКА:**
```bash
--author 'photoAuthor'
```

**УКАЗАНИЕ ДАТЫ СНИМКА:**
```bash
--date 'photoDate'
```

**УКАЗАНИЕ ЛОКАЦИИ СНИМКА:**
```bash
--location 'photoLocation'
```

**УКАЗАНИЕ ОПИСАНИЯ СНИМКА:**
```bash
--caption 'photoCaption'
```

**УКАЗАНИЕ ТЭГОВ ПОСТА:**
```bash
--tags 'post_tag1 post_tag2 ...'
```

**УКАЗАНИЕ СТАТУСА ПОСТА *"АКТИВЕН/НЕ АКТИВЕН"*.**  
По-умолчанию присваивается статус *"активен"*:
```bash
--active
```
```bash
--no-active
```

### ДЕАКТИВАЦИЯ И АКТИВАЦИЯ
**КОМАНДА *ДЕАКТИВАЦИИ* РЕГУЛЯРНОГО ПОСТА:**
```bash
python -m src.cli post deactivate postId  
```
**КОМАНДА *АКТИВАЦИИ* РЕГУЛЯРНОГО ПОСТА:**
```bash
python -m src.cli post activate postId  
```

### ОБНОВЛЕНИЕ ПОЛЕЙ
*В случае отсутствия передачи значения в БД передается None/null*  

**КОМАНДА ОБНОВЛЕНИЯ *ПУТИ ДО ФОТО-ФАЙЛА*:**  
```bash
 python -m src.cli post set-photo-path postId --value 'path\photo.jpg'

```

**КОМАНДА ОБНОВЛЕНИЯ *НАЗВАНИЯ* СНИМКА РЕГУЛЯРНОГО ПОСТА:**
```bash
python -m src.cli post set-title postId --value 'newTitle'
```

**КОМАНДА ОБНОВЛЕНИЯ *АВТОРА* СНИМКА РЕГУЛЯРНОГО ПОСТА:**
```bash
python -m src.cli post set-author postId --value 'newAuthor'
```

**КОМАНДА ОБНОВЛЕНИЯ *ДАТЫ* СНИМКА РЕГУЛЯРНОГО ПОСТА:**
```bash
python -m src.cli post set-date postId --value 'newDate'
```

**КОМАНДА ОБНОВЛЕНИЯ *ЛОКАЦИИ* СНИМКА РЕГУЛЯРНОГО ПОСТА:**
```bash
python -m src.cli post set-location postId --value 'newLocation'
```

**КОМАНДА ОБНОВЛЕНИЯ *ОПИСАНИЯ* СНИМКА РЕГУЛЯРНОГО ПОСТА:**
```bash
python -m src.cli post set-caption postId --value 'newCaption'
```

**КОМАНДА ОБНОВЛЕНИЯ *ЗАГОЛОВКА* РЕГУЛЯРНОГО ПОСТА:**
```bash
python -m src.cli post set-header postId --value 'newHeader'
```

**КОМАНДА ОБНОВЛЕНИЯ *ТЭГОВ* РЕГУЛЯРНОГО ПОСТА:**
```bash
python -m src.cli post set-tags postId --value 'tag1 tag2 ...'
```



## КОМАНДЫ ТЕРМИНАЛА ДЛЯ РАБОТЫ С `РЕКЛАМНЫМИ` ПОСТАМИ
*Запуск команд указан с учетом терминала, 
открытого из корневой директории проекта*

### ДОБАВЛЕНИЕ В БД

**НЕПОСРЕДСТВЕННО КОМАНДА ДОБАВЛЕНИЯ:**
```bash
python -m src.cli ad add
```

**УКАЗАНИЕ ПУТИ ДО ФОТО-ФАЙЛА.**   
ОБЯЗАТЕЛЬНЫЙ ПАРАМЕТР (но, есть дефолтный файл):
```bash
--file ./photos/adPhoto.jpg
```

**ДАТЫ/ВРЕМЯ ПУБЛИКАЦИИ РЕКЛАМНОГО ПОСТА.**  
*Передается в виде строки с датами/временем в формате ***ДД.ММ.ГГГГ-ЧЧ:ММ***, разделенными пробелами.*  
*Даты/время необходимо передавать по МСК.*  
ОБЯЗАТЕЛЬНЫЙ ПАРАМЕТР:
```bash
--schedule '18.07.2025-16:25 18.07.2025-17:25 ...'
```

**УКАЗАНИЕ ERID РЕКЛАМНОГО ПОСТА:**
```bash
--erid 'adErid'
```

**УКАЗАНИЕ РЕКЛАМОДАТЕЛЯ:**
```bash
--advertiser_name 'advertiserName'
```

**УКАЗАНИЕ ССЫЛКИ НА ОФИЦИАЛЬНЫЙ РЕСУРС РЕКЛАМОДАТЕЛЯ:**
```bash
--advertiser_link 'advertiserLink'
```

**УКАЗАНИЕ ЗАГОЛОВКА РЕКЛАМНОГО ПОСТА:**
```bash
--title "adTitle"
```

**УКАЗАНИЕ ТЕКСТА РЕКЛАМНОГО ПОСТА:**
```bash
--text 'adText'
```

**УКАЗАНИЕ ССЫЛКИ (НАПРИМЕР, РЕФЕРАЛЬНОЙ) РЕКЛАМНОГО ПОСТА:**
```bash
--link 'adLink'
```

**УКАЗАНИЕ ТЭГОВ РЕКЛАМНОГО ПОСТА:**
```bash
--tags 'ad_tag1 ad_tag2 ...'
```

**УКАЗАНИЕ СТАТУСА РЕКЛАМНОГО ПОСТА *"АКТИВЕН/НЕ АКТИВЕН"*.**  
По-умолчанию присваивается статус *"активен"*:
```bash
--active
```
```bash
--no-active
```

### ДЕАКТИВАЦИЯ И АКТИВАЦИЯ

**КОМАНДА ДЕАКТИВАЦИИ РЕКЛАМНОГО ПОСТА:**
```bash
python -m src.cli ad deactivate adId  
```
**КОМАНДА АКТИВАЦИИ РЕКЛАМНОГО ПОСТА:**
```bash
python -m src.cli ad activate adId  
```

### ОБНОВЛЕНИЕ ПОЛЕЙ

**КОМАНДА ОБНОВЛЕНИЯ *ПУТИ ДО ФОТО-ФАЙЛА* РЕКЛАМНОГО ПОСТА:**
```bash
python -m src.cli ad set-photo-path adId --value 'path/ad_photo.jpg'
```

**КОМАНДА ОБНОВЛЕНИЯ *ERID* РЕКЛАМНОГО ПОСТА:**
```bash
python -m src.cli ad set-erid adId --value 'adErid'
```

**КОМАНДА ОБНОВЛЕНИЯ *ИМЕНИ РЕКЛАМОДАТЕЛЯ* РЕКЛАМНОГО ПОСТА:**
```bash
python -m src.cli ad set-advertiser-name adId --value 'advertiserName'
```

**КОМАНДА ОБНОВЛЕНИЯ *ССЫЛКИ НА ОФ. РЕСУРС РЕКЛАМОДАТЕЛЯ* РЕКЛАМНОГО ПОСТА:**
```bash
python -m src.cli ad set-advertiser-link adId --value 'advertiserLink'
```

**КОМАНДА ОБНОВЛЕНИЯ *ЗАГОЛОВКА* РЕКЛАМНОГО ПОСТА:**
```bash
python -m src.cli ad set-title adId --value 'adTitle'
```

**КОМАНДА ОБНОВЛЕНИЯ *ТЕКСТА* РЕКЛАМНОГО ПОСТА:**
```bash
python -m src.cli ad set-text adId --value 'adText'
```

**КОМАНДА ОБНОВЛЕНИЯ *ССЫЛКИ* РЕКЛАМНОГО ПОСТА:**
```bash
python -m src.cli ad set-link adId --value 'adLink'
```

**КОМАНДА ОБНОВЛЕНИЯ *ТЭГОВ* РЕКЛАМНОГО ПОСТА:**
```bash
python -m src.cli ad set-tags adId --value 'adTag1 adTag2 ...'
```

**КОМАНДА ОБНОВЛЕНИЯ *РАСПИСАНИЯ ДАТ ПУБЛИКАЦИИ* РЕКЛАМНОГО ПОСТА.**  
'dd.mm.yyyy-hh:mm dd.mm.yyyy-hh:mm ...' (MSK):
```bash
python -m src.cli ad set-dates adId --value 'dd.mm.yyyy-hh:mm dd.mm.yyyy-hh:mm ...'
```

**КОМАНДА ДОБАВЛЕНИЯ НОВЫХ *ДАТ ПУБЛИКАЦИИ* К СУЩЕСТВУЮЩЕМУ РАСПИСАНИЮ РЕКЛАМНОГО ПОСТА.**  
'dd.mm.yyyy-hh:mm dd.mm.yyyy-hh:mm ...' (MSK):
```bash
python -m src.cli ad add-dates adId --value 'dd.mm.yyyy-hh:mm dd.mm.yyyy-hh:mm ...'
```


## КОМАНДЫ ТЕРМИНАЛА ДЛЯ РАБОТЫ С `ВНЕОЧЕРЕДНЫМИ` ПОСТАМИ
*Запуск команд указан с учетом терминала, 
открытого из корневой директории проекта*

### ДОБАВЛЕНИЕ В БД

**НЕПОСРЕДСТВЕННО КОМАНДА ДОБАЛЕНИЯ:**
```bash
python -m src.cli instant add
```

**УКАЗАНИЕ ПУТИ ДО ФОТО-ФАЙЛА.**  
ОБЯЗАТЕЛЬНЫЙ ПАРАМЕТР (но, есть дефолтный файл):
```bash
--file ./photos/instantPhoto.jpg
```

**ДАТЫ/ВРЕМЯ ПУБЛИКАЦИИ ВНЕОЧЕРЕДНОГО ПОСТА.**  
*Передается в виде строки с датами/временем в формате ***дд.мм.гггг-чч:мм***, разделенными пробелами.*  
*Даты/время необходимо передавать по МСК.*  
ОБЯЗАТЕЛЬНЫЙ ПАРАМЕТР:
```bash
--schedule '18.07.2025-16:25 18.07.2025-17:25 ...'
```

**УКАЗАНИЕ ТЕКСТА ВНЕОЧЕРЕДНОГО ПОСТА:**
```bash
--text 'instantText'
```

**УКАЗАНИЕ ТЭГОВ ВНЕОЧЕРЕДНОГО ПОСТА:**
```bash
--tags 'instantTag1 instantTag2 ...'
```

**УКАЗАНИЕ СТАТУСА ПОСТА *"АКТИВЕН/НЕ АКТИВЕН"*.**  
По-умолчанию присваивается статус *"активен"*:
```bash
--active
```
```bash
--no-active
```

### ДЕАКТИВАЦИЯ И АКТИВАЦИЯ

**КОМАНДА ДЕАКТИВАЦИИ ВНЕОЧЕРЕДНОГО ПОСТА:**
```bash
python -m src.cli instant deactivate instantId  
```
**КОМАНДА АКТИВАЦИИ ВНЕОЧЕРЕДНОГО ПОСТА:**
```bash
python -m src.cli instant activate instantId  
```


### ОБНОВЛЕНИЕ ПОЛЕЙ

**КОМАНДА ОБНОВЛЕНИЯ *ПУТИ ДО ФОТО-ФАЙЛА* ВНЕОЧЕРЕДНОГО ПОСТА:**
```bash
python -m src.cli instant set-photo-path instantId --value 'path/instant_photo.jpg'
```

**КОМАНДА ОБНОВЛЕНИЯ *ТЕКСТА* ВНЕОЧЕРЕДНОГО ПОСТА:**
```bash
python -m src.cli instant set-text instantId --value 'instantText'
```

**КОМАНДА ОБНОВЛЕНИЯ *ТЭГОВ* ВНЕОЧЕРЕДНОГО ПОСТА:**
```bash
python -m src.cli instant set-tags instantId --value 'instantTag1 instantTag2 ...'
```

**КОМАНДА ОБНОВЛЕНИЯ *РАСПИСАНИЯ ДАТ ПУБЛИКАЦИИ* ВНЕОЧЕРЕДНОГО ПОСТА.**  
'dd.mm.yyyy-hh:mm dd.mm.yyyy-hh:mm ...' (MSK):
```bash
python -m src.cli instant set-dates instantId --value 'dd.mm.yyyy-hh:mm dd.mm.yyyy-hh:mm ...'
```

**КОМАНДА ДОБАВЛЕНИЯ НОВЫХ *ДАТ ПУБЛИКАЦИИ* К СУЩЕСТВУЮЩЕМУ РАСПИСАНИЮ ВНЕОЧЕРЕДНОГО ПОСТА.**  
'dd.mm.yyyy-hh:mm dd.mm.yyyy-hh:mm ...' (MSK):
```bash
python -m src.cli instant add-dates instantId --value 'dd.mm.yyyy-hh:mm dd.mm.yyyy-hh:mm ...'
```


## СПЕЦСИМВОЛЫ И РАЗМЕТКА СООБЩЕНИЙ:
- `****` - переход на следующую строку  
- `"` - кавычки необходимо экранировать (`\"`)  
- `<b>Жирный текст</b>`  
- `<strong>Жирный текст</strong>`  
- `<i>Курсивный текст</i>`  
- `<em>Курсивный текст</em>`  
- `<u>Подчёркнутый текст</u>`
- `<s>Зачёркнутый текст</s>`
- `<strike>Зачёркнутый текст</strike>`
- `<del>Зачёркнутый текст</del>`
- `<tg-spoiler>Скратый текст</tg-spoiler>`
- `<code>Строка кода</code>`
- `-pre> Для блоков кода -/pre>` (минус заменить на '<')
- `<a href=\"https://www.link.ru\">Подпись</a>` - ссылка с подписью  
- `<a href=\"https://t.me/username\">Какой-то пользователь</a>` - ссылка на пользователя ТГ (по username)  
- `<a href=\"tg://user?id=123456789\">Какой-то пользователь</a>` - ссылка на пользователя ТГ (по user_id)  
- `<a href=\"https://t.me/group_username\">Какая-то группа</a>` - ссылка на группу/канал (по username группы/канала)
- `<a href=\"https://t.me/c/123456789\">Какая-то группа</a>` - ссылка на группу/канал (по id группы/канала)

START_FOR_NEWBIES = '''<b>Приветствую тебя, {name}!</b>\n
🔰 Начни с небольшой подсказки - нажми <b>"Как со мной общаться?"</b>
🔰 Создавай свой список желаний с помощью кнопки <b>"Создать мой список желаний"</b>
🔰 Ищи список желаний друга с помощью кнопки <b>"Выбрать подарок другу"</b>
'''

START_PHRASES = [
    "🪄 Крибле-крабле-бумс! Чего изволите в подарок? Или вы друзьям подарок выбираете? 🧞",
    "🪄 ВЖУХ! И скоро Новый Год. Чего загадаете? 🧞",
    "🪄 Абракадабра и прочие заклинания не помогут. Просто нажми кнопку. 🧞",
    "🪄 Империус! Ой, не сработало. Ну тогда опять вы выбираете. 🧞",
    "🪄 Нажми кнопку и может случится какая-то магия... Ну или хоть пообщаемся. 🧞",
    "🪄 \"Сим-сим откройся\", - сказал я! А из лампы меня так и не выпустили. Чем могу быть полезен? 🧞",
    "🪄 Поделишься своими желаниями? Я точно никому не расскажу! Честное Алладинское! 🧞",
    "🪄 Сколько-сколько желаний тебе нужно?? У меня с вами скоро борода полысеет... 🧞",
    "🪄 Сколько лампу не три, а все равно я не выйду. Теперь вот тут работаю, вся магия через Телеграм. 🧞",
    "🪄 Принимаю заявки на Новый Год. Но с доставочкой могут быть задержки - ковры зимой летают плохо, сами понимаете. 🧞"
]

INSTRUCTION = '''
<b>Как создать свой список желаний и поделиться им с друзьями? ✏️</b>
🔰 Выбери "Создать мой список желаний" и расскажи мне немного о себе ИЛИ выбери "Открыть мой список подарков", если мы уже познакомились.
🔰 Теперь ты можешь добавить желания в свой список. Пользуйся кнопками "Добавить желание" или "Добавить желания списком". 
<b>Расскажи подробно, чего желаешь, чтобы твои друзья точно тебя поняли.</b>
🔰 Твои желания появятся в списке. Под каждым будут кнопки "Удалить" и "Добавить ссылку" (на товар или изображение).
🔰 Под списком желаний будет указан твой уникальный 6-ти значный код, которым нужно поделиться с друзьями, чтобы они увидели твой список желаний.
<b>Если при регистрации ты сообщил мне свой номер телефона, то друзья могут найти твой список по нему.</b>

<b>Как найти список желаний друга? 🔎</b>
🔰 Выбери "Выбрать подарок другу" и введи его уникальный 6-ти значный код (или его номер телефона).
<b>Не знаешь код? Тогда скорее спроси его у друга!</b>
🔰 Тебе откроется информация о друге и его список свободных желаний.
🔰 Выбери понравившийся подарок с помощью кнопки "Выбрать подарок".
🔰 Ты увидишь весь список подарков, которые ты выбрал у своих друзей. Рядом с каждым подарком будет кнопка "Отменить выбор".
🔰 Теперь не забудь купить выбранный подарок к празднику друга, ведь он будет очень его ждать!
<b>Для каждого своего друга ты можешь выбрать не больше 2 подарков. Остальные оставь другим!</b>

<i>В случае ошибок и по всем вопросам/предложениям ты можешь написать моему создателю:</i>
https://t.me/dena_den
'''

WISHES_TOP = """
⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇⠀
"""

MY_WISHES_BOTTOM = """
⬆️⬆️⬆️⬆️⬆️⬆️⬆️⬆️⬆️⬆️⬆️⬆️⬆️
<b>Это твой список желаний.</b> Ты можешь добавлять желания по одному или сразу списком.\n
Поделись кодом с друзьями 📲, чтобы они могли найти твой список желаний: <b>{user_id}</b>
"""

MY_WISHES_EMPTY_BOTTOM = """
⭕️
<b>Твой список желаний абсолютно пуст.</b> Их можно добавить с помощью кнопок ниже.\n
Поделись кодом с друзьями 📲, чтобы они могли найти твой список желаний: <b>{user_id}</b>
"""

FIND_BY_PHONE = "Или они могут найти тебя по твоему <b>номеру телефона</b> вместо кода."

RESERVED_WISHES_BOTTOM = """
⬆️⬆️⬆️⬆️⬆️⬆️⬆️⬆️⬆️⬆️⬆️⬆️⬆️
<b>Это список выбранных тобой подарков.</b> Уже купил выбранные подарки? Поторопись, если еще нет ⏰
"""

RESERVED_WISHES_EMPTY_BOTTOM = """
⭕️
<b>Это список выбранных тобой подарков</b> Ты еще не выбрал подарков своим друзьям. Нажми <b>Выбрать подарок другу</b> и найди своих друзей 🤝
"""

FRIEND_WISHES_BOTTOM = """
⬆️⬆️⬆️⬆️⬆️⬆️⬆️⬆️⬆️⬆️⬆️⬆️⬆️
Это список подарков твоего друга:
<b>{name}, {birthdate}</b>
Выбирай тот, что нравится и готовься к празднику 🥳
"""

FRIEND_WISHES_EMPTY_BOTTOM = """
⭕️
Список подарков твоего друга пока что пуст.
<b>{name}, {birthdate}</b>
Напомни ему, чтобы он добавил свои желания. Или просто загляни попозже 😉
"""

FRIENDS_WISHES_BLOCKED = """
⬆️⬆️⬆️⬆️⬆️⬆️⬆️⬆️⬆️⬆️⬆️⬆️⬆️
Это список подарков твоего друга: 
<b>{name}, {birthdate}</b>
Ты уже выбрал для него 2 подарка. Оставь другим 😁
"""

MY_WISH = """
🎁 <b>{wish_name}</b>
{product_link}{is_reserved}
"""

RESERVED_WISH = """
🎁 <b>{wish_name}</b>
{product_link}Именинник: {name}, {birthdate}
"""

FRIEND_WISH = """
🎁 <b>{wish_name}</b>
{product_link}
"""


# description
'''
Я бот 🤖, исполняющий желания! 🔮 (ну почти)
Скоро праздник? Я помогу подсказать твоим друзьям, что ты действительно хочешь в подарок!

🔰 С моей помощью ты можешь составить список своих желаний 📝, а потом поделиться им с друзьями
🔰 Они смогут выбрать понравившиеся подарки и подарить тебе именно то, что ты хочешь 🔥
🔰 Каждый подарок может быть забронирован только одним другом, так что никто точно не подарит одинаковые 👍
'''
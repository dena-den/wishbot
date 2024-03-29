START_FOR_NEWBIES = '''<b>Приветствую тебя, {name}!</b>

🔰 Начни с небольшой подсказки - нажми <b>"Как пользоваться ботом?"</b>
🔰 Создавай свой список желаний с помощью кнопки <b>"Мой вишлист"</b>
🔰 Ищи список желаний друга с помощью кнопки <b>"Вишлисты друзей"</b>
'''

START_PHRASES = [
    "🪄 Крибле-крабле-бумс!\nЧего изволите в подарок? Или вы друзьям подарок выбираете? 🧞",
    "🪄 ВЖУХ! И скоро 14 февраля.\nЧего пожелаете? 🧞",
    "🪄 Абракадабра и прочие заклинания не помогут - просто нажми кнопку. 🧞",
    "🪄 Империус!\nОй, не сработало.\nНу тогда опять вы выбираете. 🧞",
    "🪄 Нажми кнопку и может случится какая-то магия! Ну или хоть пообщаемся. 🧞",
    "🪄 \"Сим-сим откройся\", - сказал я! А из лампы меня так и не выпустили.\nЧем могу быть полезен? 🧞",
    "🪄 Поделишься своими желаниями? Я точно никому не расскажу! Честное Алладинское! 🧞",
    "🪄 Сколько-сколько желаний тебе нужно??\nУ меня с вами скоро борода полысеет... 🧞",
    "🪄 Сколько лампу не три, а все равно я не выйду. Теперь вот тут работаю, вся магия через Телеграм. 🧞",
    "🪄 Принимаю заявки на ближайшие праздники. Но с доставочкой могут быть задержки - ковры зимой летают плохо, сами понимаете. 🧞"
]

INSTRUCTION = '''
<b>Как создать свой список желаний и поделиться им с друзьями? ✏️</b>
🔰 Просто нажми "Мой вишлист" и добавляй свои желания с помощью кнопок "Добавить желание".
<b>Расскажи подробно, чего желаешь, чтобы твои друзья точно тебя поняли.</b>
🔰 Твои желания появятся в списке. Под каждым будут кнопки "Удалить" и "Добавить описание" (можно добавить ссылку на товар или на его изображение 😉).
🔰 Теперь в главном меню выбери "Поделиться вишлистом" и перешли полученное сообщение своим друзьям. 
Готово 👍

<b>Как найти список желаний друга? 🔎</b>
🔰 Выбери "Вишлисты друзей" и введи его уникальный шестизначный код.
<b>Не знаешь код? Тогда скорее спроси его!</b>
🔰 Тебе откроется список свободных желаний твоего друга.
🔰 Обязательно выбери понравившийся подарок с помощью кнопки "Выбрать этот подарок".
<b>Теперь этот подарок зарезервирован только тобой 🔒 и никто другой его не купит.</b>
Готово 👍

❗️ Для каждого своего друга ты можешь выбрать не более 2 подарков. Остальные оставь другим!
❗️ Зарезервированные подарки ты всегда можешь посмотреть в разделе "Выбранные мною подарки". Там же можно отменить выбранный подарок, если передумал.

<i>В случае ошибок и по всем вопросам/предложениям ты можешь написать моему создателю:</i>
https://t.me/dena_den
'''

FRIENDS_INVITATION_BY_CODE = '''
Привет 👋

https://t.me/ai_wish_bot - этот бот может рассказать тебе, что я хочу в подарок.
Начни диалог с ним, нажми <b>"Вишлисты друзей"</b> и введи мой уникальный код <b>{code}</b>
'''

MY_WISHES_BOTTOM = """
<b>Это твой список желаний.</b> 
Добавляй желания и делись кодом <b>{user_id}</b> с друзьями 📲"""

MY_WISHES_EMPTY_BOTTOM = """
<b>Твой список желаний абсолютно пуст.</b> 
Их можно добавить с помощью кнопок ниже."""

RESERVED_WISHES_BOTTOM = """
<b>Это список выбранных тобой подарков.</b> 
Уже купил их? Поторопись, если еще нет ⏰
"""

RESERVED_WISHES_EMPTY_BOTTOM = """
<b>Это список выбранных тобой подарков</b> 
Ты еще не выбрал подарков своим друзьям. 
Вернись в главное меню, нажми <b>"Вишлисты друзей"</b> и найди своих друзей 🤝
"""

FRIEND_WISHES_BOTTOM = """
Это список подарков твоего друга: <b>{name} {last_name} {tg_nickname}</b>
Выбирай тот, что нравится, и готовься к празднику 🥳
"""

FRIEND_WISHES_EMPTY_BOTTOM = """
Список подарков твоего друга пока что пуст.
<b>{name} {last_name} {tg_nickname}</b>
Напомни ему, чтобы он добавил свои желания, или просто загляни попозже 😉
"""

FRIENDS_WISHES_BLOCKED = """
Это список подарков твоего друга: <b>{name} {last_name} {tg_nickname}</b>
Ты уже выбрал для него 2 подарка. Оставь другим 😁
"""

MY_WISH = """
🎁 <b>{wish_name}</b>
{product_link}{is_reserved}
"""

RESERVED_WISH = """
🎁 <b>{wish_name}</b>
{product_link}Именинник: {name} {last_name} {tg_nickname}
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
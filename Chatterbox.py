import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import numpy as np
import random as aboba


# отправка сообщений
def write_msg(peer_id, message, random_id):
    VK.method('messages.send', {'peer_id': peer_id, 'message': message, 'random_id': random_id})


# отправка картинок
def send_photo(user_id, random_id):
    upload = vk_api.VkUpload(VK)
    photo = upload.photo_messages(r'F:\a.png')
    # photo = upload.photo_messages('https://news.ykt.ru/upload/image/2021/04/119011/main_thumb.jpg?1618626690')
    owner_id = photo[0]['owner_id']
    photo_id = photo[0]['id']
    access_key = photo[0]['access_key']
    attachment = f'photo{owner_id}_{photo_id}_{access_key}'
    VK.method('messages.send', {'user_id': user_id, 'random_id': random_id, 'attachment': attachment})


def generate_photo():
    pass


# генерация текста
def generate_answer(request):
    # отправляем в переменную всё содержимое текстового файла
    text = open('text.txt', encoding='utf8').read()

    # разбиваем текст на отдельные слова (знаки препинания останутся рядом со своими словами)
    corpus = text.split()

    # делаем новую функцию-генератор, которая определит пары слов
    def make_pairs(corpus):
        # перебираем все слова в корпусе, кроме последнего
        for i in range(len(corpus) - 1):
            # генерируем новую пару и возвращаем её как результат работы функции
            yield (corpus[i], corpus[i + 1])

    # вызываем генератор и получаем все пары слов
    pairs = make_pairs(corpus)

    # словарь, на старте пока пустой
    word_dict = {}

    # перебираем все слова попарно из нашего списка пар
    for word_1, word_2 in pairs:
        # если первое слово уже есть в словаре
        if word_1 in word_dict.keys():
            # то добавляем второе слово как возможное продолжение первого
            word_dict[word_1].append(word_2)
        # если же первого слова у нас в словаре не было
        else:
            # создаём новую запись в словаре и указываем второе слово как продолжение первого
            word_dict[word_1] = [word_2]

    list_request = request.split()
    flag = True
    for word in list_request:
        if word in word_dict:
            first_word = word
            print("request")
            flag = False
            break
    if flag:
        # случайно выбираем первое слово для старта
        first_word = np.random.choice(corpus)
        # если в нашем первом слове нет больших букв
        while first_word.islower():
            # то выбираем новое слово случайным образом
            # и так до тех пор, пока не найдём слово с большой буквой
            first_word = np.random.choice(corpus)
    # делаем наше первое слово первым звеном
    chain = [first_word]

    # сколько слов будет в готовом тексте
    n_words = aboba.randint(1, 10)

    # делаем цикл с нашим количеством слов
    for i in range(n_words):
        # на каждом шаге добавляем следующее слово из словаря, выбирая его случайным образом из доступных вариантов
        chain.append(np.random.choice(word_dict[chain[-1]]))

    # выводим результат
    answer = str(' '.join(chain))
    return answer


# API-key
token = "64ae3b7e3b93d059ac9a1b36f68aa4b10a9ca5b0acc41971d05fecfe1df4378f0dae8a11de124d42bc853"

# Авторизуемся как сообщество
VK = vk_api.VkApi(token=token)

# Работа с сообщениями
longpoll = VkLongPoll(VK)

file_path = r'F:\_G96sgbJuQo.jpg'

# Основной цикл
for event in longpoll.listen():
    random_id = vk_api.utils.get_random_id()
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        request = event.text.lower()
        if request == "стоп":
            write_msg(event.peer_id, request, random_id)
            generate_photo()
            break
        if request == "да":
            write_msg(event.peer_id, "пизда", random_id)
        if request == 'f':
            pass
        else:
            write_msg(event.peer_id, generate_answer(request), random_id)

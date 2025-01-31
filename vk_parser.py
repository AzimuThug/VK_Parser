import vk
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType


# отправка сообщений
def write_msg(peer_id, message, random_id):
    VK.method('messages.send', {'peer_id': peer_id, 'message': message, 'random_id': random_id})


# парсер сообществ
def parser(request):
    answer = ''

    vk_api = vk.API(vk.Session(access_token=TOKEN))

    DOMAIN = request.split()[0][15:]
    try:
        MODE = request.split()[1]
    except IndexError:
        MODE = 'likes'
    try:
        COUNT = int(request.split()[2])
    except IndexError:
        COUNT = 3
    data = []
    i = 0
    MAX = 50
    try:
        while (vk_api.wall.get(domain=DOMAIN, count=100, filter="owner", v=5.131, offset=100 * i)["items"]) and (
                i <= MAX):
            data += vk_api.wall.get(domain=DOMAIN, count=100, filter="owner", v=5.131, offset=100 * i)["items"]
            i += 1
        answer = create_answer(data, MODE, COUNT, answer)
        print(i)
    except Exception:
        answer = 'oops, smth wrong'
    return answer


# сборка сообщения для парсера
def create_answer(data, mode, count, answer):
    dict_of_posts = {}
    for item in data:
        key = item[mode]['count']
        value = "https://vk.com/wall" + str(item['from_id']) + "_" + str(item['id'])
        dict_of_posts[key] = value
    list_keys = list(dict_of_posts.keys())
    list_keys.sort(reverse=True)
    iter = 0
    for i in list_keys:
        answer += (str(i) + ' : ' + dict_of_posts[i] + '\n')
        iter += 1
        if iter == count:
            break
    return answer


# API-key
token = "64ae3b7e3b93d059ac9a1b36f68aa4b10a9ca5b0acc41971d05fecfe1df4378f0dae8a11de124d42bc853"

# Service token
TOKEN = "78f6194c78f6194c78f6194c08788dae43778f678f6194c1ac2cc82b02923ed65a648c2"

# Авторизуемся как сообщество
VK = vk_api.VkApi(token=token)

# Работа с сообщениями
longpoll = VkLongPoll(VK)

info = 'Ку, я бот слепленный из говна и палок для парсинга групп в вк.\n ' \
       'Запрос должен выглядеть так:\n' \
       'https://vk.com/memfactorys likes 5\n' \
       'где первый параметр - ссылка, второй - режим по каторому парсим(likes, comments, reposts), четвертый -' \
       'число постов, которые нужно вернуть\n' \
       'Если вставить только ссылку, то я верну 3 самых лайкнутых поста'

# Основной цикл
for event in longpoll.listen():
    random_id = vk_api.utils.get_random_id()
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        request = event.text.lower()
        if request == "стоп":
            write_msg(event.peer_id, request, random_id)
            break
        if "https://vk.com/" in request:
            write_msg(event.peer_id, parser(request), random_id)
        if request == "info":
            write_msg(event.peer_id, info, random_id)
        else:
            write_msg(event.peer_id, 'моя твоя не понимать', random_id)

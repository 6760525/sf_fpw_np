from django.contrib.auth.models import User
from news.models import *

user1 = User.objects.create_user('user_a')
user2 = User.objects.create_user('user_b')

auth1 = Author.objects.create(user=user1)
auth2 = Author.objects.create(user=user2)

cat1 = Category.objects.create(category='Спорт')
cat2 = Category.objects.create(category='Образование')
cat3 = Category.objects.create(category='Шапито')
cat4 = Category.objects.create(category='Наука')

post1 = Post.objects.create(author=auth1, type='AR', title='В Google Maps на месте острова в Тихом океане нашли черную дыру. Так мог бы выглядеть вход в метавселенную Марка Цукерберга', text='Пользователь Reddit под ником kokoblocks нашел на Google Maps остров треугольной формы, напоминающий черную дыру. «Какого *** [черта]. Это не выглядит как остров», — написал он в подфоруме r/GoogleMaps в посте со скриншотом карты. Внимание на его запись обратили многие зарубежные СМИ.')
post2 = Post.objects.create(author=auth2, type='AR', title='Оксфордский словарь выбрал слово года - vax («вакцина», «вакцинация», «вакцинировать»). Его стали употреблять в 72 раза чаще Бонус: в британский доклад попали слова «ширяться» и «шмурдяк»', text='Составители Оксфордского словаря английского языка выбрали слово 2021 года - vax («вакцина», «вакцинация», «вакцинировать»). Об этом сообщается в докладе «Слово года 2021. Vax: отчет о языке вакцин», который подготовили в рамках программы исследований Oxford Languages.\nVax - сравнительно редкое слово, но к сентябрю 2021-го его стали употреблять в 72 раза чаще по сравнению с сентябрем 2020-го, говорится в докладе. «От него образовалось множество производных, которые, как мы сейчас видим, используются в разнообразных неформальных контекстах. Нет слова, лучше отражающего атмосферу уходящего года, чем vax», - отмечают авторы доклада.')
post3 = Post.objects.create(author=auth1, type='NE', title='Интернет-регулятор Узбекистана ограничил доступ к YouTube, Instagram и Telegram. Президент назвал решение «непродуманным» - и его сразу же отменили', text='Интернет-регулятор Узбекистана Узкомназорат ограничил доступ к целому ряду соцсетей, в числе которых Telegram, Facebook, «Одноклассники», YouTube, Instagram и LinkedIn. Об этом сообщает «Газета.уз».\nКак уточняет издание, доступ к соцсетям был ограничен из-за того, что они нарушили требование властей о хранении данных узбекских пользователей на территории Узбекистана. Соответствующий закон, обязывающий все зарубежные соцсети делать это, был принят весной 2021 года.')

PostCategory.objects.create(post=post1, category=cat1)
PostCategory.objects.create(post=post1, category=cat3)
PostCategory.objects.create(post=post2, category=cat3)
PostCategory.objects.create(post=post2, category=cat4)
PostCategory.objects.create(post=post3, category=cat3)

comm1 = Comment.objects.create(post=post1, user=user1, text='Комметарий 1 к посту 1')
comm2 = Comment.objects.create(post=post2, user=user1, text='Комметарий 1 к посту 2')
comm3 = Comment.objects.create(post=post3, user=user1, text='Комметарий 1 к посту 3')
comm4 = Comment.objects.create(post=post1, user=user2, text='Комметарий 2 к посту 1')
comm5 = Comment.objects.create(post=post2, user=user2, text='Комметарий 2 к посту 2')
comm6 = Comment.objects.create(post=post3, user=user2, text='Комметарий 2 к посту 3')
user3 = User.objects.create_user('user_c')
comm7 = Comment.objects.create(post=post1, user=user3, text='Комметарий 3 к посту 1')
comm8 = Comment.objects.create(post=post2, user=user3, text='Комметарий 3 к посту 2')
comm9 = Comment.objects.create(post=post3, user=user3, text='Комметарий 3 к посту 3')

post1.like()
post2.like()
post3.dislike()
post1.like()
post1.dislike()
post2.like()
post3.dislike()
post3.dislike()

comm1.like()
comm2.like()
comm3.like()
comm4.like()
comm5.like()
comm6.like()
comm7.like()
comm8.like()
comm9.like()
comm1.like()
comm3.like()
comm6.like()
comm9.like()

auth1.update_rating()
auth2.update_rating()

top_author = Author.objects.order_by('-rating')[0]
print(f'Лучший автор: {top_author.user}, его рейтинг: {top_author.rating}')

top_post = Post.objects.filter(type=Post.article).order_by('-rating')[0]
print('Лучий пост:')
print(f'Дата: {top_post.creation_time}')
print(f'Автор: {top_post.author.user}')
print(f'Рейтинг: {top_post.rating}')
print(f'Превью: {top_post.preview()}')
print('Комментарии:')
for comment in Comment.objects.filter(post=top_post):
    print('\t', 'Дата:', comment.creation_time)
    print('\t', 'Пользователь:', comment.user)
    print('\t', 'Рейтинг:', comment.rating)
    print('\t', 'Текст:', comment.text)
    print('\t', '-'*50)

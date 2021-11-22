from django import template
 
register = template.Library()
 
replacements = {'вакцин': '*Роскомнадзор*',
                'хер': 'х*р',
                'Google': '*Yandex*',
                'ширяться': '*Роскомнадзор*',
                'Facebook': '*Meta*'}
 
@register.filter(name='Censor')
def Censor(text):
    if isinstance(text, str):
        res = str(text)
        for word in replacements.keys():
            res = res.replace(word, replacements[word])
        return res
    else:
        raise TypeError(f'Invalid type {type(text)}')

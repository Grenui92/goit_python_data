class Meta(type):

    def __new__(*args, **kwargs):
        # якщо прочитаєте, дайте відповідь будьласка в комментах до роботи, чи правильно я розумію, що ось ця __new__ використовується\викликається коли
        # створюється сам клас. Тобто вона виконується коли ще ні який код не виконується, коли інтерпрітатор просто продивляється з верху до низу що я тут
        # понаписав. Коли формується сам каркас класу.
        args[3]["class_number"] = Meta.children_number
        Meta.children_number += 1
        return type.__new__(*args, **kwargs)

    def __call__(cls, *args, **kwargs):
        # а ось ця __call__ використовується\викликається коли ЛИШЕ створюється вже ОБ'ЄКТ класу!
        result_class = object.__new__(cls)
        result_class.__init__(*args, **kwargs)
        return result_class




Meta.children_number = 0

class Cls1(metaclass=Meta):

    def __init__(self, data):
        self.data = data


class Cls2(metaclass=Meta):

    def __init__(self, data):
        self.data = data

class Cls3(metaclass=Meta):

    def __init__(self, data):
        self.data = data


assert (Cls1.class_number, Cls2.class_number, Cls3.class_number) == (0, 1, 2)
a, b, c = Cls1('3'), Cls2('5'), Cls3('7')
assert (a.class_number, b.class_number, c.class_number) == (0, 1, 2)

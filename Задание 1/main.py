import functools
import time
from datetime import datetime
import os

def logger(old_function):
    @functools.wraps(old_function)
    def new_function(*args, **kwargs):
        with open('main.log', 'a') as file:
            time = datetime.now()
            current_time = time.time().strftime('%H:%M')
            current_date = time.today().strftime('%d.%m.%y')
            list_args = [str(i) for i in args]
            list_kwargs = [f'{j}={n!r}' for j, n in kwargs.items()]
            result = ', '.join(list_args + list_kwargs)
            func_result = old_function(*args, **kwargs)
            func_name_str = f'Вызываемая функция - {old_function.__name__}({result})'
            func_args_str = f'Аргументы функции - {result}'
            func_date = f'Функция {old_function.__name__!r} вызвана в {current_time}, {current_date}'
            func_return = f'Функция возвращает - {func_result}'
            info_write = [func_name_str, func_args_str, func_date, func_return]
            for i in info_write:
                file.write(i)
                file.write('\n')
            file.write('\n')
        return func_result
    return new_function


def test_1():
    path = 'main.log'
    if os.path.exists(path):
        os.remove(path)

    @logger
    def hello_world():
        return 'Hello World'

    @logger
    def summator(a, b=0):
        return a + b

    @logger
    def div(a, b):
        return a / b

    assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
    result = summator(2, 2)
    assert isinstance(result, int), 'Должно вернуться целое число'
    assert result == 4, '2 + 2 = 4'
    result = div(6, 2)
    assert result == 3, '6 / 2 = 3'

    assert os.path.exists(path), 'файл main.log должен существовать'

    summator(4.3, b=2.2)
    summator(a=0, b=0)

    with open(path) as log_file:
        log_file_content = log_file.read()

    assert 'summator' in log_file_content, 'должно записаться имя функции'
    for item in (4.3, 2.2, 6.5):
        assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_1()
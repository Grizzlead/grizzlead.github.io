#продолжите решение здесь
test_lst = [
    ['1234', '#1234', '1 тест'],
    [['1', '3', 'a'], '#13a', '2 тест'],
    [['qwsdf4'], '#qwsdf4', '3 тест'],
    [5, None, '4 тест'],
    [('q', 'w', 'd'), None, '5 тест'],
    [[1, True, 'f'], '#1Truef', '6 тест']
]

def func(s):
    if type(s) == str:
        return '#' + s
    elif type(s) == list:
        return '#' + ''.join(map(str, s))
    
def test_func(func, lst):
    for item in lst:
        assert func(item[0]) == item[1]

test_func(func, test_lst)        
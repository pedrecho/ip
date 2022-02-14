import copy
import math

error = 'Неправильный ввод'


def ip_in(x):
    ip_loc = x.strip(' ').split('.')
    if len(ip_loc) != 4:
        return error
    b = True
    for i in ip_loc:
        if len(i) > 3:
            b = False
        else:
            try:
                l = int(i)
                if l < 0 or l > 255:
                    b = False
            except:
                b = False
    if b:
        return ip_loc
    b = True
    for i in ip_loc:
        if len(i) == 8:
            for l in i:
                if l != '0' and l != '1':
                    b = False
        else:
            b = False
    if b:
        return to_dec(ip_loc)
    return error


def ints_to_strings(a):
    return list(map(lambda x: str(x), a))


def ip_out(ip):
    return '.'.join(ints_to_strings(ip))


def to_dec(ip):
    ip_loc = copy.copy(ip)
    for i in range(len(ip_loc)):
        ip_loc[i] = int(ip_loc[i], 2)
    return ip_loc


def to_bin(ip):
    ip_loc = copy.copy(ip)
    for i in range(len(ip_loc)):
        ip_loc[i] = "{0:b}".format(int(ip_loc[i]))
        ip_loc[i] = '0' * (8 - len(ip_loc[i])) + ip_loc[i]
    return ip_loc


def net_type(ip):
    ip_loc = copy.copy(ip)
    ip_loc = to_bin(ip_loc)
    if ip_loc[0][0] == '0':
        return 'A', '0.0.0.0', '127.255.255.255', '255.0.0.0', 8
    if ip_loc[0][0:2] == '10':
        return 'B', '128.0.0.0', '192.255.255.255', '255.255.0.0', 16
    if ip_loc[0][0:3] == '110':
        return 'C', '192.0.0.0', '223.255.255.255', '255.255.255.0', 24
    if ip_loc[0][0:4] == '1110':
        return 'D', '224.0.0.0', '239.255.255.255', None, 32
    if ip_loc[0][0:4] == '1111':
        return 'E', '240.0.0.0', '255.255.255.255', None, 32
    return error


def net_mask(n, s, i):
    mask = '1' * n
    i = "{0:b}".format(i)
    mask += '0' * (s - len(i)) + i
    mask += '0' * (32 - n - s)
    mask2 = mask[0:8] + '.' + mask[8:16] + '.' + mask[16:24] + '.' + mask[24:32]
    return ip_in(mask2)


def net_mask2(n, s, i):
    mask = n
    i = "{0:b}".format(i)
    mask += '0' * (s - len(i)) + i
    mask2 = mask + '0' * (32 - len(mask))
    mask3 = mask + '1' * (32 - len(mask))
    mask2 = mask2[0:8] + '.' + mask2[8:16] + '.' + mask2[16:24] + '.' + mask2[24:32]
    mask3 = mask3[0:8] + '.' + mask3[8:16] + '.' + mask3[16:24] + '.' + mask3[24:32]
    return ip_in(mask2), ip_in(mask3)


def main():
    ip = ip_in(input("Введите ip:"))
    if ip == error:
        print(ip)
        return
    print('Десятичная форма:', ip_out(ip))
    print('Двоичная форма:', ip_out(to_bin(ip)))
    net = net_type(ip)
    print('Тип сети:', net[0])
    print('Начальный адрес:', net[1])
    print('Конечный адрес:', net[2])
    print('Маска класса:', net[3])

    nets = input("Введите кол-во подсетей:")
    hosts = input("Введите кол-во хостов:")
    try:
        nets = math.ceil(math.log(int(nets), 2))
        hosts = math.ceil(math.log(int(hosts) + 2, 2))
    except:
        print(error)
        return
    if nets + hosts + net[4] > 32:
        print('Невозможные условия')
        return
    hosts = 32 - net[4] - nets
    mask = ''
    for i in range(32):
        if i < net[4] + nets:
            mask += '1'
        else:
            mask += '0'
        if i % 8 == 7 and i != 31:
            mask += '.'
    mask = ip_in(mask)
    print("Маска:", ip_out(to_bin(mask)))
    print("Кол-во IP-адресов в каждой подсети:", 2 ** hosts)
    print("Кол-во IP-адресов в каждой подсети для назначения хостам:", 2 ** hosts - 2)
    input()
    for i in range(2 ** nets):
        print()
        print("Подсеть", i)
        m = net_mask(net[4], nets, i)
        print("Маска:", ip_out(to_bin(m)))
        m = net_mask2(''.join(to_bin(ip)[0:net[4] // 8]), nets, i)
        print("Начало сети:", ip_out(m[0]))
        print("Конец сети:", ip_out(m[1]))
        print("Первые 5 допустимых IP-адресов:")
        for _ in range(5):
            m[0][3] += 1
            print(ip_out(m[0]))
        print("Последние 5 допустимых IP-адресов:")
        for _ in range(5):
            m[1][3] -= 1
            print(ip_out(m[1]))


main()

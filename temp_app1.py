k = 'name = <USER_NAME>'

print(k.find('<'))
print(k.find('<', 8))
print(k[7:18])

t = {
    'USER_NAME': 'SunilDuvvuru',
    'pass':"safdfsd"
}
print('USER_NAME111' in t)
print(k.replace(k[7:18], t['USER_NAME']))
print(k)

import requests

with open('kb.txt') as f:
    f = f.readlines()

res = open("res.txt", "a")  # append mode
for el in f:
    d = el.split('/')
    resp = requests.get(f'https://support.mts.ru/api/v1/articles/by-sefurl?articleSefUrl={d[-1].strip('\n')}&productSefUrl={d[3].strip('\n')}')
    res.write(str(resp.json()) + '\n')
res.close()
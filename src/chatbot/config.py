host = 'https://api.gotinder.com'

with open('smstoken.txt') as f:
    line = f.readlines()
    tinder_token = line[0].split(",")[0]
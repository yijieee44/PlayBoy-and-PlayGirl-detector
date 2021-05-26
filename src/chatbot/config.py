host = 'https://api.gotinder.com'

with open('src/cred/smstoken.txt') as f:
    line = f.readlines()
    tinder_token = line[0].split(",")[0]
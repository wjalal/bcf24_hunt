import hashlib

def quiz():
    print('SET TRANSACTION READ WRITE;')

    for line in open('puzzles.txt').readlines():
        vars = line.split('\t')
        id = vars[0].strip()[0]
        link = vars[1].strip()
        answer = vars[2].strip()
        print('INSERT INTO quiz (id, link, answer) ')
        print(f'VALUES (\'{id}\', \'{link}\', \'{answer}\');')

    print('COMMIT;')

def user():
    print('SET TRANSACTION READ WRITE;')

    for line in open('users.txt').readlines():
        vars = line.split('\t')
        id = vars[0].strip()
        name = vars[1].strip()
        pwd = vars[2].strip()
        pwd = hashlib.sha256(pwd.encode()).hexdigest()

        token = vars[10].strip() + 'Z'
        if id=='admin':
            role = 'ADMIN'
        else:
            role ='TEAM'
        print('INSERT INTO \"user\"(id, last_time, level_completed, name, pwd, role, token)')
        print(f'VALUES (\'{id}\', NOW(), 0, \'{name}\', \'{pwd}\', \'{role}\', \'{token}\');')

    print('COMMIT;')

# quiz()
user()
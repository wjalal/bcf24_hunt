import hashlib

def quiz():
    print('SET TRANSACTION READ WRITE;')

    for line in open('puzzles.txt').readlines():
        vars = line.split('\t')
        id = vars[0].strip()[0]
        link = vars[1].strip()
        answer = vars[2].strip()
        print('INSERT INTO quiz')
        print(f'VALUES (\'{id}\', \'{link}\', \'{answer}\');')

    print('COMMIT;')

def user():
    print('SET TRANSACTION READ WRITE;')

    for line in open('users.txt').readlines():
        vars = line.split('\t')
        name = vars[0].strip()
        pwd = vars[1].strip()
        pwd = hashlib.sha256(pwd.encode()).hexdigest()

        token = vars[9].strip()
        print('INSERT INTO \"user\"(last_time, level_completed, name, pwd, role, token)')
        print(f'VALUES (NOW(), 0, \'{name}\', \'{pwd}\', \'TEAM\', \'{token}\');')

    print('COMMIT;')

user()
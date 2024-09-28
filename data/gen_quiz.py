import hashlib

def quiz():
    print('SET TRANSACTION READ WRITE;')
    print('DELETE FROM quiz;')
    for line in open('hashed/puzzles_h.tsv').readlines():
        vars = line.split('\t')
        id = vars[0].strip()[0]
        link = vars[1].strip()
        answer = vars[2].strip()
        print('INSERT INTO quiz (id, link, answer) ')
        print(f'VALUES (\'{id}\', \'{link}\', \'{answer}\');')

    print('COMMIT;')

quiz()

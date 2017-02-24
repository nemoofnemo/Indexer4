import sqlite3

def clearTable():
    dbconn = sqlite3.connect('data.db')
    cu = dbconn.cursor()
    cu.execute('DELETE FROM main_table')
    cu.execute('VACUUM')
    cu.execute('DELETE FROM video_table')
    cu.execute('VACUUM')
    cu.execute('DELETE FROM keyword_table')
    cu.execute('VACUUM')
    cu.execute('DELETE FROM tag_table')
    cu.execute('VACUUM')
    cu.execute('DELETE FROM live_table')
    cu.execute('VACUUM')
    cu.execute('DELETE FROM live_tag_table')
    cu.execute('VACUUM')
    cu.execute('DELETE FROM division_table')
    cu.execute('VACUUM')
    dbconn.commit()
    cu.close()
    dbconn.close()


if __name__ == '__main__':
    print 'clear database.'   
    clearTable()
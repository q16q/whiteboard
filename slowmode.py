from datetime import datetime, timedelta
import sqlite3, os

class SlowmodeDB:
    def __init__(self) -> None:
        newdb = not os.path.exists('slowmode.db')
        self.con = sqlite3.connect('slowmode.db')
        self.cur = self.con.cursor()

        if newdb:
            self.cur.execute("CREATE TABLE slowmode(user, slowmode)")
    
    def check_slowmode(self, uid: int) -> any:
        res = self.cur.execute("SELECT slowmode FROM slowmode WHERE user = ?", (str(uid),))
        res = res.fetchone()
        
        if not res:
            return (True, None)
        res = float(res[0])
        res = int(f"{res:10.0f}")
        if res <= (datetime.now() - timedelta(hours = 1)).timestamp():
            return (True, res)
        else:
            return (False, res)

    def user_exists(self, uid: int) -> bool:
        res = self.cur.execute("SELECT user FROM slowmode WHERE user = ?", (str(uid),))
        if res.fetchone():
            return True
        else:
            return False
        
    def set_slowmode(self, uid: int, slowmode: int) -> None:
        if not self.user_exists(uid):
            self.cur.execute('INSERT INTO slowmode VALUES (?, ?)', (str(uid),str(slowmode),))
        else:
            self.cur.execute('UPDATE slowmode SET slowmode = ? WHERE user = ?', (str(slowmode),str(uid),))
        
        self.con.commit()
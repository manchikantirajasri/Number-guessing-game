import sqlite3, random, math, os, json, csv
from datetime import datetime, date

DB = "guess_game.db"
CONFIG_FILE = "config.json"

DEFAULT_CONFIG = {
    "max_attempt_multiplier": 1.0,
    "enable_cheat_detection": True,
    "enable_achievements": True,
    "daily_range": 500
}


# ---------------- CONFIG ----------------
def load_config():
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w") as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)
    with open(CONFIG_FILE) as f:
        return json.load(f)


CONFIG = load_config()


# ---------------- DATABASE ----------------
class DBManager:
    def __init__(self):
        self.conn = sqlite3.connect(DB)
        self.create()

    def create(self):
        c = self.conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS players(
            id INTEGER PRIMARY KEY, name TEXT UNIQUE)""")

        c.execute("""CREATE TABLE IF NOT EXISTS games(
            id INTEGER PRIMARY KEY,
            player_id INTEGER,
            secret INTEGER,
            attempts INTEGER,
            max_attempts INTEGER,
            status TEXT,
            replay TEXT,
            daily INTEGER,
            start_time TEXT,
            end_time TEXT)""")

        c.execute("""CREATE TABLE IF NOT EXISTS achievements(
            player_id INTEGER,
            name TEXT,
            UNIQUE(player_id, name))""")

        self.conn.commit()

    def player(self, name):
        c = self.conn.cursor()
        c.execute("INSERT OR IGNORE INTO players(name) VALUES(?)", (name,))
        self.conn.commit()
        return c.execute("SELECT id FROM players WHERE name=?", (name,)).fetchone()[0]


# ---------------- GAME ENGINE ----------------
class GuessGame:
    def __init__(self):
        self.db = DBManager()
        self.player = None
        self.pid = None

    def daily_number(self):
        random.seed(date.today().isoformat())
        return random.randint(1, CONFIG["daily_range"])

    def hint(self, secret, guess):
        diff = abs(secret - guess)
        if diff == 0:
            return "Correct"
        if diff <= 5:
            return "🔥 Extremely close"
        if diff <= 15:
            return "Warm"
        if diff <= 50:
            return "Cold"
        return "❄️ Very far"

    def math_hint(self, n):
        if n % 2 == 0:
            return "Even number"
        if all(n % i for i in range(2, int(math.sqrt(n)) + 1)):
            return "Prime number"
        return "Composite number"

    def start_game(self, daily=False):
        secret = self.daily_number() if daily else random.randint(1, 100)
        max_attempts = int(10 * CONFIG["max_attempt_multiplier"])
        replay = []

        c = self.db.conn.cursor()
        c.execute("""INSERT INTO games(player_id, secret, attempts, max_attempts,
                    status, replay, daily, start_time)
                    VALUES(?,?,?,?,?,?,?,?)""",
                  (self.pid, secret, 0, max_attempts, "ACTIVE", "", int(daily), datetime.now()))
        gid = c.lastrowid
        self.db.conn.commit()

        low, high = 1, 100

        while True:
            guess = int(input("Your guess: "))
            replay.append(guess)

            if CONFIG["enable_cheat_detection"]:
                if guess < low or guess > high:
                    print("⚠️ Cheating detected: impossible guess range")

            if guess < secret:
                low = max(low, guess + 1)
            elif guess > secret:
                high = min(high, guess - 1)

            c.execute("UPDATE games SET attempts = attempts + 1 WHERE id=?", (gid,))
            self.db.conn.commit()

            if guess == secret:
                print("🎉 You won!")
                self.finish(gid, "WIN", replay)
                self.achievements(gid)
                return

            print("Hint:", "Higher" if guess < secret else "Lower")
            print("Distance:", self.hint(secret, guess))

            if len(replay) == max_attempts // 2:
                print("Math hint:", self.math_hint(secret))

            if len(replay) >= max_attempts:
                print("❌ You lost. Number was", secret)
                self.finish(gid, "LOSS", replay)
                return

    def finish(self, gid, status, replay):
        self.db.conn.execute("""UPDATE games
            SET status=?, replay=?, end_time=?
            WHERE id=?""",
            (status, json.dumps(replay), datetime.now(), gid))
        self.db.conn.commit()

    def achievements(self, gid):
        if not CONFIG["enable_achievements"]:
            return
        c = self.db.conn.cursor()
        c.execute("INSERT OR IGNORE INTO achievements VALUES(?,?)",
                  (self.pid, "First Win"))
        if c.execute("SELECT attempts FROM games WHERE id=?", (gid,)).fetchone()[0] <= 3:
            c.execute("INSERT OR IGNORE INTO achievements VALUES(?,?)",
                      (self.pid, "Sharp Shooter"))
        self.db.conn.commit()

    def export_analytics(self):
        rows = self.db.conn.execute("""
            SELECT p.name, g.status, g.attempts, g.daily
            FROM games g JOIN players p ON g.player_id=p.id
        """).fetchall()

        with open("analytics.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Player", "Result", "Attempts", "Daily"])
            writer.writerows(rows)

        print("📊 Analytics exported to analytics.csv")

    def start(self):
        self.player = input("Player name: ").title()
        self.pid = self.db.player(self.player)

        while True:
            print("""
1. New Game
2. Daily Challenge
3. Export Analytics
4. Exit
""")
            ch = input("Choose: ")
            if ch == "1":
                self.start_game()
            elif ch == "2":
                self.start_game(daily=True)
            elif ch == "3":
                self.export_analytics()
            else:
                break


if __name__ == "__main__":
    GuessGame().start()

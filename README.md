# Advanced Number Guessing Game - CLI

A production-grade Python CLI Number Guessing Game with database persistence, daily challenges, achievements, replay system, analytics export, and cheat detection.

This project goes far beyond a basic guessing game and demonstrates real software engineering concepts like state persistence, data modeling, analytics, and extensible design.

---

## 📌 Features Overview

### 🎮 Core Gameplay
* Play a classic number guessing game with intelligent hints
* Multiple attempts with adaptive feedback
* Logical range narrowing for efficient guessing

### 📅 Daily Challenge Mode
* Same secret number for all players on the same day
* Number changes automatically every day
* Encourages fair competition and consistency

### 🧠 Smart Hint System
* Direction hints (Higher / Lower)
* Distance-based hints:
  * 🔥 Extremely Close
  * 🌡️ Warm
  * 🧊 Cold
  * ❄️ Very Far
* Mathematical hints (Prime / Even / Composite) at mid-game

### 🛑 Cheat / Inconsistency Detection
* Detects impossible guesses based on narrowed range
* Warns the player if guesses contradict earlier hints
* Demonstrates logical validation and defensive programming

### 💾 Database-Powered (SQLite)

The game uses SQLite for full persistence.

**Stored Data:**
* Player profiles
* Game history
* Attempts and outcomes
* Replay data (every guess)
* Achievements earned
* Daily challenge participation

**No text files. No temporary memory. Everything is queryable, resumable, and exportable.**

### 🏆 Achievements System

Players can unlock achievements such as:
* **First Win** – Win your first game
* **Sharp Shooter** – Win within 3 attempts

Achievements are stored permanently and can be extended easily.

### 🔁 Replay System
* Every guess is stored in the database
* Enables:
  * Post-game analysis
  * Future replay viewing
  * Debugging and analytics

### 📊 Analytics Export
* Export all game data to a CSV file
* Useful for:
  * Data analysis
  * Visualizations
  * Performance tracking

**Example exported fields:**
```
Player Name | Result | Attempts | Daily Challenge
```

### ⚙️ Configuration Support

The game uses a `config.json` file for easy customization.

**Example Configuration:**
```json
{
  "max_attempt_multiplier": 1.0,
  "enable_cheat_detection": true,
  "enable_achievements": true,
  "daily_range": 500
}
```

You can:
* Increase or decrease difficulty
* Enable/disable features
* Change daily challenge range

---

## 📁 Project Structure
```
.
├── guess_game.py      # Main game file
├── guess_game.db      # SQLite database (auto-created)
├── config.json        # Configuration file
├── analytics.csv      # Exported analytics (generated)
├── README.md
```

---

## ▶️ How to Run

### Requirements
* Python 3.9+ (tested on Python 3.12)
* No external dependencies required

### Run the Game
```bash
python guess_game.py
```

---

## 🧭 Game Menu
```
1. New Game
2. Daily Challenge
3. Export Analytics
4. Exit
```

### New Game
* Random secret number
* Standard gameplay with hints and achievements

### Daily Challenge
* One shared number per day
* Same range for all players
* Encourages optimal guessing strategy

### Export Analytics
* Generates `analytics.csv`
* Contains full historical game data

---

## 🧪 Technical Highlights

* SQLite relational data modeling
* Defensive programming & validation
* Replay and analytics architecture
* Configuration-driven behavior
* Python 3.12–safe datetime handling
* Clean, extensible CLI design

---

## 🚀 Why This Project Stands Out

✔ Not a toy project  
✔ Persistent database-backed gameplay  
✔ Analytics-ready design  
✔ Real-world engineering patterns  
✔ Resume & interview worthy  
✔ Highly extensible architecture  

This project is ideal for showcasing:
* Python fundamentals
* Database integration
* CLI UX design
* Logical reasoning and validation
* Software engineering maturity

---

## 🔮 Future Enhancements

* Rich UI (colors, progress bars)
* Daily leaderboards
* One-attempt-per-day lock
* Replay viewer
* Docker & pip packaging
* Web version (FastAPI + React)

---

## 👨‍💻 Author

**Suhaas S**  
Data Science & AI Undergraduate  
Interested in building practical, scalable, and well-engineered systems.

---

## ⭐ If You Like This Project

Give it a ⭐ on GitHub — it motivates continuous improvement!

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!  

---


---

**Built with 💙 and Python**

# 🌙 MoodMate – A Mood-Based Journal with AI Quotes

**MoodMate** is a mood-based journal web app built with **Django**.  
It allows users to record their daily mood and short notes — and in return, it displays a comforting or motivational quote that matches their mood 💬

This project is part of my **7-day Django learning challenge**, where I build and polish one complete app step by step.

---

## ✨ Features

- 📝 Add daily mood and a short journal entry
- 💬 Get mood-based motivational quotes (via API or local data)
- 🔒 User authentication (signup, login, logout)
- 📜 View mood history (recent entries, mood filter)
- 📊 Simple dashboard (optional mood frequency chart)
- 🎨 Clean and responsive Bootstrap UI

---

## 🗓️ Development Plan

### 🕐 **Day 1 – Setup & Models**

- Create Django project `moodmate`
- Create app `journal`
- Define `MoodEntry` model:
  - user (ForeignKey)
  - date (auto_now_add=True)
  - mood (choices: Happy, Sad, Tired, Excited, Calm)
  - note (TextField)
- Register model in admin and test

### 🕑 **Day 2 – Forms & Views**

- Create form to add new mood entry
- Create views to add and display entries
- Design templates with Bootstrap

### 🕒 **Day 3 – Authentication**

- Add signup, login, logout using Django’s built-in auth
- Protect routes so each user can only access their own entries

### 🕓 **Day 4 – Quotes Integration**

- Connect to ZenQuotes API or local `quotes.json`
- Show a quote based on the user’s selected mood

### 🕔 **Day 5 – Dashboard**

- Add recent entries section
- Display mood statistics (optional: Chart.js)

### 🕕 **Day 6 – UI Polish**

- Add Bootstrap cards, navbar, footer, and icons
- Make pages mobile-responsive

### 🕖 **Day 7 – Testing & Final Touches**

- Test all CRUD operations
- Fix UI bugs
- (Optional) Deploy on Render or PythonAnywhere

---

## ⚙️ Tech Stack

| Layer             | Technology                            |
| ----------------- | ------------------------------------- |
| Backend           | Django (Python)                       |
| Frontend          | HTML, CSS, Bootstrap                  |
| Database          | SQLite                                |
| Optional API      | [ZenQuotes.io](https://zenquotes.io/) |
| Charts (optional) | Chart.js                              |

---

## 💡 Goal

To build a simple, meaningful web app that helps users track their emotions and get a comforting quote in return 🌸

---

### ✨ Author

Developed by **Sunita Chaulagain**

> _“Let your mood speak, and let your words heal.”_

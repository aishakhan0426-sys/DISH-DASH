# 🍛 Dish Dash – Smart Recipe Recommendation System

Dish Dash is an interactive desktop application built with Python and Tkinter that helps you discover recipes, manage your own collection, and get instant AI‑powered solutions to cooking mishaps.

---

## ✨ Features

* **Smart Recommendation Pipeline** – Rank recipes by time and ingredient match using a custom priority queue.
* **AI Troubleshooting Chat** – Get instant fixes for burnt food, excess salt, overpowering spice, curdling, and 50+ other common kitchen issues.
* **Full CRUD for Custom Recipes** – Add, update, and delete your own recipes with persistent storage in `recipe_db.json`.
* **Linked‑List Step Tracker** – Walk through recipe steps seamlessly one by one.
* **FIFO Action Queue** – View live system actions and background processes as they happen.
* **3 Built‑in Themes** – Switch between **Light**, **Dark**, and **Moderate** modes on the fly.
* **Huge Recipe Database** – Pre-loaded with 100+ recipes across Desi, Continental, East Asian, South East Asian, and West/Central Asian cuisines.

---

## 🛠️ Tech Stack

* **Language:** Python 3.10+
* **GUI Framework:** Tkinter
* **Data Structures:** Custom implementations of `PriorityQueue`, `Stack`, `LinkedList`, and `Queue`
* **Storage:** JSON for persistent recipe data

---

## 🚀 How to Run

> **Note:** This project relies entirely on the Python standard library. No external `pip` dependencies are required!

```bash
# Clone the repository
git clone [https://github.com/yourusername/dish-dash.git](https://github.com/yourusername/dish-dash.git)

# Navigate to the project directory
cd dish-dash

# Run the application
python main.py
```
## 📂 Project Structure

**├── main.py**              
**├── ai_engine.py**        
**├── data_structures.py**   
**└── recipe_db.json**       

---

## 📌 Future Ideas
* [ ] Export/import custom recipes as shareable files.
* [ ] Migrate to a Web/Mobile frontend (Flask/FastAPI + React/Flutter).
* [ ] Integrate nutritional info tracking and automated meal planning.

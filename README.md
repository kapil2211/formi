# formi


# 🏨 Moustache Escapes - Nearest Property API

This FastAPI backend helps the tele-calling team of [Moustache Escapes](https://www.moustachescapes.com/) quickly find the nearest Moustache property based on the customer's location, even with minor typos.

## 🚀 Features

- 🔍 Query any city/state/area in India
- 🧠 Handles spelling mistakes in user input (e.g., `delih` → `Delhi`)
- 📍 Returns the nearest property within a **50km** radius
- ⚡ Response time under **2 seconds**
- 🌍 Calculates real distances using **latitude/longitude**
- 🌐 Live-deployed on **Render**

---

## 🛠️ Tech Stack

- **FastAPI** for backend
- **Uvicorn** ASGI server
- **Geopy** for distance and geocoding
- **RapidFuzz** for fuzzy matching
- **Render** for hosting

---

## 📦 Installation (for local development)

```bash
git clone https://github.com/kapil2211/formi.git
cd formi
pip install -r requirements.txt
uvicorn main:app --reload

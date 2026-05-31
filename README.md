# 🏠 PropIQ Property Scraper & AI Market Analyzer

> Real-time Egyptian property market intelligence powered by AI. Scrapes live listings, analyzes price trends, and generates institutional-grade market insights using Google Gemini.

![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-336791?style=flat&logo=postgresql)
![Gemini](https://img.shields.io/badge/Google_Gemini-2.0_Flash-4285F4?style=flat&logo=google)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=flat&logo=streamlit)
![Pandas](https://img.shields.io/badge/Pandas-Data_Analysis-150458?style=flat&logo=pandas)

---

## ✨ What It Does

PropIQ Property Scraper collects real estate listings from the Egyptian market, stores them in PostgreSQL, and uses AI to generate market insights — automatically, every 24 hours.

- 📡 **Live scraping** — collects property listings with price, area, location, bedrooms
- 🗄️ **PostgreSQL storage** — persistent database with deduplication
- 🤖 **AI market analysis** — Gemini generates insights from real data (avg price, price/m², trends)
- 📊 **Streamlit dashboard** — interactive UI with property cards, charts, and AI insights
- ⏱️ **Auto-scheduled** — APScheduler runs the scraper every 24 hours automatically
- 🔍 **Advanced filtering** — filter by location, price range, bedrooms, property type

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend API | FastAPI |
| Database | PostgreSQL + SQLAlchemy |
| Migrations | Alembic |
| AI | Google Gemini 2.0 Flash |
| Data Analysis | Pandas |
| Web Scraping | BeautifulSoup + Requests |
| Scheduling | APScheduler |
| Dashboard | Streamlit |
| Server | Uvicorn |

---

## 📁 Project Structure

```
property-scraper/
├── main.py              # FastAPI app + routes + scheduler
├── models.py            # SQLAlchemy DB models
├── database.py          # PostgreSQL connection
├── streamlit_app.py     # Interactive Streamlit dashboard
├── seed.py              # Seed realistic Egyptian property data
├── services/
│   ├── scraper.py       # Web scraper (BeautifulSoup)
│   └── ai.py            # Gemini AI market analysis
├── alembic/             # Database migrations
├── .env                 # Environment variables
├── .env.example
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- PostgreSQL 15+
- Google Gemini API key (free at `aistudio.google.com`)

### 1. Clone the repo
```bash
git clone https://github.com/codedbybodi/property-scraper.git
cd property-scraper
```

### 2. Create virtual environment
```bash
python -m venv .venv
.venv\Scripts\activate     # Windows
source .venv/bin/activate  # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
Create a `.env` file:
```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/property_scraper_db
GEMINI_API_KEY=your-gemini-api-key
```

Get a free Gemini API key: `https://aistudio.google.com/app/apikey`

### 5. Create the database
In pgAdmin: right click Databases → Create → `property_scraper_db`

### 6. Run migrations
```bash
alembic upgrade head
```

### 7. Seed with Egyptian property data
```bash
python seed.py
```

### 8. Start the API
```bash
uvicorn main:app --reload
```

### 9. Start the Streamlit dashboard
```bash
streamlit run streamlit_app.py
```

- API: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`
- Dashboard: `http://localhost:8501`

---

## 📖 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Health check |
| POST | `/scrape` | Trigger manual scrape |
| GET | `/properties` | List properties with filters |
| GET | `/properties/count` | Total property count |
| GET | `/analyze` | AI market analysis |

### Query Parameters for `GET /properties`

| Parameter | Type | Example |
|---|---|---|
| `location` | string | `?location=new+cairo` |
| `min_price` | float | `?min_price=1000000` |
| `max_price` | float | `?max_price=5000000` |
| `bedrooms` | int | `?bedrooms=3` |
| `skip` | int | `?skip=0` |
| `limit` | int | `?limit=20` |

### Example: AI Market Analysis
```bash
curl "http://localhost:8000/analyze?location=New+Cairo"
```

**Response:**
```json
{
  "location": "New Cairo",
  "total_listings": 5,
  "avg_price_egp": 3660000.0,
  "max_price_egp": 6500000.0,
  "min_price_egp": 950000.0,
  "avg_area_m2": 171.0,
  "avg_price_per_m2": 21403.5,
  "avg_by_type": {
    "apartment": 2225000.0,
    "penthouse": 6500000.0
  },
  "ai_analysis": "New Cairo's property market shows strong growth..."
}
```

---

## 📊 Dashboard Features

### Properties Tab
- Property cards with price, location, bedrooms, area, type
- Real-time filtering by location, price, bedrooms

### Market Analysis Tab
- Key metrics: total listings, avg price, avg price/m², avg area
- Bar chart: average price by property type
- Min/max price range

### AI Insights Tab
- AI-generated market analysis using real data
- Investment potential and buyer recommendations
- Powered by Google Gemini 2.0 Flash

---

## ⚙️ Automated Scheduling

The scraper runs automatically every 24 hours via APScheduler:

```python
scheduler.add_job(scheduled_scrape, "interval", hours=24)
```

Trigger manually anytime:
```bash
curl -X POST http://localhost:8000/scrape
```

---

## 🗄️ Database Models

### Property
```
id, title, price, area_m2, bedrooms, location,
property_type, source_url, scraped_at
```

### MarketInsight
```
id, location, avg_price, avg_price_per_m2,
total_listings, ai_analysis, generated_at
```

---

## 🌍 Egyptian Market Coverage

Currently tracks properties across:
- New Cairo · Maadi · Zamalek · Sheikh Zayed
- 6th of October · Heliopolis · Madinaty
- Nasr City · New Capital · North Coast

---

## 📄 License

MIT License — open source and free to use.
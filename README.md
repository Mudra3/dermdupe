# dermdupe
Skincare product similarity engine that compares ingredient lists across major retailers and finds lower cost alternatives.
# DermDupe!!!
### AI-powered skincare ingredient analysis that discovers high-quality, lower-cost alternatives.

DermDupe is a full-stack web application that helps users identify affordable skincare products with ingredient profiles comparable to premium brands. By combining web scraping, natural language processing, and similarity algorithms, the platform analyzes product formulations to recommend cost-effective alternatives based on ingredient composition rather than marketing claims.

**THE LIVE DEMO** on
https://dermdupe.onrender.com

## Features:

DermDupe supports multiple search workflows to make ingredient analysis intuitive for both skincare enthusiasts and casual users.

* **Ingredient Analysis** – Paste an ingredient list to instantly find products with highly similar formulations.
* **AI-Powered Search** – Describe your skincare goals in natural language, and an AI assistant translates your request into ingredient-based recommendations.
* **Product Lookup** – Search for a skincare product by name and receive comparable alternatives ranked by ingredient similarity.

Rather than relying on brand reputation or price, DermDupe evaluates products using their actual ingredient lists, helping users discover alternatives with over **90% ingredient overlap**.


## Tech Stack:

| Layer             | Technology                   |
| ----------------- | ---------------------------- |
| Backend           | Python, Flask                |
| Database          | SQLite                       |
| Data Collection   | BeautifulSoup4, Requests     |
| Similarity Engine | Jaccard Similarity Algorithm |
| Frontend          | HTML, CSS, JavaScript        |
| Deployment        | Render                       |

## How It Works:

DermDupe's recommendation engine compares skincare formulations using the **Jaccard Similarity Index**, a set-based algorithm that measures overlap between ingredient lists.

The application first collects and normalizes ingredient data through a custom web-scraping pipeline. Ingredients are standardized, converted into comparable sets, and scored using the similarity algorithm. Products are then ranked by formulation similarity, allowing users to quickly identify alternatives that closely match the original product.

This approach prioritizes ingredient composition over branding, enabling recommendations that are transparent, explainable, and data-driven.
similarity = |A ∩ B| / |A ∪ B|
This calculates the intersection over union of two ingredient sets — the same technique used in machine learning and data science to measure similarity between sets. Products scoring 90%+ are flagged as dupes.

---

## In depth features: 

- Scrapes 300+ skincare products across 8 categories from INCI Decoder
- Real-time product lookup by name
- AI-powered natural language search
- Ingredient match score with visual progress bar
- Duplicate prevention in database

## Run locally:
```bash
git clone https://github.com/Mudra3/dermdupe.git
cd dermdupe
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python frontend/app.py
```

Visit `http://127.0.0.1:5000`

## Project Structure
## Project Structure
dermdupe/
├── scraper/ # Web scraper for INCI Decoder
├── database/ # SQLite database setup and queries
├── matcher/ # Jaccard similarity algorithm
├── aiSearch/ # AI-powered natural language search
├── frontend/ # Flask app and HTML templates
└── data/ # SQLite database file

Built by Mudra, studying Information Systems at NJIT.
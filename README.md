# California House Price Prediction

A full-stack Machine Learning project that predicts California house prices using a **Random Forest Regressor** model, served via a **FastAPI** backend with an interactive **HTML/CSS/JS** frontend.

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green?logo=fastapi&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML-orange?logo=scikit-learn&logoColor=white)
![Render](https://img.shields.io/badge/Deployed%20on-Render-blueviolet?logo=render&logoColor=white)

---

##  Project Structure

```
CL_house_price_prediction/
│
├── backend/                  # ← Deploy this folder to Render
│   ├── main.py               # FastAPI application
│   ├── explore.py            # Model training script
│   ├── requirements.txt      # Python dependencies
│   ├── Procfile              # Render start command
│   ├── house_model.joblib    # Trained ML model (see setup)
│   ├── house_features.joblib # Feature list
│   └── test.csv              # Sample CSV for testing
│
├── frontend/                 # ← Static frontend (GitHub Pages / local)
│   ├── index.html            # Main prediction form
│   ├── upload.html           # CSV bulk prediction page
│   ├── about.html            # About the project
│   └── style.css             # Glassmorphism UI styles
│
├── .gitignore
└── README.md
```

---

##  Machine Learning Model

| Detail            | Value                        |
|-------------------|------------------------------|
| **Algorithm**     | Random Forest Regressor      |
| **Library**       | Scikit-Learn                 |
| **Dataset**       | California Housing (20,640 rows) |
| **Problem Type**  | Regression                   |
| **Avg Error**     | ~$39,000                     |

### Features Used

| Feature     | Description                              |
|-------------|------------------------------------------|
| `MedInc`    | Median income in the block group         |
| `HouseAge`  | Average age of houses                    |
| `AveRooms`  | Average rooms per household              |
| `AveBedrms` | Average bedrooms per household           |
| `Population`| Total population of block group          |
| `AveOccup`  | Average household members                |
| `Latitude`  | Latitude (32–42)                         |
| `Longitude` | Longitude (-125 to -114)                 |

---

##  API Endpoints

| Method | Endpoint        | Description                          |
|--------|-----------------|--------------------------------------|
| GET    | `/`             | Welcome message & API status         |
| GET    | `/health`       | Model info & health check            |
| POST   | `/predict`      | Predict price for single input (JSON)|
| POST   | `/predict-file` | Predict prices for CSV file upload   |

### Example — Single Prediction

**Request:**
```json
POST /predict
{
    "MedInc": 8.3252,
    "HouseAge": 41,
    "AveRooms": 6.9841,
    "AveBedrms": 1.0238,
    "Population": 322,
    "AveOccup": 2.5556,
    "Latitude": 37.88,
    "Longitude": -122.23
}
```

**Response:**
```json
{
    "predicted_price": "$452,600",
    "predicted_price_short": "$453K",
    "confidence_range": "$413,600 to $491,600"
}
```

---

## 🚀Deploy Backend to Render

### Step 1 — Generate the Model File

The `.joblib` model files are too large for GitHub (~138 MB). You need to generate them on your machine first:

```bash
cd backend
pip install scikit-learn pandas joblib
python explore.py
```

This creates `house_model.joblib` and `house_features.joblib` in the `backend/` folder.

### Step 2 — Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/CL_house_price_prediction.git
git push -u origin main
```

> ⚠️ The `.gitignore` excludes `.joblib` files. You must either:
> - **Option A:** Remove `*.joblib` from `.gitignore` and use [Git LFS](https://git-lfs.github.com/) to push large files, **OR**
> - **Option B:** Run `explore.py` as part of Render's build command (see below).

### Step 3 — Create a Render Web Service

1. Go to [render.com](https://render.com) → **New** → **Web Service**
2. Connect your GitHub repository
3. Configure:

| Setting           | Value                                                        |
|-------------------|--------------------------------------------------------------|
| **Name**          | `cl-house-price-prediction`                                  |
| **Root Directory**| `backend`                                                    |
| **Runtime**       | `Python 3`                                                   |
| **Build Command** | `pip install -r requirements.txt && python explore.py`       |
| **Start Command** | `uvicorn main:app --host 0.0.0.0 --port $PORT`              |

> The build command installs dependencies **and** trains the model, so the `.joblib` files are generated on Render itself.

4. Click **Create Web Service**

Your API will be live at: `https://cl-house-price-prediction.onrender.com`



## Host Frontend (Optional)

The `frontend/` folder contains static HTML/CSS/JS files. You can host them using:

- **GitHub Pages** — Push and enable Pages from Settings
- **Netlify** — Drag & drop the `frontend/` folder
- **Open locally** — Just open `frontend/index.html` in a browser

---

##  Run Locally

### Backend
```bash
cd backend
pip install -r requirements.txt
python explore.py          # Generate model (first time only)
uvicorn main:app --reload  # Start server at http://127.0.0.1:8000
```

### Frontend
Open `frontend/index.html` in your browser.

> For local development, change `API_BASE_URL` in the HTML files back to `http://127.0.0.1:8000`.

---

## 📊 Sample CSV Format

Use this format for bulk predictions via `/predict-file`:

```csv
MedInc,HouseAge,AveRooms,AveBedrms,Population,AveOccup,Latitude,Longitude
8.3252,41,6.9841,1.0238,322,2.5556,37.88,-122.23
8.3014,21,6.2381,0.9719,2401,2.1098,37.86,-122.22
7.2574,52,8.2881,1.0734,496,2.8023,37.85,-122.24
```

A sample `test.csv` file is included in the `backend/` folder.

---

## Technologies Used

- **Python** — Core language
- **FastAPI** — Backend API framework
- **Scikit-Learn** — ML model training
- **Pandas** — Data processing
- **Joblib** — Model serialization
- **Pydantic** — Input validation
- **HTML / CSS / JavaScript** — Frontend UI
- **Render** — Backend deployment

---

##  License

This project is open-source and available for learning and personal use.

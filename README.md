# California House Price Prediction

A full-stack machine learning application that predicts California house prices using a Random Forest Regressor model, a FastAPI backend, and a responsive HTML/CSS/JavaScript frontend.

This project was built to understand the complete journey of a machine learning model — from training and evaluation to API development, frontend integration, version control, handling large model files, and cloud deployment.

The final result is a working web application where a user can enter housing information, receive a predicted house price, or upload a CSV file for multiple predictions.

---

## Live Application

### Frontend

[Open the California House Price Predictor](https://justayushman.github.io/california-house-price-prediction/frontend/index.html)

The frontend is hosted using GitHub Pages.

### Backend API

[Open the FastAPI backend](https://ml-api-eew8.onrender.com)

The backend is deployed using Render.

### API Documentation

[Open FastAPI Swagger Documentation](https://ml-api-eew8.onrender.com/docs)

FastAPI automatically provides interactive API documentation through Swagger UI.

---

## Project Overview

The project is divided into two independent but connected parts:

### Backend

The backend is responsible for:

* Loading the trained machine learning model
* Validating incoming data
* Making predictions
* Returning prediction results as JSON
* Accepting CSV files for bulk predictions
* Providing health and status endpoints
* Serving the model through a REST API

The backend is built with FastAPI and deployed on Render.

### Frontend

The frontend provides the user interface for interacting with the model.

It includes:

* A manual house-price prediction form
* Input validation
* Prediction results
* Bulk CSV prediction
* An About page explaining the project
* A glassmorphism-inspired interface
* JavaScript-based communication with the FastAPI backend

The frontend is deployed independently using GitHub Pages.

---

## Project Architecture

```text
                 User
                   |
                   v
        +---------------------+
        |      Frontend       |
        |  HTML / CSS / JS    |
        |    GitHub Pages     |
        +----------+----------+
                   |
                   | HTTP Requests
                   v
        +---------------------+
        |      FastAPI        |
        |      Backend        |
        |      Render         |
        +----------+----------+
                   |
                   v
        +---------------------+
        | Random Forest Model |
        |     .joblib         |
        +----------+----------+
                   |
                   v
          Prediction Result
```

The frontend and backend are hosted separately, but communicate through HTTP API requests.

---

## Repository Structure

```text
california-house-price-prediction/
│
├── backend/
│   ├── main.py
│   ├── explore.py
│   ├── requirements.txt
│   ├── Procfile
│   ├── house_model.joblib
│   ├── house_features.joblib
│   └── test.csv
│
├── frontend/
│   ├── index.html
│   ├── upload.html
│   ├── about.html
│   └── style.css
│
├── .gitignore
├── .gitattributes
└── README.md
```

### Backend Files

| File                    | Purpose                                     |
| ----------------------- | ------------------------------------------- |
| `main.py`               | FastAPI application and API endpoints       |
| `explore.py`            | Model training and evaluation               |
| `requirements.txt`      | Python dependencies                         |
| `Procfile`              | Process/start command used for deployment   |
| `house_model.joblib`    | Trained Random Forest model                 |
| `house_features.joblib` | Saved feature order used during prediction  |
| `test.csv`              | Sample CSV file for bulk prediction testing |

### Frontend Files

| File          | Purpose                       |
| ------------- | ----------------------------- |
| `index.html`  | Main prediction interface     |
| `upload.html` | CSV bulk prediction interface |
| `about.html`  | Project information           |
| `style.css`   | Styling and visual design     |

---

## Machine Learning

The machine learning component uses the California Housing dataset and a Random Forest Regressor.

### Model Details

| Detail                 | Value                   |
| ---------------------- | ----------------------- |
| Algorithm              | Random Forest Regressor |
| Library                | Scikit-Learn            |
| Problem Type           | Regression              |
| Dataset                | California Housing      |
| Dataset Size           | 20,640 rows             |
| Number of Trees        | 50                      |
| Random State           | 42                      |
| Average Absolute Error | Approximately $39,000   |

The training process uses an 80/20 train-test split.

The model is trained using the following features:

```text
MedInc
HouseAge
AveRooms
AveBedrms
Population
AveOccup
Latitude
Longitude
```

The trained model and the exact feature order are serialized using Joblib.

---

## Features Used by the Model

| Feature      | Description                              |
| ------------ | ---------------------------------------- |
| `MedInc`     | Median income in the block group         |
| `HouseAge`   | Average age of houses in the block group |
| `AveRooms`   | Average number of rooms per household    |
| `AveBedrms`  | Average number of bedrooms per household |
| `Population` | Total population of the block group      |
| `AveOccup`   | Average number of household members      |
| `Latitude`   | Latitude of the location                 |
| `Longitude`  | Longitude of the location                |

The frontend also validates geographic values based on the expected ranges used by the API:

```text
Latitude: 32 to 42
Longitude: -125 to -114
```

---

## Model Training

The training script is located at:

```text
backend/explore.py
```

The model is trained using:

```python
RandomForestRegressor(
    n_estimators=50,
    random_state=42
)
```

After training, two files are created:

```text
house_model.joblib
house_features.joblib
```

The first stores the trained model.

The second stores the feature names and preserves the feature order expected by the model during prediction.

---

## Model Evaluation

The model is evaluated using:

* Mean Absolute Error (MAE)
* R² Score

The project currently reports an average absolute error of approximately:

```text
$39,000
```

This value is also used by the API when displaying the estimated prediction range.

It is important to note that the API field is named `confidence_range`, but this should not be interpreted as a formal statistical confidence interval. In this project, the displayed range is based on adding and subtracting the approximate average absolute error from the predicted value.

---

## FastAPI Backend

The API is implemented in:

```text
backend/main.py
```

FastAPI was chosen because it provides:

* Simple API development
* Automatic request validation
* Pydantic integration
* Automatic interactive API documentation
* High-performance ASGI support
* Easy integration with machine learning models

The trained model is loaded when the API starts.

```python
model = joblib.load(...)
features = joblib.load(...)
```

The API then uses the loaded model to generate predictions without retraining it for every request.

---

## API Endpoints

| Method | Endpoint        | Purpose                                           |
| ------ | --------------- | ------------------------------------------------- |
| `GET`  | `/`             | Returns API welcome message and status            |
| `GET`  | `/health`       | Returns health and model information              |
| `POST` | `/predict`      | Predicts the price for a single house             |
| `POST` | `/predict-file` | Accepts a CSV file and generates bulk predictions |

---

## Root Endpoint

### `GET /`

Returns a basic status message confirming that the API is running.

Example:

```json
{
  "message": "California house prediction API",
  "status": "running",
  "endpoint": "Send POST request to /predict"
}
```

---

## Health Endpoint

### `GET /health`

Returns model and API information.

Example:

```json
{
  "status": "running",
  "model": "Random Forest Regressor",
  "features": [
    "MedInc",
    "HouseAge",
    "AveRooms",
    "AveBedrms",
    "Population",
    "AveOccup",
    "Latitude",
    "Longitude"
  ],
  "avg_error": "$39,000"
}
```

---

## Single Prediction

### `POST /predict`

The endpoint accepts the following JSON structure:

```json
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

The API validates the input using Pydantic before passing the data to the machine learning model.

Example response:

```json
{
    "predicted_price": "$452,600",
    "predicted_price_short": "$453K",
    "confidence_range": "$413,600 to $491,600"
}
```

---

## Bulk CSV Prediction

### `POST /predict-file`

The project also supports batch predictions through CSV uploads.

The user uploads a CSV file containing the required model features.

The API:

1. Checks that the uploaded file is a CSV
2. Reads the file
3. Validates the required columns
4. Checks that data rows exist
5. Passes the data to the trained model
6. Adds a prediction column
7. Returns the resulting CSV file

The generated file contains:

```text
predicted_price_usd
```

along with the original input data.

---

## CSV Format

The CSV must contain the following columns:

```csv
MedInc,HouseAge,AveRooms,AveBedrms,Population,AveOccup,Latitude,Longitude
8.3252,41,6.9841,1.0238,322,2.5556,37.88,-122.23
8.3014,21,6.2381,0.9719,2401,2.1098,37.86,-122.22
7.2574,52,8.2881,1.0734,496,2.8023,37.85,-122.24
```

A sample file is also included in:

```text
backend/test.csv
```

---

## Frontend

The frontend is built using:

* HTML
* CSS
* JavaScript

The main interface allows the user to enter:

```text
Median Income
House Age
Average Rooms
Average Bedrooms
Population
Average Occupancy
Latitude
Longitude
```

The current live frontend also provides navigation to:

* Single Prediction
* Bulk Prediction
* About

The live interface is available here:

https://justayushman.github.io/california-house-price-prediction/frontend/index.html

---

## Frontend and Backend Integration

The frontend communicates with the deployed FastAPI server using HTTP requests.

The general flow is:

```text
User Input
    |
    v
JavaScript
    |
    v
POST /predict
    |
    v
FastAPI
    |
    v
Random Forest Model
    |
    v
Prediction
    |
    v
JSON Response
    |
    v
Frontend Display
```

For bulk predictions, the frontend sends a CSV file to:

```text
POST /predict-file
```

and receives the generated prediction CSV in response.

---

## Deployment

One of the most important parts of this project was getting the trained machine learning model running on a real cloud server.

The application uses two deployment platforms:

| Component   | Platform     |
| ----------- | ------------ |
| Frontend    | GitHub Pages |
| Backend     | Render       |
| Source Code | GitHub       |

---

## Deploying the Backend to Render

The backend is located inside:

```text
backend/
```

Render was configured to use this directory as the backend working directory.

The important deployment configuration is:

```text
Root Directory:
backend
```

The application is started using Uvicorn:

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

The actual deployed service is available at:

https://ml-api-eew8.onrender.com

---

## Large Model Files and Git LFS

One of the challenges in this project was the size of the trained model.

The generated `.joblib` model file was approximately 138 MB, which created a problem when attempting to upload it as a normal GitHub file.

GitHub's standard repository file size limit meant that the model could not simply be committed like a normal source-code file.

To solve this problem, Git Large File Storage (Git LFS) was used.

The process included:

```bash
git lfs install
```

Then the Joblib files were tracked using:

```bash
git lfs track "*.joblib"
```

This generated a `.gitattributes` file that tells Git to handle `.joblib` files using LFS.

The large model files were then committed and pushed through Git LFS.

This was an important practical lesson because machine learning projects often contain model artifacts that are much larger than typical source-code files.

---

## Deployment Issues Solved During Development

The deployment process was not completely straightforward. Several real-world issues had to be identified and fixed.

### 1. Git commands were initially executed outside the repository

The first Git LFS commands were run from:

```text
C:\Users\DELL>
```

instead of inside:

```text
C:\Users\DELL\california-house-price-prediction>
```

The solution was to enter the repository before running Git commands:

```bash
cd california-house-price-prediction
```

---

### 2. Joblib files were ignored by Git

Git initially reported:

```text
The following paths are ignored by one of your .gitignore files
```

because `.joblib` files were excluded by the repository's ignore rules.

The ignore configuration had to be adjusted so that Git LFS could track the model files.

---

### 3. Large model files could not be uploaded normally

The trained model was too large for a normal GitHub upload.

Git LFS solved this problem.

The resulting repository now contains:

```text
.gitattributes
```

along with the tracked `.joblib` model files.

---

### 4. Render could not initially find `requirements.txt`

Render first attempted:

```bash
pip install -r requirements.txt
```

but the file was inside the `backend` directory.

The deployment configuration had to be aligned with the repository structure.

---

### 5. Render could not import `main`

Another deployment error was:

```text
Error loading ASGI app.
Could not import module "main".
```

This occurred because the application was being started from the repository root while the FastAPI application was located inside the `backend` package.

The start command was therefore adjusted to:

```bash
uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```

---

### 6. Model file path problem

After the application itself was successfully imported, Render returned:

```text
FileNotFoundError:
No such file or directory: 'house_model.joblib'
```

The issue was caused by the relative path used when loading the model.

The model was located under:

```text
backend/house_model.joblib
```

while the application was being started relative to the repository root.

The model path was adjusted accordingly so the deployed service could locate the file.

---

### 7. Successful deployment

After resolving the repository structure, dependency path, module path, and model path issues, the Render logs confirmed:

```text
Application startup complete.
Uvicorn running on http://0.0.0.0:10000
Your service is live
```

The deployed API is now publicly accessible.

---

## Running the Project Locally

### 1. Clone the Repository

```bash
git clone https://github.com/JustAyushman/california-house-price-prediction.git
cd california-house-price-prediction
```

---

### 2. Set Up the Backend

```bash
cd backend
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

If the model files are not already available locally, train the model:

```bash
python explore.py
```

This generates:

```text
house_model.joblib
house_features.joblib
```

---

### 3. Run FastAPI

Start the API locally:

```bash
uvicorn main:app --reload
```

The API should then be available at:

```text
http://127.0.0.1:8000
```

FastAPI documentation will be available at:

```text
http://127.0.0.1:8000/docs
```

---

### 4. Run the Frontend

Open:

```text
frontend/index.html
```

in a browser.

For local development, make sure the frontend API URL points to:

```text
http://127.0.0.1:8000
```

instead of the deployed Render URL.

---

## Technologies Used

| Technology    | Purpose                              |
| ------------- | ------------------------------------ |
| Python        | Core programming language            |
| Scikit-Learn  | Machine learning                     |
| Random Forest | Regression model                     |
| Pandas        | Data processing                      |
| Joblib        | Model serialization                  |
| FastAPI       | Backend API                          |
| Pydantic      | Input validation                     |
| Uvicorn       | ASGI server                          |
| HTML          | Frontend structure                   |
| CSS           | Frontend styling                     |
| JavaScript    | Frontend logic and API communication |
| Git           | Version control                      |
| GitHub        | Source-code hosting                  |
| Git LFS       | Large model-file management          |
| Render        | Backend deployment                   |
| GitHub Pages  | Frontend deployment                  |

---

## What I Learned From This Project

This project helped me understand that building a machine learning application does not end after training a model.

The practical workflow involved several different areas:

```text
Dataset
   |
   v
Model Training
   |
   v
Model Evaluation
   |
   v
Model Serialization
   |
   v
FastAPI API
   |
   v
Frontend Integration
   |
   v
Git / GitHub
   |
   v
Git LFS
   |
   v
Cloud Deployment
   |
   v
Debugging
   |
   v
Live Application
```

Some of the most important things I learned through the project were:

* How a trained machine learning model can be serialized and loaded later
* How to expose a model through a REST API
* How FastAPI handles request validation
* How a frontend communicates with a backend API
* How to structure a full-stack machine learning project
* How to use Git and GitHub for version control
* Why large machine learning artifacts require a different storage strategy
* How Git LFS works with large model files
* How deployment environments differ from local environments
* How relative file paths can break a deployed application
* How to read deployment logs and debug errors systematically
* How to separate frontend hosting from backend hosting
* How to take a machine learning model from a local Python script to a publicly accessible application

---

## Development Approach

The main objective of this project was learning by building.

There were several points during development where the application did not work immediately. Instead of treating those errors as something to avoid, they became part of the learning process.

For example, the deployment involved troubleshooting:

```text
Git repository path
       ↓
Git LFS configuration
       ↓
Ignored model files
       ↓
Render requirements path
       ↓
FastAPI module import
       ↓
Model file path
       ↓
Successful deployment
```

That process was important because deploying a real application requires more than writing code that works on a local machine.

It also requires understanding how different tools, environments, and services interact.

---

## Use of AI During Development

AI tools were used during parts of this project as a learning and debugging aid.

The intention was not to blindly copy generated solutions.

Whenever I was stuck, AI was used to:

* Understand an error
* Explore possible approaches
* Debug deployment issues
* Learn unfamiliar concepts
* Improve implementation ideas
* Understand why something was failing

The final goal was to understand the solution rather than simply make the application work.

I believe AI is most useful when it is combined with personal reasoning, experimentation, and verification. Learning how to use AI effectively is becoming an important part of software development, but understanding the underlying concepts still matters.

---

## Current Status

The project is currently deployed and accessible online.

### Frontend

https://justayushman.github.io/california-house-price-prediction/frontend/index.html

### Backend

https://ml-api-eew8.onrender.com

### API Documentation

https://ml-api-eew8.onrender.com/docs

The application supports:

* Single house-price prediction
* Bulk CSV prediction
* Input validation
* Model health/status checking
* Live frontend-to-backend communication
* Cloud-hosted backend inference

---

## Limitations

This project is intended primarily as a learning and portfolio project.

The predicted price is an estimate based on patterns learned from the California Housing dataset. It should not be treated as a professional real-estate valuation.

The reported approximate error of $39,000 also means that individual predictions can differ substantially from actual market values.

The project can be improved further through:

* Better model experimentation
* Hyperparameter tuning
* More detailed evaluation
* Feature engineering
* Improved error analysis
* Authentication and API security
* Production-grade model storage
* Automated testing
* CI/CD
* Monitoring and logging
* Containerization with Docker

---

## Future Improvements

Some possible future improvements include:

1. Compare Random Forest with other regression algorithms
2. Perform systematic hyperparameter tuning
3. Add additional evaluation metrics and visualizations
4. Improve the frontend user experience
5. Add automated tests for API endpoints
6. Add API authentication
7. Introduce better model artifact storage such as object storage
8. Containerize the backend using Docker
9. Add CI/CD through GitHub Actions
10. Add monitoring and structured logging
11. Add model versioning
12. Improve error handling and API documentation

---

## Why I Built This

The main purpose of this project was to move beyond only working with machine learning notebooks.

Training a model in a notebook is one part of machine learning development. Making that model available through an API, connecting it to a frontend, deploying it to the cloud, handling large model files, and debugging the deployment introduced a different set of engineering problems.

This project was an attempt to understand that complete process.

It also helped me become more comfortable with the idea that machine learning and software engineering are closely connected.

---

## License

This project is open-source and intended for learning and personal use.

---

## Author

**Ayushman Sharma**

GitHub:

https://github.com/JustAyushman

Project Repository:

https://github.com/JustAyushman/california-house-price-prediction

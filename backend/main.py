import io
from io import StringIO
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel, Field
from fastapi.responses import StreamingResponse


app = FastAPI()


import os

BASE_DIR = os.path.dirname(__file__)

model_path = os.path.join(BASE_DIR, "house_model.joblib")
features_path = os.path.join(BASE_DIR, "house_features.joblib")

model = joblib.load(model_path)
features = joblib.load(features_path)



class HouseFeatures(BaseModel):
    MedInc: float = Field(gt=0, description="Median income of block group")
    HouseAge: float = Field(ge=0, description="Average age of houses in block group")
    AveRooms: float = Field(gt=0, description="Average number of rooms per household")
    AveBedrms: float = Field(gt=0, description="Average number of bedrooms per household")
    Population: float = Field(gt=0, description="Total population of block group")
    AveOccup: float = Field(gt=0, description="Average number of household members")
    Latitude: float = Field(ge=32, le=42, description="Latitude of block group")
    Longitude: float = Field(ge=-125, le=-114, description="Longitude of block group")



@app.get("/")
def home():
    return {
        "message": "California house prediction API",
        "status": "running",
        "endpoint": "Send POST request to /predict"
    }



@app.get("/health")
def health():
    return {
        "status": "running",
        "model": "Random Forest Regressor",
        "features": features,
        "avg_error": "$39,000"
    }



@app.post("/predict")
def predict(house: HouseFeatures):
    try:
      
        input_data = pd.DataFrame([{
            "MedInc": house.MedInc,
            "HouseAge": house.HouseAge,
            "AveRooms": house.AveRooms,
            "AveBedrms": house.AveBedrms,
            "Population": house.Population,
            "AveOccup": house.AveOccup,
            "Latitude": house.Latitude,
            "Longitude": house.Longitude
        }])

        
        input_data = input_data[features]

        
        predicted = model.predict(input_data)[0]

        
        price_usd = predicted * 100000

        return {
            "predicted_price": f"${price_usd:,.0f}",
            "predicted_price_short": f"${price_usd/1000:,.0f}K",
            "confidence_range": f"${price_usd - 39000:,.0f} to ${price_usd + 39000:,.0f}"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.post("/predict-file")
async def predict_file(file: UploadFile = File(...)):
    
    if not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Please upload a CSV file only"
        )

    try:
        
        contents = await file.read()
        decoded = contents.decode("utf-8")
        df = pd.read_csv(StringIO(decoded))

        
        required_columns = [
            'MedInc', 'HouseAge', 'AveRooms',
            'AveBedrms', 'Population',
            'AveOccup', 'Latitude', 'Longitude'
        ]

        
        missing_columns = [
            col for col in required_columns if col not in df.columns
        ]

        if missing_columns:
            raise HTTPException(
                status_code=400,
                detail=f"These columns are missing from your file: {missing_columns}"
            )

        
        if len(df) == 0:
            raise HTTPException(
                status_code=400,
                detail="The uploaded file has no data rows"
            )

        
        predictions = model.predict(df[required_columns])

        
        df["predicted_price_usd"] = (predictions * 100000).round(0)
        df["predicted_price_usd"] = df["predicted_price_usd"].apply(
            lambda x: f"${x:,.0f}"
            )

        
        output = df.to_csv(index=False)

        

        return StreamingResponse(
            io.StringIO(output),
            media_type="text/csv",
            headers={
                "Content-Disposition": "attachment; filename=predictions.csv"
            }
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing file: {str(e)}"
        )

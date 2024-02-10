import os
import pickle
from typing import Union, Optional

import boto3
from botocore.exceptions import NoCredentialsError
from fastapi import FastAPI, Depends, UploadFile, File, Form, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

import models
from crud import create_user, login_user
from database import SessionLocal, engine
from response import create_response
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def prediction(input_list):
    file_path = 'model/predictor.pickle'

    try:
        with open(file_path, 'rb') as file:
            # Load the pickle file
            data = pickle.load(file)
            print("Pickle file is running correctly.")
            # If you want, you can print or inspect the loaded data
            print("Loaded data:", data)

        pred_value = data.predict(input_list)
        return pred_value

    except Exception as e:
        print("Error loading pickle file:", str(e))


# @app.get("/")
# async def root():
#     pred = prediction([
#         84000, 2022, 0, 0, 0, 0, 0, 1, 0, 0,
#         0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#         0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#         0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#         0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#         0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
#         0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#         0, 0, 0, 0, 0, 0, 1, 0, 0, 0,
#         0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#         0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#         0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
#         1, 0
#     ])
#     print('prediction value >> ', pred)


class CarAd(BaseModel):
    brand: str
    model: str
    mileage: str
    model_year: str
    fuel_type: str
    engine: str
    transmission: str


class User(BaseModel):
    username: str
    email: str
    password: str


class Login(BaseModel):
    username: str
    password: str


@app.post('/api/v1/auth/create-user')
async def create_user_endpoint(user: User, db: Session = Depends(get_db)):
    return create_user(db=db, username=user.username, email=user.email, password=user.password)


@app.post("/api/v1/auth/login-user")
async def login_user_endpoint(login_info: Login, db: Session = Depends(get_db)):
    user = login_user(db=db, username=login_info.username, password=login_info.password)
    if user:
        return {
            "status": "200",
            "message": "Login successful",
            "data": user
        }
    else:
        return "Invalid credentials"


@app.post("/api/v1/post/predict-price")
async def predict_price(car_ad: CarAd):
    print('hello')
    brand_list = ['Ford', 'BMW', 'Mercedes-Benz', 'Chevrolet', 'Porsche', 'Audi', 'Toyota', 'Lexus', 'Jeep',
                  'Land', 'Nissan', 'Cadillac', 'GMC', 'RAM', 'Dodge', 'Tesla', 'Kia', 'Hyundai', 'Subaru', 'Mazda',
                  'Acura', 'Honda', 'INFINITI', 'Volkswagen', 'Lincoln', 'Other', 'Jaguar', 'Volvo', 'Maserati',
                  'Bentley', 'MINI', 'Buick', 'Chrysler', 'Lamborghini', 'Genesis', 'Mitsubishi', 'Alfa', 'Rivian',
                  'Hummer', 'Pontiac', 'Ferrari', 'Rolls-Royce']

    model_list = ['Other', 'M3 Base', 'F-150 XLT', 'Corvette Base', '1500 Laramie', 'Wrangler Sport', 'Camaro 2SS',
                  'Model Y Long Range', 'Mustang GT Premium', '911 Carrera', 'M4 Base', 'F-250 Lariat', 'Explorer XLT',
                  '911 Carrera S', 'E-Class E 350', 'E-Class E 350 4MATIC', 'F-150 Lariat', 'M5 Base', 'ES 350 Base',
                  'F-250 XLT', 'R1S Adventure Package']

    fuel_list = ['Gasoline', 'Hybrid', 'E85 Flex Fuel', 'Diesel', 'Plug-In Hybrid']

    engine_list = [
        '835.0HP Electric Motor Electric Fuel System',
        '2.0L I4 16V GDI DOHC Turbo',
        '355.0HP 5.3L 8 Cylinder Engine Gasoline Fuel',
        '420.0HP 6.2L 8 Cylinder Engine Gasoline Fuel',
        '300.0HP 3.0L Straight 6 Cylinder Engine Gasoline Fuel',
        '240.0HP 2.0L 4 Cylinder Engine Gasoline Fuel',
        '285.0HP 3.6L V6 Cylinder Engine Gasoline Fuel',
        '5.7L V8 16V MPFI OHV',
        '340.0HP 3.0L V6 Cylinder Engine Gasoline Fuel',
        '3.6L V6 24V MPFI DOHC',
        '3.6L V6 24V GDI DOHC',
        'Other',
        '268.0HP 3.5L V6 Cylinder Engine Gasoline Fuel',
        '455.0HP 6.2L 8 Cylinder Engine Gasoline Fuel',
        '302.0HP 3.5L V6 Cylinder Engine Gasoline Fuel',
        '490.0HP 6.2L 8 Cylinder Engine Gasoline Fuel',
        '445.0HP 4.4L 8 Cylinder Engine Gasoline Fuel',
        '295.0HP 3.5L V6 Cylinder Engine Gasoline Fuel',
        '4.0L V8 32V GDI DOHC Twin Turbo',
        '3.5L V6 24V PDI DOHC Twin Turbo',
        '425.0HP 3.0L Straight 6 Cylinder Engine Gasoline Fuel'
    ]

    transmission_list = [
        'A/T', '8-Speed A/T', 'Transmission w/Dual Shift Mode', '6-Speed A/T',
        '6-Speed M/T', 'Automatic', '7-Speed A/T', '8-Speed Automatic', '10-Speed A/T',
        '5-Speed A/T', '9-Speed A/T', '6-Speed Automatic', '4-Speed A/T',
        '1-Speed A/T', 'CVT Transmission', '5-Speed M/T', '10-Speed Automatic',
        '9-Speed Automatic', 'M/T', 'Automatic CVT', 'Other'
    ]

    data_list = [int(car_ad.mileage), int(car_ad.model_year)]

    for item_list, attribute in zip([brand_list, model_list, fuel_list, engine_list, transmission_list],
                                    [car_ad.brand, car_ad.model, car_ad.fuel_type, car_ad.engine, car_ad.transmission]):
        data_list.extend([1 if item == attribute else 0 for item in item_list])

    print(data_list)
    print(len(data_list))

    pred = prediction([data_list])

    print('prediction value >> ', int(pred[0]))
    return create_response("200", "predict successfully", data={"prediction": int(pred[0])})


# ===================================

# Updated upload_to_aws with environment variables
def upload_to_aws(file, car_id):
    access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    bucket_name = os.getenv("AWS_BUCKET_NAME")

    if not access_key_id or not secret_access_key or not bucket_name:
        print("AWS credentials or bucket name not configured properly")
        return False

    s3 = boto3.client(
        "s3",
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key,
    )

    try:
        s3.upload_fileobj(file, bucket_name, f"{car_id}.jpg")
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False


# Updated save_car with proper data types and logging
@app.post("/save-car")
async def save_car(
        brand: str = Form(...),
        model: str = Form(...),
        model_year: str = Form(...),
        mileage: str = Form(...),
        fuel_type: str = Form(...),
        engine: str = Form(...),
        transmission: str = Form(...),
        car_image: UploadFile = File(...),
        db: Session = Depends(get_db),
):
    try:
        # Convert mileage to integer
        mileage = int(mileage)

        # Save input values to SQLite without specifying 'id'
        car = models.Car(
            brand=brand,
            model=model,
            model_year=model_year,
            mileage=mileage,
            fuel_type=fuel_type,
            engine=engine,
            transmission=transmission,
        )
        db.add(car)
        db.commit()

        # Handle car image upload to AWS S3
        if upload_to_aws(car_image.file, str(car.id)):
            return {"message": "Car details and image saved successfully"}
        else:
            # If image upload fails, roll back database changes and handle the error
            db.rollback()
            raise HTTPException(
                status_code=500, detail="Failed to upload image to AWS"
            )
    except Exception as e:
        # Log the error and return an error response
        print(f"Error: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        # Close the database session
        db.close()


# Function to fetch car image from AWS S3 (replace with your actual implementation)
def get_image_url_from_aws_s3(car_id: str):
    # Your implementation to fetch image URL from AWS S3
    # This could involve using the Boto3 library or any other S3 client library
    # Return the image URL
    return f"{os.getenv('AWS_Image_URL')}{car_id}.jpg"


# Updated endpoint to get all cars with images
@app.get("/get-all-cars")
async def get_all_cars(db: Session = Depends(get_db)):
    cars = db.query(models.Car).all()

    # Create a list to store car details along with image URLs
    car_details_with_images = []

    for car in cars:
        # Fetch the image URL for each car
        image_url = get_image_url_from_aws_s3(str(car.id))

        # Append car details along with image URL to the list
        car_details_with_images.append({
            "car_details": car,
            "image_url": image_url
        })

    return {"all_cars": car_details_with_images}
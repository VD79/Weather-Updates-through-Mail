from fastapi import FastAPI, Depends, HTTPException, Request, Response, Path
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import read
app = FastAPI( 
    root_path="/weather",
    title="Weather Updates",
    description="This API finds the weather updates and will send to the user through message/email",
    contact={
        "name": "Developer - Vamsi Darsi",
        "email": "vamsidarsi10@gmail.com",
    },
)


templates = Jinja2Templates(directory="C://Newfast2//.newenv2//templates")

@app.get("/weather-updates", response_class=HTMLResponse, tags=["weather-updates"], summary="Weather Updates", include_in_schema=True)
async def read_root(request: Request):
    # Render the HTML file using Jinja2Templates
    return templates.TemplateResponse("Weather.html", {"request": request})


@app.get("/weather-updates/{city_name}/email/{email}",
         tags=["weather-updates"], 
         summary="Get weather updates of a city", 
         description="This API will help in knowing the weather conditions of a city")
def get_weather(city_name: str, email:str):
    return read.weather(city_name = city_name, email=email, api_key = 'your_API_key') 
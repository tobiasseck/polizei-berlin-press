from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from sqlmodel import Session
from datetime import timedelta
import logging
from io import StringIO

from models import User, PoliceReport, create_db_and_tables, get_session
from auth import Token, authenticate_user, create_access_token, get_current_active_user, ACCESS_TOKEN_EXPIRE_MINUTES
from controller import PoliceReportController

app = FastAPI()

log_stream = StringIO()
logging.basicConfig(level=logging.INFO, stream=log_stream, format='%(asctime)s - %(levelname)s - %(message)s')

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("static/index.html", "r") as file:
        return file.read()

@app.get("/login", response_class=HTMLResponse)
async def read_login():
    with open("static/login.html", "r") as file:
        return file.read()

@app.get("/browse", response_class=HTMLResponse)
async def read_browse():
    with open("static/browse.html", "r") as file:
        return file.read()

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@app.post("/trigger-scraping")
async def trigger_scraping(current_user: User = Depends(get_current_active_user), session: Session = Depends(get_session)):
    logging.info("Triggering scraping process")
    controller = PoliceReportController(session)
    try:
        controller.run_scraper()
        log_output = log_stream.getvalue()
        return JSONResponse(content={"message": "Scraping completed", "logs": log_output}, status_code=200)
    except Exception as e:
        logging.error(f"Error during scraping: {str(e)}")
        log_output = log_stream.getvalue()
        return JSONResponse(content={"error": f"Scraping failed: {str(e)}", "logs": log_output}, status_code=500)

@app.get("/reports", response_model=list[PoliceReport])
async def get_reports(current_user: User = Depends(get_current_active_user), session: Session = Depends(get_session)):
    logging.info("Fetching all reports")
    controller = PoliceReportController(session)
    try:
        reports = controller.get_all_reports()
        return reports
    except Exception as e:
        logging.error(f"Error fetching reports: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching reports: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
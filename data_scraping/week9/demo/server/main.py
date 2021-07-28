from fastapi import FastAPI, Request, Form, File, UploadFile
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
import io
import base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/")
async def root(request: Request, message='Hello, Coursera students'):
    # return {"message": "Hello World"}
    return templates.TemplateResponse("index.html",
                        {"request": request,
                        "message": message})

@app.post("/show_plot")
async def show_plot(request: Request, numbers: str = Form(...)):
    numbers = list(map(int, numbers.split(',')))

    fig = plt.figure()
    plt.plot(numbers)

    pngImage = io.BytesIO()
    fig.savefig(pngImage)
    pngImageB64String\
        = base64.b64encode(pngImage.getvalue()).decode('ascii')
    return templates.TemplateResponse("plot.html",
                                {"request": request,
                                "numbers": numbers,
                                "picture": pngImageB64String})

@app.get("/lib")
async def get_lib(request: Request):
    books = os.listdir('static/lib')
    return templates.TemplateResponse("lib.html", 
                {"request": request,
                 "books": books})

@app.post("/upload_book")
async def upload(request: Request,
                 name: str = Form(...),
                 book_file: UploadFile = File(...)):
    file_name = '_'.join(name.split()) + '.txt'
    save_path = f'static/lib/{file_name}'
    with open(save_path, 'wb') as f:
        for line in book_file.file:
            f.write(line)
    return {"result": "success!"}

@app.get("/greet")
async def greet_name(name):
    return {"message": f"Hello {name}"}

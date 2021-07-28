from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

import io, base64
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')

def __solve(a: int, b: int, c: int):
    roots = np.roots([a, b, c])
    roots = roots[~np.iscomplex(roots)]
    roots = np.unique(roots).tolist()
    roots.sort()
    return roots

def __quadeqeval(a: int, b: int, c: int, x: np.array):
    return a*x**2 + b*x + c

def __create_func_label(a: int, b: int, c: int):
    label = str()
    if a != 0:
        label += f'{a}x^2'
    if b > 0:
        label += f'+{b}x'
    elif b < 0:
        label += f'{b}x'
    if c > 0:
        label += f'+{c}'
    elif c < 0:
        label += f'{c}'
    
    return label

@app.get('/solve')
async def solve(a, b, c):
    coeffs = tuple(map(int, (a, b, c)))
    if coeffs[0] == coeffs[1] == coeffs[2] == 0:
        return {'message': 'One of the coefficients must be non-zero'}
    roots = __solve(*coeffs)
    return {'roots': roots}

@app.get('/main')
async def home(request: Request):
    return templates.TemplateResponse('main.html',
                                    {'request': request})

@app.post('/show_plot')
async def show_plot(request: Request,
                    a_coef: int = Form(...),
                    b_coef: int = Form(...),
                    c_coef: int = Form(...)):
    if a_coef == b_coef == c_coef == 0:
        return {'message': 'One of the coefficients must be non-zero'}
    roots = __solve(*(a_coef, b_coef, c_coef))
    if a_coef != 0:
        vertex = -int(b_coef / (2 * a_coef))
    else:
        vertex = roots[0] if len(roots) != 0 else 0

    x = np.linspace(-10 + vertex, vertex + 10, 1000)
    y = __quadeqeval(a_coef, b_coef, c_coef, x)
    
    fig = plt.figure()
    plt.plot(x, y, label=f'$y={__create_func_label(a_coef, b_coef, c_coef)}$')
    if len(roots) != 0:
        plt.scatter(roots, np.zeros(len(roots)), marker='x', c='r', label='roots')
    plt.axhline(0, c='k', alpha=.5)
    plt.axvline(0, c='k', alpha=.5)
    plt.xlabel('$x$')
    plt.ylabel('$y$')
    plt.grid()
    plt.legend()
    
    pngImage = io.BytesIO()
    fig.savefig(pngImage)
    pngImageB64String = base64.b64encode(pngImage.getvalue()).decode('ascii')

    return templates.TemplateResponse('plot.html',
                                {'request': request,
                                'picture': pngImageB64String,
                                'roots': roots})
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <html>
        <head>
            <title>DevSecOps Landing Page</title>
        </head>
        <body style="font-family: Arial; text-align: center; margin-top: 50px;">
            <h1>🚀 Welcome to DevSecOps Landing Page</h1>
            <p>This simple FastAPI app will be used for SonarQube & Trivy integration demo.</p>
        </body>
    </html>
    """


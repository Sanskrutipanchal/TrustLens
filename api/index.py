from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"status": "TrustLens API is running"}

@app.get("/api")
def api_root():
    return {"status": "TrustLens API is running"}

@app.get("/api/")
def api_root_slash():
    return {"status": "TrustLens API is running"}
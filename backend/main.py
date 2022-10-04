from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Instantiate FastAPI app
app = FastAPI()

# Permit origin from React to allow for connection
origins = [
    'https://localhost:3000'
]

# Define middleware rules for app, currently all methods
# and headers are allowed for dev purposes 
# (*SHOULD BE CHANGED IN FINAL VERSION)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

# Root HTTP method
@app.get("/")
def read_root():
    return {"Rent4Hire"}

# Rental HTTP methods
@app.get("/api/rental")
async def get_rental():
    return 1

@app.get("/api/rental{id}")
async def get_rental_by_id(id):
    return 1

@app.post("/api/rental")
async def post_rental(rental):
    return 1

@app.put("/api/rental{id}")
async def put_rental(id, data):
    return 1

@app.delete("/api/rental{id}")
async def delete_rental(id):
    return 1
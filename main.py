from fastapi import FastAPI, APIRouter

app = FastAPI()
pro_router = APIRouter()

# Fixed CORS middleware configuration
# from fastapi.middleware.cors import CORSMiddleware
# app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])

# Properly structuring Veredicto class definition
class Veredicto:
    def __init__(self, score):
        self.score = score

# Changed endpoint definition to avoid duplication
@pro_router.get('/proplusplus_veredicto')
async def proplusplus_veredicto(value: int):
    score = calcular_score(value)
    return {'score': score}

# Ensure proper flow control
async def calcular_score(value):
    # Assume some calculation based on value
    return value * 2

app.include_router(pro_router)
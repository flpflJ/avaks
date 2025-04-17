import json
import PyPDF2

from g4f.client import Client

from fastapi import APIRouter, HTTPException, status, Depends
import requests
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from . import crud
from .schemas import RequestTableCreate, RequestTable, LLMReqBase, LLMRespBase, EquipItems

router = APIRouter(prefix="/router", tags=['rrouter'])


@router.get("/all", response_model=list[RequestTable])
async def get_all_req(session: AsyncSession = Depends(db_helper.session_dependency)):
    return await crud.get_all_request_table(session=session)


@router.get("/{req_id}", response_model=RequestTable)
async def get_req(req_id: int, session: AsyncSession = Depends(db_helper.session_dependency)):
    req = await crud.get_request_table(session=session, request_id=req_id)
    if req is None:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Request {req_id} not found!"
    )
    else:
        return req

def gpt(prompt: str):
    client = Client()
    chat_completion = client.chat.completions.create(
        model='gpt-4o',
        messages=[{"role": "user", "content": prompt}],
        web_search=False
    )
    return chat_completion.choices[0].message.content

@router.post("/")
async def create_req(req_in: RequestTableCreate, session: AsyncSession = Depends(db_helper.session_dependency)):

    await crud.create_request_table(request_in=req_in,session=session)
    prompt1 = ''
    with open("2.txt", 'r', encoding='utf-8') as f:
        prompt1 = f.read()
    answer = gpt(prompt1)
    print(answer)
    text = ''
    with open("1.txt", 'r', encoding='utf-8') as f:
        text = f.read()
    prompt = (f''' {answer}

     с учетом этой информации выбери подходящие устройства в необходимом количестве из вот этого текста {text} А также 
    ''')

    #print(gpt(prompt))

    prompt = prompt + '''Выведи краткую сводку, сколько это будет стоить, что за модели, смету, и рекомендации в виде JSON. Пример такого JSON { 
        "smeta":1000000, 
        "drone_model":[
          {"name":"P10", "cnt":10, "price_one":123},
          {"name":"A32-ultra", "cnt":2, "price_one":10000},
        ], 
        "additional":[
          {"name":"Расширитель ХХХ", "cnt":2, "price_one":100},
          {"name":"Расширитель бочка", "cnt":2, "price_one":100},
        ], 
        "recomendation":"Lorem, ipsum dolor sit amet consectetur adipisicing elit. Minima facere pariatur voluptate dolorem quo cumque mollitia ad, ipsam nihil excepturi at atque eaque nisi minus tempora? Distinctio voluptatem suscipit dignissimos."
      }
      Выведи только этот JSON только в таком формате, без лишних апострофов и символов и ничего больше. СТРОГО ЭТА СХЕМА!!!
    '''
    ans = gpt(prompt)
    print(ans)
    return json.loads(ans)


#@router.post("/generate", response_model=LLMRespBase)
#def generate_text(prompt: LLMReqBase):
    #response = requests.post(
    #    "http://localhost:11434/api/generate",
    #    json={
    #        "model":"etc",
    #        "prompt": prompt.prompt,
    #        "stream": False
    #    }
    #)
#    return LLMRespBase(
#        smeta=1000000,
#        drone_model=[
#            EquipItems(name="P10", cnt=10, price_one=123),
#            EquipItems(name="A32-ultra", cnt=2, price_one=10000)
#        ],
#        additional=[
#            EquipItems(name="Расширитель ХХХ", cnt=2, price_one=100),
#            EquipItems(name="Расширитель бочка", cnt=2, price_one=100)
#        ],
#        recommendation=prompt.prompt
#    )
import json

from g4f.client import Client

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from . import crud
from .schemas import RequestTableCreate, RequestTable, LLMReqBase, LLMRespBase, EquipItems
from .utils import split_text, createDocxSAU, create_survey_document, parse_raw_data

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
    #print(req_in.dron_location)
    prompt1 = f'''Ты выступаешь как технический специалист АВАКС. Цель — подготовить ответ для технического запроса клиента, который планирует использовать дрон в сложных климатических условиях. Используй профессиональный язык, но избегай избыточных формальностей. Подбирай самое оптимальное решение из всех имеющихся.

    Даны ответы на вопросы:
    - Для каких задач вам нужен дрон? {req_in.dron_usage}
    - Планируемые локации использования дрона? {req_in.dron_location}
    - Вас интересует работа в реальном времени или вас интересует запись какой-то информации? {req_in.dron_realtime}
    - Какие характеристики для вас важны: время полёта, дальность, грузоподъёмность, тип камеры? {req_in.dron_asset}'''
    with open("2.txt", 'r', encoding='utf-8') as f:
        prompt1 += f.read()
    answer = gpt(prompt1)
    #print(answer)
    with open(f"docs/data_analysis_{req_in.email}.txt", 'w', encoding='utf-8') as f:
        f.write(answer)
    p1,p2= split_text(answer)
    print(p1,p2)
    try:
        createDocxSAU(p1,req_in.email)
        create_survey_document(parse_raw_data(p2),req_in.email)
    except:
        pass
    #print(answer)
    text = ''
    with open("1.txt", 'r', encoding='utf-8') as f:
        text = f.read()
    prompt = (f''' {answer}

     с учетом этой информации выбери подходящие устройства в необходимом количестве из вот этого текста {text}. Можешь также попробовать поискать коммерческие модели и предложить их. А также 
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
    #print(ans)
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
from fastapi import FastAPI, Query, Body
import uvicorn

app = FastAPI()

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]


@app.get('/hotels')
def get_hotels(
        title: str | None = Query(default=None, description='Название отеля'),
        id: int | None = Query(default=None, description='id отеля'),
        page: int | None = Query(default=1, description='Номер страницы'),
        per_page: int | None = Query(default=2, description='Количество отелей на странице')
):
    hotels_ = []
    for hotel in hotels[(page - 1) * per_page:(page - 1) * per_page + per_page]:
        if id and hotel['id'] != id:
            continue
        if title and hotel['title'] != title:
            continue
        hotels_.append(hotel)
    return hotels_


@app.delete('/hotels/{hotel_id}')
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != hotel_id]
    return {'status': 'OK'}


@app.post('/hotels')
def create_hotel(
        title: str = Body(),
        name: str = Body()
):
    global hotels
    hotels.append({
        'id': hotels[-1]['id'] + 1,
        'title': title,
        'name': name
    })
    return {'status': 'ok'}


@app.put(
    '/hotels/{hotel_id}',
    summary='Обновление данных об отеле')
def put_hotel(
        hotel_id: int,
        title: str = Body(),
        name: str = Body()
):
    for hotel in hotels:
        if hotel['id'] == hotel_id:
            hotel['title'] = title
            hotel['name'] = name
            return {'status': 'OK'}
    return {'status': 'Not found'}


@app.patch('/hotels')
def patch_hotel(
        id: int = Body(),
        title: str = Body(None),
        name: str = Body(None)
):
    for hotel in hotels:
        if id and hotel['id'] == id:
            if title:
                hotel['title'] = title
            if name is not None:
                hotel['name'] = name
            return 'OK'
    return {'status': 'Not found'}


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)

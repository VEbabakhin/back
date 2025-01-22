from fastapi import FastAPI, Query, Body
import uvicorn

app = FastAPI()

hotels = [
    {'id': 1, 'title': 'sochi', 'name': 'Сочи'},
    {'id': 2, 'title': 'dubai', 'name': 'Дубай'}
]


@app.get('/')
def f():
    return 'Hello!!!'


@app.get('/hotels')
def get_hotels(
        title: str | None = Query(default=None, description='Название отеля'),
        id: int | None = Query(default=None, description='id отеля')):
    hotels_ = []
    for hotel in hotels:
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


@app.put('/hotels')
def put_hotel(
        id: int = Body(),
        title: str = Body(),
        name: str = Body()
):
    for hotel in hotels:
        if hotel['id'] == id:
            hotel['title'] = title
            hotel['name'] = name
            return 'OK'
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

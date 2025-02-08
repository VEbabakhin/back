from fastapi import  Query, APIRouter
from src.api.dependencies import PaginationDep
from src.schemas.hotels import HotelPATCH, Hotel


router = APIRouter(prefix='/hotels')
hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]


@router.get('')
def get_hotels(
        pagination: PaginationDep,
        title: str | None = Query(default=None, description='Название отеля'),
        id: int | None = Query(default=None, description='id отеля')

):
    hotels_ = []
    for hotel in hotels:
        if id and hotel['id'] != id:
            continue
        if title and hotel['title'] != title:
            continue
        hotels_.append(hotel)
    if pagination.page and pagination.per_page:
        return hotels_[(pagination.page - 1) * pagination.per_page:][:pagination.per_page]
    return hotels_


@router.delete('/{hotel_id}')
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != hotel_id]
    return {'status': 'OK'}


@router.post('')
def create_hotel(hotel_data: Hotel):
    global hotels
    hotels.append({
        'id': hotels[-1]['id'] + 1,
        'title': hotel_data.title,
        'name': hotel_data.name
    })
    return {'status': 'ok'}


@router.put(
    '/{hotel_id}',
    summary='Обновление данных об отеле')
def put_hotel(hotel_id: int, hotel_data: Hotel):
    for hotel in hotels:
        if hotel['id'] == hotel_id:
            hotel['title'] = hotel_data.title
            hotel['name'] = hotel_data.name
            return {'status': 'OK'}
    return {'status': 'Not found'}


@router.patch('/{hotel_id}')
def patch_hotel(
        hotel_id: int,
        hotel_data: HotelPATCH
):
    for hotel in hotels:
        if hotel['id'] == hotel_id:
            if hotel_data.title:
                hotel['title'] = hotel_data.title
            if hotel_data.name is not None:
                hotel['name'] = hotel_data.name
            return 'OK'
    return {'status': 'Not found'}
import grpc
import analytics_pb2
import analytics_pb2_grpc

#Функция запуска клиента
def run():
    #Канал для подключения к серверу
    channel = grpc.insecure_channel('localhost:50051')
    #Заглушка для взаимодействием с сервисом аналитики
    stub = analytics_pb2_grpc.AnalyticsStub(channel)
    #Создание объекта с начальной и конечной датами периода
    date_range = analytics_pb2.DateRange(
        start_date="2023-10-01",
        end_date="2023-10-31"
    )
    #Вывод информации о запросеп и периоде
    print("Запрос событий за период:", date_range.start_date, "-", date_range.end_date)
    #Вызов метода StreamEvents и получение потока событий
    responses = stub.StreamEvents(date_range)
    #Выводим детали каждого события из полученного потока
    for response in responses:
        print("Event Type:", response.event_type)
        print("Timestamp:", response.timestamp)
        print("User ID:", response.user_id)
        print("Details:", response.details)
        print("---------------------------")

run()

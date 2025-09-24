from concurrent import futures
import grpc
import time
import analytics_pb2
import analytics_pb2_grpc


#Класс для реализации сервиса Аналитики
class AnalyticsServicer(analytics_pb2_grpc.AnalyticsServicer):


    #Получение потока событий за определенный период
    #request - объект с начальной и конечной датой 
    #context - контекст grpc запроса
    def StreamEvents(self, request, context):
        start_date = request.start_date
        end_date = request.end_date

        # Пример списка событий
        events = self.get_events_in_range(start_date, end_date)

        for event in events:
            yield event


    #Получение списка событий за заданный период
    def get_events_in_range(self, start_date, end_date):
        events = [
        analytics_pb2.Event(
            event_type="click",
            timestamp="2023-10-01T12:34:56Z",
            user_id="user123",
            details="Clicked on product page"
        ),
        analytics_pb2.Event(
            event_type="view",
            timestamp="2023-10-01T13:45:00Z",
            user_id="user456",
            details="Viewed product details"
        ),
        analytics_pb2.Event(
            event_type="click",
            timestamp="2023-10-02T09:15:30Z",
            user_id="user789",
            details="Clicked on homepage banner"
        ),
        analytics_pb2.Event(
            event_type="view",
            timestamp="2023-10-02T10:45:00Z",
            user_id="user101",
            details="Viewed blog post"
        )
        ]
        #Возвращает список событий
        return events
    

#Создание grpc-сервиса с потоком данных и запуск
def serve():
    # Создаем gRPC-сервер с пулом потоков
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    # Добавляем сервис AnalyticsServicer к серверу
    analytics_pb2_grpc.add_AnalyticsServicer_to_server(AnalyticsServicer(), server)
    
    # Добавляем порт для прослушивания
    server.add_insecure_port('[::]:50051')
    
    # Запускаем сервер
    server.start()
    print("Server started, listening on port 50051")
    
    # Поддерживаем работу сервера до прерывания
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        print("Stopping server...")
        server.stop(0)  # Останавливаем сервер при нажатии Ctrl+C
        print("Server stopped.")
serve()

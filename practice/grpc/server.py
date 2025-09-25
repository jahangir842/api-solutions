import grpc
from concurrent import futures
import todo_pb2
import todo_pb2_grpc

# In-memory DB
todos = []
counter = 1

class TodoService(todo_pb2_grpc.TodoServiceServicer):
    def CreateTodo(self, request, context):
        global counter
        todo = todo_pb2.TodoResponse(
            id=counter,
            title=request.title,
            completed=request.completed
        )
        todos.append(todo)
        counter += 1
        return todo

    def GetTodos(self, request, context):
        return todo_pb2.TodoList(todos=todos)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    todo_pb2_grpc.add_TodoServiceServicer_to_server(TodoService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("🚀 gRPC server running on port 50051")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()

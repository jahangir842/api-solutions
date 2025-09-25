import grpc
import todo_pb2
import todo_pb2_grpc

def run():
    channel = grpc.insecure_channel("localhost:50051")
    stub = todo_pb2_grpc.TodoServiceStub(channel)

    # Create a Todo
    todo = stub.CreateTodo(todo_pb2.TodoRequest(title="Learn gRPC", completed=False))
    print("Created:", todo)

    # Get all Todos
    todos = stub.GetTodos(todo_pb2.Empty())
    print("All Todos:", todos)

if __name__ == "__main__":
    run()

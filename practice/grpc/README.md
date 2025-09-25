# 🔹 What is gRPC?

* **gRPC (Google Remote Procedure Call)** is a **binary, high-performance communication protocol** built on **HTTP/2**.
* Instead of REST’s `GET/POST/PUT/DELETE`, you define **services** and **methods** in a `.proto` file.
* It uses **Protocol Buffers (protobuf)** for serialization (smaller & faster than JSON).

---

# 🔹 Lab Setup for gRPC

### **1. Install Requirements**

```bash
python3 -m venv grpc-lab
source grpc-lab/bin/activate

pip install grpcio grpcio-tools
```

---

### **2. Define a `.proto` File**

Create `todo.proto`:

```proto
syntax = "proto3";

package todo;

// The Todo service definition.
service TodoService {
  rpc CreateTodo (TodoRequest) returns (TodoResponse);
  rpc GetTodos (Empty) returns (TodoList);
}

// Request message
message TodoRequest {
  string title = 1;
  bool completed = 2;
}

// Response for CreateTodo
message TodoResponse {
  int32 id = 1;
  string title = 2;
  bool completed = 3;
}

// Empty request for GetTodos
message Empty {}

// List of todos
message TodoList {
  repeated TodoResponse todos = 1;
}
```

---

### **3. Generate Python Code from `.proto`**

Run:

```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. todo.proto
```

This creates:

* `todo_pb2.py` → message classes
* `todo_pb2_grpc.py` → service base class + stubs

---

### **4. Implement the gRPC Server**

Create `server.py`:

```python
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
```

---

### **5. Implement the gRPC Client**

Create `client.py`:

```python
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
```

---

### **6. Run the Lab**

1. Start the server:

   ```bash
   python server.py
   ```
2. In another terminal, run client:

   ```bash
   python client.py
   ```

✅ You’ll see output like:

```
Created: id: 1 title: "Learn gRPC" completed: false
All Todos: todos {
  id: 1
  title: "Learn gRPC"
  completed: false
}
```

---

# 🔹 Next Steps for gRPC Lab

1. Add **UpdateTodo** and **DeleteTodo** methods.
2. Enable **TLS** (secure gRPC).
3. Deploy gRPC in **Docker / Kubernetes**.
4. Try **gRPC Gateway** → REST ↔ gRPC bridge.

---

**Next:** extend this lab into **full CRUD with Update/Delete** right away, or should we first practice this basic **Create/Get** version?

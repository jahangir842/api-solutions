from fastapi import FastAPI, HTTPException

app = FastAPI()

# In-memory "database"
todos = []
todo_id_counter = 1


# Create a Todo (POST)
@app.post("/todos")
def create_todo(todo: dict):
    global todo_id_counter
    new_todo = {
        "id": todo_id_counter,
        "title": todo.get("title"),
        "completed": todo.get("completed", False)
    }
    todos.append(new_todo)
    todo_id_counter += 1
    return new_todo


# Read All Todos (GET)
@app.get("/todos")
def get_todos():
    return todos


# Read Single Todo (GET)
@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):
    for todo in todos:
        if todo["id"] == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")


# Update Todo (PUT)
@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, updated_todo: dict):
    for todo in todos:
        if todo["id"] == todo_id:
            todo["title"] = updated_todo.get("title", todo["title"])
            todo["completed"] = updated_todo.get("completed", todo["completed"])
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")


# Delete Todo (DELETE)
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    for i, todo in enumerate(todos):
        if todo["id"] == todo_id:
            deleted = todos.pop(i)
            return {"message": "Todo deleted", "todo": deleted}
    raise HTTPException(status_code=404, detail="Todo not found")

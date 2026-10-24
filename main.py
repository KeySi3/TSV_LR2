from fastapi import FastAPI, HTTPException, status
import os
from utils import json_to_dict_list, dict_list_to_json
from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional

# Определение путей к директориям и локальному файлу базы данных
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
STORAGE_FILE = os.path.join(DATA_DIR, "tasks.json")


class TaskCreate(BaseModel):
    """
    Pydantic-модель для валидации данных при создании новой задачи.

    :param owner_id: Идентификатор владельца задачи
    :param task_name: Наименование задачи
    """
    model_config = ConfigDict(extra="forbid")
    owner_id: int = Field(gt=0)
    task_name: str = Field(min_length=1, max_length=120)


class TaskRead(BaseModel):
    """
    Pydantic-модель для валидации возвращаемых данных о задаче.

    :param task_id: Уникальный идентификатор задачи
    :param owner_id: Идентификатор владельца задачи
    :param task_name: Наименование задачи
    """
    model_config = ConfigDict(from_attributes=True)
    task_id: int = Field(gt=0)
    owner_id: int = Field(gt=0)
    task_name: str = Field(min_length=1, max_length=120)


# Инициализация экземпляра приложения FastAPI
app = FastAPI(
    title="Task management"
)


@app.get("/tasks", response_model=List[TaskRead])
def get_all_tasks(owner_id: Optional[int] = None):
    """
    Возвращает список всех сохранённых задач с возможностью фильтрации по владельцу.

    :param owner_id: Необязательный идентификатор владельца для фильтрации
    :return: Список объектов задач TaskRead
    """
    tasks = json_to_dict_list(STORAGE_FILE)
    if tasks is None:
        tasks = []
    if owner_id:
        if owner_id <= 0:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Некорректные данные: ID задачи должен быть положительным числом"
            )
        return [task for task in tasks if task.get("owner_id") == owner_id]
    return tasks


@app.get("/tasks/{task_id}", response_model=TaskRead)
def get_task_by_id(task_id: int):
    """
    Осуществляет поиск и возврат конкретной задачи по её идентификатору.

    :param task_id: Идентификатор искомой задачи
    :return: Объект найденной задачи TaskRead
    """
    tasks = json_to_dict_list(STORAGE_FILE)
    if tasks is None:
        tasks = []
    for task in tasks:
        if task.get("task_id") == task_id:
            return task
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Задача с ID {task_id} не найдена"
    )


@app.post("/tasks", response_model=TaskRead)
def post_task(data: TaskCreate):
    """
    Создаёт новую задачу, присваивает уникальный идентификатор и сохраняет её в файл.

    :param data: Входные валидированные данные задачи (TaskCreate)
    :return: Созданная задача с назначенным task_id
    """
    tasks = json_to_dict_list(STORAGE_FILE)
    if tasks is None:
        tasks = []
    new_id = max([task["task_id"] for task in tasks], default=0) + 1
    new_task = {
        "task_id": new_id,
        **data.model_dump()
    }
    tasks.append(new_task)
    if not dict_list_to_json(tasks, STORAGE_FILE):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при сохранении задачи"
        )
    return new_task


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    """
    Удаляет задачу из локального хранилища по её идентификатору.

    :param task_id: Идентификатор задачи, которую требуется удалить
    :return: None при успешном удалении
    """
    tasks = json_to_dict_list(STORAGE_FILE)
    if tasks is None:
        tasks = []
    index = None
    count = -1
    for task in tasks:
        count += 1
        if task.get("task_id") == task_id:
            index = count
            break
    if not index:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Задача с ID {task_id} не найдена"
        )
    tasks.pop(index)
    if not dict_list_to_json(tasks, STORAGE_FILE):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при обновлении файла"
        )
    return None

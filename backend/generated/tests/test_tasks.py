import pytest
from generated.code.services.task_service import create_task, list_tasks

def test_create_task_success():
    task = create_task('Write test')
    assert task.title == 'Write test'
    assert task.completed is False

def test_create_task_empty_title():
    with pytest.raises(ValueError, match='Title is required'):
        create_task('')

def test_create_task_long_title():
    with pytest.raises(ValueError, match='Title cannot exceed 100 characters'):
        create_task('A' * 101)

def test_list_tasks():
    tasks = list_tasks()
    assert isinstance(tasks, list)
    assert len(tasks) == 0

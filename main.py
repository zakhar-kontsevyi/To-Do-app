
from pydantic import BaseModel , Field
from typing import Annotated
from sqlalchemy.ext.asyncio import create_async_engine , async_sessionmaker , AsyncSession
from sqlalchemy.orm import DeclarativeBase , Mapped , mapped_column 
from fastapi import FastAPI , Depends, HTTPException , status
from sqlalchemy import select


app = FastAPI()

engine = create_async_engine('sqlite+aiosqlite:///tasks.db')
new_session = async_sessionmaker(engine , expire_on_commit=False)

async def get_session():
    async with new_session() as session:
        yield session

SessionDep = Annotated[AsyncSession , Depends(get_session)]

class Base(DeclarativeBase):
    pass

class TaskModel(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    completed: Mapped[bool]





class TaskAddSchema(BaseModel):
    title: str = Field(max_length=50)
    description: str | None = Field(max_length=1000)
    completed: bool 

class TaskSchema(TaskAddSchema):
    id:int


'''
@app.post("/setup_database")
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return {"success": True}
'''



@app.post("/tasks" , tags = ["Tasks"] , summary = "Create task")
async def create_task(data:TaskAddSchema , session:SessionDep):
    new_task = TaskModel(
        title = data.title,
        description = data.description,
        completed = data.completed
    )

    session.add(new_task)
    await session.commit()

    return {
        "success" : True ,
        "message":"Task creation successful"
    }



@app.get("/tasks", tags = ["Tasks"] , summary= "Geting all tasks")
async def get_tasks(session: SessionDep):
    query = select(TaskModel)
    result = await session.execute(query)
    return result.scalars().all()

    


@app.get("/tasks/{task_id}", tags = ["Tasks"] , summary = "Geting tasks by id")
async def get_tasks(task_id : int, session: SessionDep ):

    query = select(TaskModel).where(TaskModel.id == task_id)

    data = await session.execute(query)
    task_db = data.scalar_one_or_none()

    if task_db is None:
        raise HTTPException(
            status_code=404,
            detail="No tasks by this title"
        )
    
    return task_db

    


@app.put("/tasks/{task_id}",tags=["Tasks"],summary="Editing tasks by title")
async def put_tasks_by_title(task_id: int, task: TaskAddSchema, session: SessionDep ):

    query = select(TaskModel).where(TaskModel.id == task_id)

    data = await session.execute(query)
    task_db = data.scalar_one_or_none()

    if task_db is None:
        raise HTTPException(
            status_code=404,
            detail="No task by this title"
        )
    
    task_db.title = task.title
    task_db.description = task.description
    task_db.completed = task.completed

    await session.commit()

    return {
        "success": True,
        "message": "Task editing successful"
    }



@app.delete("/tasks/{task_id}", tags = ["Tasks"] , summary= "Delete tasks by id",status_code=status.HTTP_204_NO_CONTENT)
async def delete_tasks_by_ID(task_id: int , session: SessionDep):

    query = select(TaskModel).where(TaskModel.id == task_id)

    data = await session.execute(query)
    task_db = data.scalar_one_or_none()

    if task_db is None:
        raise HTTPException(
            status_code=404,
            detail="No task by this title"
        )
    
    await session.delete(task_db)
    await session.commit()

    return {"success" : True,"message": "Task deleted"}

    
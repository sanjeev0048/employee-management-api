from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, crud
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Employee Management API")


# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 🟢 GET all employees
@app.get("/employees", response_model=list[schemas.Employee])
def read_employees(db: Session = Depends(get_db)):
    return crud.get_employees(db)


# 🟡 GET one employee by ID
@app.get("/employees/{emp_id}", response_model=schemas.Employee)
def read_employee(emp_id: int, db: Session = Depends(get_db)):
    emp = crud.get_employee_by_id(db, emp_id)
    if emp is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp


# 🟢 POST create new employee
@app.post("/employees", response_model=schemas.Employee)
def add_employee(emp: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    return crud.create_employee(db, emp)


# 🟠 PUT update existing employee
@app.put("/employees/{emp_id}", response_model=schemas.Employee)
def update_employee(emp_id: int, emp_data: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    updated_emp = crud.update_employee(db, emp_id, emp_data)
    if updated_emp is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return updated_emp


# 🔴 DELETE employee
@app.delete("/employees/{emp_id}")
def delete_employee(emp_id: int, db: Session = Depends(get_db)):
    deleted_emp = crud.delete_employee(db, emp_id)
    if deleted_emp is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"message": f"Employee ID {emp_id} deleted successfully."}

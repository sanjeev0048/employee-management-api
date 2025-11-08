from sqlalchemy.orm import Session
import models, schemas


# 🟢 Read all employees
def get_employees(db: Session):
    return db.query(models.Employee).all()


# 🟢 Read single employee by ID
def get_employee_by_id(db: Session, emp_id: int):
    return db.query(models.Employee).filter(models.Employee.id == emp_id).first()


# 🟡 Create a new employee
def create_employee(db: Session, emp: schemas.EmployeeCreate):
    new_emp = models.Employee(**emp.dict())
    db.add(new_emp)
    db.commit()
    db.refresh(new_emp)
    return new_emp


# 🟠 Update an employee by ID
def update_employee(db: Session, emp_id: int, emp_data: schemas.EmployeeCreate):
    emp = db.query(models.Employee).filter(models.Employee.id == emp_id).first()
    if emp is None:
        return None
    emp.name = emp_data.name
    emp.role = emp_data.role
    emp.email = emp_data.email
    db.commit()
    db.refresh(emp)
    return emp


# 🔴 Delete an employee by ID
def delete_employee(db: Session, emp_id: int):
    emp = db.query(models.Employee).filter(models.Employee.id == emp_id).first()
    if emp is None:
        return None
    db.delete(emp)
    db.commit()
    return emp

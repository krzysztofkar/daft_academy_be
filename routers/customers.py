import sqlite3

from fastapi import APIRouter, HTTPException
from models.customers import Customer

router = APIRouter()


@router.on_event("startup")
async def startup():
    router.db_connection = sqlite3.connect("chinook.db")
    router.db_connection.row_factory = sqlite3.Row


@router.on_event("shutdown")
async def shutdown():
    router.db_connection.close()


@router.put("/customers/{customer_id}")
async def customers(customer_id, customer: Customer = {}):
    cursor = router.db_connection.cursor()
    selected_customer = cursor.execute(
        "SELECT * FROM customers WHERE customerid = ?", (customer_id,),
    ).fetchone()

    if not selected_customer:
        raise HTTPException(status_code=404, detail={"error": "Not Found"})

    column_names = [value[0] for value in customer if value[1] is not None]
    values = [value[1] for value in customer if value[1] is not None]

    columns = " = ?,".join(column_names) + "= ?"
    cursor.execute(
        f"UPDATE customers SET {columns} WHERE customerid = ?", (*values, customer_id,),
    )
    router.db_connection.commit()
    return selected_customer


@router.get("/sales")
async def sales(category: str):
    if category != "customers":
        raise HTTPException(status_code=404, detail={"error": "Not Found"})

    cursor = router.db_connection.cursor()
    sales = cursor.execute(
        """
        SELECT customerid, email, phone, ROUND(SUM(total),2) AS Sum FROM
        invoices JOIN customers USING(customerid) GROUP BY customerid
        ORDER BY Sum DESC, customerid
        """
    ).fetchall()

    return sales

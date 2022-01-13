import os
from typing import Optional
from fastapi import FastAPI
import sqlite3


########################################################################
#
# function: runQuery(sql,ctx)
# function to extract the data from the raw message class to a dict
#
########################################################################
def runQuery(sql,ctx):
    c = ctx.cursor()
    c.execute(sql)
    return c.fetchall()


########################################################################
#
# function: commitQuery(sql,ctx)
# function to extract the data from the raw message class to a dict
#
########################################################################
def commitQuery(sql,ctx):
    c = ctx.cursor()
    c.execute(sql)
    ctx.commit()
    return c.fetchall()

########################################################################
#
# function: getTable(table,limit,ctx)
# function to extract the data from the raw message class to a dict
#
########################################################################
def getTable(table: str,limit: Optional[int], columns: Optional[str]):
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    limit_str = ''
    column_str = '*'
    if limit:
        limit_str = f'limit {limit}'
    if columns:
        column_str = f'{columns}'
    sql = f'''select {column_str} 
    from {table}
    {limit_str}
    '''
    data = ''
    try:
        data = runQuery(sql,conn)
    except Exception as e:
        data = str(e)
    return data


# get database path
DATABASE_PATH = '../discord-channel-streaming-bot/dev/sql.db'

# connect to database

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/{table}")
def read_item(table: str, limit: Optional[str] = None, columns: Optional[str] = None, auth: Optional[str] = None):
    if auth:
        if auth == os.env.get('APISERVER_AUTH'):
            return getTable(table, limit, columns)
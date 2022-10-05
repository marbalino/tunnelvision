import sqlite3
import time
import asyncio 
from kasa import SmartPlug

async def plugoff():
    p=SmartPlug("192.168.2.5")
    await p.update()
    await p.turn_off() 

async def plugon():
    p=SmartPlug("192.168.2.5")
    await p.update()
    await p.turn_on()
def trigger_time(i):
    
    try:
        conn = sqlite3.connect('test7.db')
        cur=conn.cursor()
        print ("great success opening database1 in trigger_manager for id ", i)        
    except Exception as e:
        print("Error during connection: ",str(e))    

    try:
    	sql_update_query= ("""Update Todo set state = 0 where id = ?""")
    	cur.execute (sql_update_query,[i])
    	conn.commit()
    except Exception as e:
    	print("error when updataing rule id ", i, "to state 0")    
       
    sql_search_query= ("""SELECT * FROM Todo WHERE id = ?""")
    cur.execute(sql_search_query,[i])
    x=cur.fetchone()
    print("should be state 0", x)
    conn.close()    
    asyncio.run(plugon())                      
    print('about to sleep', (x[1]))
    
    time.sleep(x[1]) 
    asyncio.run(plugoff())   
    try:
        conn = sqlite3.connect('test7.db')
        cur=conn.cursor()
        print ("great success open database in trigger_manager to change state back to 1 for id ", i)      
    except Exception as e:
        print("Error during connection: ",str(e))
    
    try:
    	sql_update_query2= ("""Update Todo set state = 1 where id = ?""") 
    	cur.execute(sql_update_query2,[i]) 
    	conn.commit()
    	print ("great success chaning state back to 1 for id ", i)
        
    except Exception as e:
        print("Error chaning state back to 1 for id ", i)

    cur.execute(sql_search_query,[i])
    print(cur.fetchone())
    conn.close()

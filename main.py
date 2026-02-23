from fastapi import FastAPI, Path, Query    # fastapi aik webframework hai or uski class FastAPI hai
# import the student model along with existing ones

from model import Home, Food, Students           # model aik file hai or Home usma class hai
from db import getDbConnection
import re
from psycopg2.extras import RealDictCursor


app = FastAPI()

@app.post("/This is an Endpint")     
def func(user : Home):          # def func aik function hai or user aik variable hai or home class
    return user


@app.put("/users/{variable}")   # @app.get ma hum user ko data show karwa raha hain
# /users/ usko variable k path pa connect kr deta haii 

async def getUser(variable: int):   # humne async function concurency hasil krna k liya kiya hai use hum
    # def function bhi kr sakhta tha but wo sychronous hai single 
    return {"user_id": variable}    # humne response generate krna k liya k user_id ma wo integar k data aye jo user enter kara


@app.get("/users")     # yahan par hum @app.get k agha hum endpoint bata raha hain
async def users(limit : int = 10, active : bool = True):    # async def users aik function hai jo asyncronus hai 
# or uski default humne limit 10 rakhdi haii 
# or uska status True hai     
    return{"limit" : limit , "active" : active}   # yahan hum response return kr raha hain JSON format main


school = {                     # humne aik variable banaya hai 
    1 : {                        # jiski humne key (ID) 1 rakhdi hai
        "name" : "Abdullah",     # name bhi aik key variable(attribute hai uska)
        "age" : 22,              # ye JOSN format ma likha hai 
        "class" : "14th years"
    },

    2 : {
        "name" : "Hadi",         # its like a Mini Database
        "age" : 23,
        "class" : "14th years"
    }  
}

# PATH PARAMETER

@app.get ("/get-student/{student_id}")   # @app.get main hum data read karwa raha hain 
# /get-student humne endpoint rakh diya hai
# {student_id} humne aik URL or path parameter rakh diya hai jo 1 enter karna pa humain students 1 k data show karwayega
async def getStudent(student_id : int): # async function banaya hai concurrency hasil krna k liya student_id humne int define kar diya hai 
    return school[student_id]  # humne students return karwa diya hai [agar hum tuple main student_id]
                                 # pass na karwata to ye sab numbers pa data show karwa deta
                                 # tuple use krna ki main reason hi yehi h k wo students sa ja k data get kara 
# gt = greater than , lt = less than , ge = greater than equal too, le = less than equal too


animal = {
    10 : {
        "Carnivorrse" : "Lion",
        "Omnivorse" : "Goat",
        "Mix" : "Both"
    }
}

@app.get("/animal/{animal_info}")
async def info(
    animalInfo : int = Path(..., description = "Enter Animal ID", gt = 0) ):     # # ... is Ellipsis it is build-in-constant means to be continued
    return animal[animalInfo]


@app.get("/This is Food Endpoint")
async def getFood(update : Food):
    return update

students = {                          # yahan pa humne student ki aik dictionary banai hai 
    101 : "Hamid",                    # yahan pa humne key or uska str pass kr diya hai
    102 : "Ali"
}

@app.put("/students/{studentID}")             # @app.put aik update/change krna h decorator hai or agha uska path parameter bata diya hai
async def updateStudent(                      # async aik function hai 
    studentID : int = Path(..., description = "The new name of the Sudent" , gt = 0),      # yahan pa hai variable hai studentId jo int hai or ... aik ellipsis hai this means this can't be skipped
    newName : str = "Abdullah"                # newName aik or variable hai jiski default string Abdullah hai 
# path yahan pa aik validation or metadata k tor pa use ho raha hai jo ye validate kr raha  hai k isko user skip nai kr sakhtaa
# ye query parameter k tor pa use ho raha hai jo ye ye batainga k agar newName nai lagata to default name Abdullah hai
):
    if studentID in students:                 # agar studentID students k ander mojood hai so print ye aik check hai
        students[studentID] = newName         # yahann pa hi humain dictionary k faida hoga jo humne uper lagai hai bcz dictionary is mutable 
        # so it updates with newName

        return{"message" : "Success" , "IDUpdated" : studentID , "newName" : students[studentID]}
    return{"Error" : "Student not found"} 


@app.delete("/delete_students/{studentID}")        # yahan humne delete k method banaya hai or studentID uska parameter hai
def deleteStudent(studentID : int):                # deleteStudent aik function hai jisme hum bata raha studentID ki datatype int hai
    if studentID not in students:                  # agar studentID main students k koi attribute nai mojood hai 
        return{"Error" : "User doesn't exist"}     # to error generate krde user doesn't exist

    del students[studentID]                        # del krdo jo bhi tmhain studentID mila students main sa
    return {"Messege" : "student deleted successful"}    # del kr msg generate krdo 


@app.post("/clean_data/{cleanData}")
async def reGex(cleanData : str):
    
    # develop the pattern
    pattern = r"[^a-zA-Z0-9]"  # ^ ye ye bata raha hai k inka ilawa baki sab remove krdo
    # clean the data

    cleanedData = re.sub(pattern, "",cleanData)    # re.sub clean and special charactors remove krna main help krta hai
    # "" this represents empty strings
    cleanedData = cleanedData.strip()        # .strip is used to remove space in the strings bcz in database it's an error         
    # return the data
    return {
        "Orginal" : cleanData,
        "CleanedData" : cleanedData,
        "Messege" : "Data is Cleaned now"
    }
   

@app.get("/get-all-students")
def getAllStudents():
    connection = getDbConnection()

    cursor = connection.cursor(cursor_factory = RealDictCursor)

    cursor.execute("select * from student;")
    rows= cursor.fetchall()

    cursor.close()
    connection.close()

    return {"data" : rows}


# get student with ID / {ID}
@app.post("/get-students-with-id/{student_id}")
def studentID(student_id : int):
    connection = getDbConnection()
    cursor = connection.cursor(cursor_factory = RealDictCursor)

    query = "select * from student where id  = %s;"
    cursor.execute(query,(student_id,))
    
    row = cursor.fetchone()
    cursor.close()
    connection.close()

    if row is None:
        return{"message" : "Student not found"}
    return{"data" : row}



# create an API, POST request, no query parameter no request parameter
@app.post("/create-user")

# method will have student: Student (which you have imported above from model)

def createUser(student : Students):
    student.id = 500
    student.name = "nouman"
    student.address = "Johar town"
    student.marks = 50

    connection = getDbConnection()
    cursor = connection.cursor(cursor_factory = RealDictCursor)

    query = """
        INSERT INTO student (id, name, address, marks) 
        VALUES (%s, %s, %s, %s)
        RETURNING *;
    """
    cursor.execute(query,(student.id,student.name,student.address,student.marks,))
    connection.commit()

    cursor.close()
    connection.close()

    return {"student" : "created successfully"} 





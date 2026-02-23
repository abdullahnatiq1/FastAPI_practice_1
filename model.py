from pydantic import BaseModel    # pydantic aik data validation hai or BaseModel uski class

class Home(BaseModel):            # humne home ki aik class banai hai jisko inherit BaseModel sa karwaya hai 
    fridge : int = 2              # fridge aik attribute hai class k jis ki datatype int hai
    oven : int = 1                
    AC : int = 3 


class Food(BaseModel):
    Biryani : int = 2
    pulao : int = 20
    pizza : int = 5

# create class for student with its attributes according to the DB

class Students(BaseModel):
    id : int = 101
    name : str = "Abdullah"
    address : str = "Johar Town"
    marks : int = 100

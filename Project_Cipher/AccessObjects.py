class Objects:
    def __init__(self, name:str,length:int):
        self.length=length
        self.name=name
        self.Id=self.gen_Id()

    def __str__(self):
        return f'Id: {self.Id} Name: {self.name}'

    def rename(self, new_name:str):#renames the Object
        self.name=new_name

    def gen_Id(self)-> str:
        from random import randint
        Id=''
        for i in range(self.length):
            digit=randint(0,9)
            Id+=str(digit)
        return Id

class user(Objects):
    def __init__(self, name:str, username:str, password:str, clearance:str,Id_length:int):
        super().__init__(name,Id_length)
        self.username=username
        self.clearance=clearance
        self.password=password

    def __str__(self):
        return super().__str__()+f' username: {self.username} clearance: {self.clearance}'

    def change_user(self,new_user):
        self.username=new_user

    def pass_hash(self):
        from hashlib import sha256
        hashed_pass=sha256(self.password.encode())
        self.password=hashed_pass.hexdigest()
    def check_pass(self,pwd)-> bool:
        from hashlib import sha256
        hashed_pass = sha256(pwd.encode())
        if hashed_pass.hexdigest()==self.password:
            return True
        else:
            return False
    def change_pass(self,newpass):
        from hashlib import sha256
        hashed_pass = sha256(newpass.encode())
        self.password = hashed_pass.hexdigest()

    def change_clear(self,clearance):
        self.clearance=clearance


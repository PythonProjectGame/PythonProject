class stack:
    def __init__(self, length: int, data:list = []) -> None:
        if len(data) > length:
            return
        self.__length = length
        self.__data = [""] * self.__length
        for i in data:
            self.__data.push(i)
        self.__pointer = 0
    
    def is_full(self) -> bool:
        if self.__pointer == self.__length:
            return True
        else:
            return False
    
    def is_empty(self) -> bool:
        if self.__pointer == 0:
            return True
        else:
            return False
    
    def peek(self) -> list:
        return self.__data
    
    def push(self, data: any) -> None:
        if self.is_full():
            return
        else:
            self.__data[self.__pointer] = data
            self.__pointer += 1
    
    def pop(self) -> None:
        if self.is_empty():
            return
        else:
            self.__pointer -= 1
            self.__data[self.__pointer] = ""
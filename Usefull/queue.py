class queue:
    def __init__(self, length: int, data: list = []) -> None:
        if len(data) > length:
            return
        self.__length = length
        self.__data = [""] * self.__length
        self.__head = 0
        self.__tail = -1
        for i in data:
            self.__data.push()

    def is_full(self) -> bool:
        if self.__head == self.__tail-1:
            return True
        else:
            return False

    def is_empty(self) -> bool:
        if self.__head == self.__tail:
            return True
        else:
            return False

    def peek(self) -> list:
        return self.__data

    def pop(self) -> None:
        if self.is_empty():
            pass
        else:
            self.__tail += 1
            if self.__tail == self.__length:
                self.__tail = -1
            self.__data[self.__tail] = ""

    def push(self, data:any) -> None:
        if self.is_full():
            return
        else:
            self.__head += 1
            if self.__head == self.__length:
                self.__head = -1
            self.__data[self.__head] = data

game = queue(2)

game.push("COD")
game.push("warframe")
game.pop()
game.push("hello")
game.pop()
print(game.peek())
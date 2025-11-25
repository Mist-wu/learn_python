class Animal:
    def __init__(self,name):
        self.name = name
    
    def sleep(self):
        print(f"{self.name} is sleeping.")

class Dog(Animal):
    def bark(self):
        print(f"{self.name} says Woof!")

dog = Dog("Snoopy")
dog.bark()
dog.sleep()
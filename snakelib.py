from pygame.math import Vector2
from pygame import USEREVENT
from random import randrange


UPDATE = USEREVENT + 1
SPECIAL_TIMER = USEREVENT + 2


class Food:

    def __init__(self, position: list, points=1, nutrition=1):
        self.position = position
        self.points = points
        self.nutrition = nutrition
    
    def __eq__(self, value: list) -> bool:
        return value == self.position
    
    def __getitem__(self, index: int) -> int:
        return self.position[index]
    
    def __setitem__(self, index: int, value: int) -> None:
        self.position[index] = value


class Snake:

    def __init__(self, position, size=3):
        x, y = position[0] - size + 1, position[1]
        self.segments = [ [x + i, y] for i in range(size) ]
        self.vector = Vector2(1, 0)
        self.alive = True
        self.score = 0
    
    def __contains__(self, segment: list) -> bool:
        return segment in self.segments

    def __getitem__(self, index: int) -> list:
        return self.segments[index]
    
    def __len__(self) -> int:
        return len(self.segments)

    def append(self, segment) -> None:
        self.segments.insert(0, segment)

    def colliding(self, segments=[]) -> bool:
        return self.head in segments if segments else self.head in self.body
    
    @property
    def body(self) -> list:
        return self.segments[:-1]
    
    @property
    def head(self) -> list:
        return self.segments[-1]
    
    @property
    def tail(self) -> list:
        return self.segments[0]
    
    def die(self):
        self.alive = False
    
    def eat(self, food: list|Food):
        if type(food) == list:
            food = Food(food)

        self.score += food.points
        [ self.append( self.tail.copy() ) for _ in range(food.nutrition) ]
    
    def move(self):
        for i, segment in enumerate(self.body):
            segment[0] = self[i + 1][0]
            segment[1] = self[i + 1][1]
        
        self.head[0] += self.vector[0]
        self.head[1] += self.vector[1]
    
    def update(self):
        if self.vector and self.alive:
            self.move()
        
        if self.colliding():
            self.die()
    
    def update_vector(self, vector):
        if vector != -self.vector and vector != self.vector:
            self.vector.update(vector)

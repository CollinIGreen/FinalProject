import pygame
import time
import random

pygame.init()

class Box:
    def __init__(self, list, minEdge):
        list.sort()
        list.reverse()
        self.height = 0
        for i in range(len(list)):
            if list[i] <= minEdge and self.height < list[i]:
                self.height = list.pop(i)
                break
        self.x = list[0]
        self.y = list[1]
        self.size = self.x* self.y* self.height
        self.ltcLocal = [None, None, None]
        self.rlcLocal = [None, None, None]
        self.llcLocal = [None, None, None]
        self.rtcLocal = [None, None, None]
    def turn(self):
        self.x, self.y = self.y, self.x
        if self.ltcLocal != [None, None, None]:
            self.ltcLocal = [self.ltcLocal[0], self.ltcLocal[1], self.ltcLocal[2]]
            self.rlcLocal = [self.ltcLocal[0] + self.x, self.ltcLocal[1] + self.y, self.ltcLocal[2]]
            self.llcLocal = [self.ltcLocal[0], self.ltcLocal[1] + self.y, self.ltcLocal[2]]
            self.rtcLocal = [self.ltcLocal[0] + self.x, self.ltcLocal[1], self.ltcLocal[2]]
    def setLeftCorner(self, lcX, lcY, baseHeight):
        self.ltcLocal = [lcX, lcY, baseHeight]
        self.rlcLocal = [lcX + self.x, lcY + self.y, baseHeight]
        self.llcLocal = [lcX, lcY + self.y, baseHeight]
        self.rtcLocal = [lcX + self.x, lcY, baseHeight]
class container:
    def __init__(self, cargo, dimension):
        self.cargo = cargo
        dimension.sort()
        self.height = dimension[0]
        self.Xdim = dimension[1]
        self.Ydim = dimension[2]
        self.screen = pygame.display.set_mode([self.Xdim, self.Ydim])
    def addCargo(self, box):
        if 0 <= box.ltcLocal[0] <= self.Xdim - box.x and 0 <= box.ltcLocal[1] <= self.Ydim - box.y and 0 <= box.ltcLocal[2] <= self.height-box.height:
            for i in range(len(self.cargo)):
                if self.cargo[i].ltcLocal[0] <= box.ltcLocal[0] < self.cargo[i].rlcLocal[0] and self.cargo[i].ltcLocal[1] <= box.ltcLocal[1] < self.cargo[i].llcLocal[1] and self.cargo[i].ltcLocal[2] <= box.ltcLocal[2] < self.cargo[i].ltcLocal[2]+self.cargo[i].height:
                    return "bad location"
                if self.cargo[i].ltcLocal[0] <= box.ltcLocal[0] < self.cargo[i].rlcLocal[0] and self.cargo[i].ltcLocal[1] < box.rlcLocal[1] <= self.cargo[i].llcLocal[1] and self.cargo[i].ltcLocal[2] <= box.ltcLocal[2] < self.cargo[i].ltcLocal[2]+self.cargo[i].height:
                    return "bad location"
                if self.cargo[i].ltcLocal[0] < box.rtcLocal[0] <= self.cargo[i].rlcLocal[0] and self.cargo[i].ltcLocal[1] <= box.ltcLocal[1]  < self.cargo[i].llcLocal[1] and self.cargo[i].ltcLocal[2] <= box.ltcLocal[2] < self.cargo[i].ltcLocal[2]+self.cargo[i].height:
                    return "bad location"
                if self.cargo[i].ltcLocal[0] < box.rlcLocal[0] <= self.cargo[i].rlcLocal[0] and self.cargo[i].ltcLocal[1] < box.rlcLocal[1] <= self.cargo[i].llcLocal[1] and self.cargo[i].ltcLocal[2] <= box.ltcLocal[2] < self.cargo[i].ltcLocal[2]+self.cargo[i].height:
                    return "bad location"
            self.cargo.append(box)
            return "works"
    def viableLocal(self, box, location):
        if 0 <= location[0] <= self.Xdim - box.x and 0 <= location[1] <= self.Ydim - box.y and 0 <= location[2] <= self.height-box.height:
            for i in range(len(self.cargo)):
                if self.cargo[i].ltcLocal[0] <= location[0] < self.cargo[i].rlcLocal[0] and self.cargo[i].ltcLocal[1] <= location[1] < self.cargo[i].llcLocal[1] and self.cargo[i].ltcLocal[2] <= location[2] < self.cargo[i].ltcLocal[2]+self.cargo[i].height:
                    return False
                if self.cargo[i].ltcLocal[0] <= location[0] < self.cargo[i].rlcLocal[0] and self.cargo[i].ltcLocal[1] < location[1]+box.y <= self.cargo[i].llcLocal[1] and self.cargo[i].ltcLocal[2] <= location[2] < self.cargo[i].ltcLocal[2]+self.cargo[i].height:
                    return False
                if self.cargo[i].ltcLocal[0] < location[0]+box.x <= self.cargo[i].rlcLocal[0] and self.cargo[i].ltcLocal[1] <= location[1] < self.cargo[i].llcLocal[1] and self.cargo[i].ltcLocal[2] <= location[2] < self.cargo[i].ltcLocal[2]+self.cargo[i].height:
                    return False
                if self.cargo[i].ltcLocal[0] < location[0]+box.x <= self.cargo[i].rlcLocal[0] and self.cargo[i].ltcLocal[1] < location[1]+box.y <= self.cargo[i].llcLocal[1] and self.cargo[i].ltcLocal[2] <= location[2] < self.cargo[i].ltcLocal[2]+self.cargo[i].height:
                    return False
            return True
        else:
            return False
    def subCargo(self, box):
        length = len(self.cargo)
        for i in range(len(self.cargo)):
            if self.cargo[i] == box:
                self.cargo.pop(i)
        if length == len(self.cargo):
            print("not in container")
    def dispCon(self):
        for i in range(len(self.cargo)):
            integer = 230*(self.cargo[i].ltcLocal[2] / self.height)
            pygame.draw.rect(self.screen, (255-integer, 0, 0), pygame.Rect(self.cargo[i].ltcLocal[0], self.cargo[i].ltcLocal[1], self.cargo[i].x, self.cargo[i].y))
            pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(self.cargo[i].ltcLocal[0]+2, self.cargo[i].ltcLocal[1]+2, self.cargo[i].x-4, self.cargo[i].y-4))
        hello = 0
        while hello < 1000:
            pygame.display.flip()
            hello += .1
class BoxSplit:
    def __init__(self, dimensions, Cargo):
        self.space = [container([], dimensions)]
        self.boxes = Cargo
        self.storage = []
        self.placement = [[0, 0, 0]]
        self.freeSpace = dimensions[0] * dimensions[1] * dimensions[2]
    def organizeBySize(self):
        for i in range(len(self.boxes)):
            value = self.boxes[i]
            count = i
            for x in range(i, len(self.boxes)):
                if value.size < self.boxes[x].size:
                    value = self.boxes[x]
                    count = x
            self.boxes[i], self.boxes[count] = self.boxes[count], self.boxes[i]
    def MoveToStorage(self, box):
        for i in range(len(self.boxes)):
            if box == self.boxes[i]:
                self.storage.append(self.boxes.pop(i))
                self.freeSpace -= box.size
                return
        return "Not one of your boxes"
    def checkDrops(self):
        box1 = Box([20, 20, 20], 60)
        array = []
        if self.space[0].viableLocal(box1, [0, 0, 0]) == True:
            array.append([0, 0, 0])
        for i in self.storage:
            if self.space[0].viableLocal(box1, i.llcLocal) == True:
                array.append(i.llcLocal)
            if self.space[0].viableLocal(box1, i.rtcLocal) == True:
                array.append(i.rtcLocal)
            topcorner = [i.ltcLocal[0], i.ltcLocal[1], i.ltcLocal[2]]
            topcorner[2] = topcorner[2] + i.height
            if self.space[0].viableLocal(box1, topcorner) == True:
                array.append(topcorner)
        array.sort()
        bestDrop = 0
        if len(array) != 0:
            for i in range(len(array)):
                if array[i][1] < array[bestDrop][1]:
                    bestDrop = i
            array.insert(0, array.pop(bestDrop))
        self.placement = array
    def fillSpace(self):
        track = 0
        length = 1
        while len(self.boxes) != 0 and track < length:
            self.organizeBySize()
            length = len(self.boxes)
            count = 0
            while len(self.boxes) == length and count != length:
                check = None
                if self.boxes[0].size < self.freeSpace:
                    for i in range(len(self.placement)):
                        check = self.space[0].viableLocal(self.boxes[0], self.placement[i])
                        if check == True:
                            self.boxes[0].setLeftCorner(self.placement[i][0], self.placement[i][1], self.placement[i][2])
                            self.space[0].addCargo(self.boxes[0])
                            self.MoveToStorage(self.boxes[0])
                            self.checkDrops()
                            track = 0
                            break
                        else:
                            self.boxes[0].turn()
                            check = self.space[0].viableLocal(self.boxes[0], self.placement[i])
                            if check == True:
                                self.boxes[0].setLeftCorner(self.placement[i][0], self.placement[i][1], self.placement[i][2])
                                self.space[0].addCargo(self.boxes[0])
                                self.MoveToStorage(self.boxes[0])
                                self.checkDrops()
                                track = 0
                                break
                            else:
                                self.boxes[0].turn()
                else:
                    check = False
                if check == False:
                    self.boxes.append(self.boxes.pop(0))
                count += 1
            track += 1
            self.space[0].dispCon()
        return self.boxes
class fill_inventory:
    def __init__(self, cargo, dimensions):
        self.dimensions = dimensions
        self.looseInv = cargo
        self.containers = [BoxSplit(dimensions, cargo)]
    def StoreCargo(self):
        count = 0
        while len(self.looseInv) != 0:
            self.looseInv = self.containers[count].fillSpace()
            self.containers.append(BoxSplit(self.dimensions, self.looseInv))
            count += 1
        return count

cont1 = container([], [120, 90, 60])
array = [Box([40, 30, 50], 60), Box([40, 30, 50], 60), Box([30, 30, 30], 60), Box([30, 30, 30], 60), Box([30, 30, 30], 60), Box([30, 30, 30], 60), Box([30, 30, 30], 60),
         Box([30, 30, 30], 60), Box([60, 20, 20], 60), Box([60, 20, 20], 60)]
program = fill_inventory(array, [120, 90, 60])
print(program.StoreCargo())
time.sleep(10)
array = [Box([40, 30, 50], 60), Box([40, 30, 50], 60), Box([40, 30, 50], 60), Box([40, 30, 50], 60), Box([40, 30, 50], 60), Box([40, 30, 50], 60), Box([30, 30, 30], 60),
         Box([30, 30, 30], 60), Box([30, 30, 30], 60), Box([30, 30, 30], 60), Box([30, 30, 30], 60), Box([30, 30, 30], 60), Box([30, 30, 30], 60), Box([30, 30, 30], 60),
         Box([30, 30, 30], 60), Box([30, 30, 30], 60), Box([60, 20, 20], 60), Box([60, 20, 20], 60), Box([60, 20, 20], 60), Box([60, 20, 20], 60), Box([60, 20, 20], 60)]
program = fill_inventory(array, [120, 90, 60])
print(program.StoreCargo())
time.sleep(10)
array = [Box([40, 30, 50], 60), Box([40, 30, 50], 60), Box([40, 30, 50], 60), Box([40, 30, 50], 60), Box([40, 30, 50], 60), Box([40, 30, 50], 60), Box([40, 30, 50], 60),
         Box([40, 30, 50], 60), Box([40, 30, 50], 60), Box([40, 30, 50], 60), Box([40, 30, 50], 60), Box([40, 30, 50], 60), Box([30, 30, 30], 60), Box([30, 30, 30], 60),
         Box([30, 30, 30], 60), Box([30, 30, 30], 60), Box([30, 30, 30], 60), Box([30, 30, 30], 60), Box([30, 30, 30], 60), Box([30, 30, 30], 60), Box([30, 30, 30], 60),
         Box([30, 30, 30], 60), Box([30, 30, 30], 60), Box([30, 30, 30], 60), Box([60, 20, 20], 60), Box([60, 20, 20], 60), Box([60, 20, 20], 60), Box([60, 20, 20], 60),
         Box([60, 20, 20], 60), Box([60, 20, 20], 60)]
program = fill_inventory(array, [120, 90, 60])
print(program.StoreCargo())


class Producer:
    def __init__(self) -> None:
        self._sleep = False  # Sleep state
        self._remainingTime = 0  # Remaining time to wake up
        self._available = True  # True = Espacio Disponible, False = Espacio Ocupado
        self._produceItems = 0  # Number of items to produce
        self._lasItemIndx = 0  # Last item index

    def isSleeping(self) -> bool:
        return self._sleep

    def getRemainingTime(self) -> int:
        return self._remainingTime

    def getProduceItems(self) -> int:
        return self._produceItems

    def isAvailable(self) -> bool:
        return self._available

    def getLastItemIndex(self) -> int:
        return self._lasItemIndx

    def setSleep(self, sleep: bool) -> None:
        self._sleep = sleep

    def setRemainingTime(self, remainingTime: int) -> None:
        self._remainingTime = remainingTime

    def setProduceItems(self, produceItems: int) -> None:
        self._produceItems = produceItems
        if (self._produceItems > 0):
            self._available = True

    def setAvailability(self, available: bool) -> None:
        self._available = available

    def setLastItemIndex(self, lastItemIndex: int) -> None:
        self._lasItemIndx = lastItemIndex

    def update(self) -> None:
        if (self._sleep):
            self._remainingTime -= 1
            if (not self._remainingTime):
                self._sleep = False
                self._available = True
        else:
            if (self._produceItems > 0):
                self._produceItems -= 1
                self._lasItemIndx += 1
                if (self._lasItemIndx == 20):
                    self._lasItemIndx = 0
            if (not self._produceItems):
                self._sleep = True
                self._available = False

class queue:
    arr = []

    def __init__(self, length):
        self.arr = []
        self.capacity = length


    def enqueue(self, element) :
        if len(self.arr) == self.capacity:
            print("The stack is full")
            else:
            self.arr.append(element)

    def dequeue(self):
                if len(self.arr) == 0:
                    print("The Queue is empty")
            else:
    del self.arr[0]

    def display(self):
        print(self.arr)

    def isempty(self):
        if len(self.arr):
            print("The queue is empty")
            return True
            else:
            print("The queue is not empty")
            return False
        queue_privilaged = queue(20)
        queue_normal = queue(20)
        print("Enter number of customers")
        n = int(input())
        for i in range(n):
            print("enter the amount")
        amount = int(input())
        if amount > 200000:
            queue_privilaged.enqueue(amount)
        elif amount < 40000:
            queue_normal.enqueue(amount)
        sum_privilaged = 0
        sum_normal = 0
        for i in range(len(queue_privilaged.arr)):
            sum_privilaged = sum_privilaged + queue_privilaged.arr[i]
        for i in range(len(queue_normal.arr)):
            sum_normal = sum_normal + queue_normal.arr[i]
        print("The sum of privilaged customers :")
        print(sum_privilaged)
        print("The sum of normal customers :")
        print(sum_normal)





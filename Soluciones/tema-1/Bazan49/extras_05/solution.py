def floyd(head):
    tortoise = hare = head
    iterations = 0
    
    while hare is not None and hare.next is not None:
        tortoise = tortoise.next
        hare = hare.next.next
        iterations += 1
        
        if tortoise is hare:
            return True, iterations
            
    return False, iterations
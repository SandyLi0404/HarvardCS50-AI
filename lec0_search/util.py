class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action
    
    def __str__(self) -> str:
        return str((self.parent, self.action, self.state))


class StackFrontier(): # DFS
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node
    
    def __str__(self) -> str:
        return str([str(i) for i in self.frontier])

class QueueFrontier(StackFrontier): # BFS

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node
    
    def __str__(self) -> str:
        return str([str(i) for i in self.frontier])

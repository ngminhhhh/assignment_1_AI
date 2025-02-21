from abc import ABC, abstractmethod

class Piece(ABC):
    def __init__(self, x, y, board_size = 8):
        self.board_size = board_size
        self.x = x
        self.y = y

    def is_in_bound(self, nx, ny):
        return 0 <= nx < self.board_size and 0 <= ny < self.board_size
        
    def get_piece(self, nx, ny, pieces):
        if not self.is_in_bound(nx, ny):
            return None

        for piece in pieces:
            if piece is not self and piece.x == nx and piece.y == ny:
                return piece
            
        return None
    
    def clone(self):
        new_piece = self.__class__(self.x, self.y)
        new_piece.board_size = self.board_size
        new_piece.type = self.type
        new_piece.point = self.point
        
        return new_piece
    
    # Override print method
    def __repr__(self):
        return f"{self.type} at ({self.x}, {self.y})"

    @abstractmethod
    def get_valid_moves(self, pieces) -> list:
        pass

    def moves(self, nx, ny):
        self.x = nx
        self.y = ny

class Knight(Piece):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.point = 3
        self.type = "Knight"

    def get_valid_moves(self, pieces) -> list:
        moves = []
        offsets = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                   (1, -2), (1, 2), (2, -1), (2, 1)]
        
        for dx, dy in offsets:
            nx = self.x + dx
            ny = self.y + dy
            piece = self.get_piece(nx, ny, pieces)

            if piece is not None:
                moves.append((nx, ny, piece))

        return moves
    
class Rook(Piece):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type = "Rook"
        self.point = 5

    def get_valid_moves(self, pieces):
        moves = []
        
        # left (offset: (-1, 0))
        for nx in range(self.x - 1, -1, -1):
            piece = self.get_piece(nx, self.y, pieces)

            if piece is not None:
                moves.append((nx, self.y, piece))
                break
        
        # right (offset: (1, 0))
        for nx in range(self.x + 1, self.board_size):
            piece = self.get_piece(nx, self.y, pieces)

            if piece is not None:
                moves.append((nx, self.y, piece))
                break       

        # up (offset: (0, -1))
        for ny in range(self.y - 1, -1, -1):
            piece = self.get_piece(self.x, ny, pieces)

            if piece is not None:
                moves.append((self.x, ny, piece))
                break

        # down (offset: (0, 1))
        for ny in range(self.y + 1, self.board_size):
            piece = self.get_piece(self.x, ny, pieces)
            if piece is not None:
                moves.append((self.x, ny, piece))
                break         

        return moves
    
class Bishop(Piece):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type = "Bishop"
        self.point = 3

    def get_valid_moves(self, pieces):
        moves = []
        
        nx, ny = self.x - 1, self.y - 1
        while nx >= 0 and ny >= 0:
            piece = self.get_piece(nx, ny, pieces)

            if piece is not None:
                moves.append((nx, ny, piece))
                break
            nx -= 1
            ny -= 1

        nx, ny = self.x - 1, self.y + 1
        while nx >= 0 and ny < self.board_size:
            piece = self.get_piece(nx, ny, pieces)

            if piece is not None:
                moves.append((nx, ny, piece))
                break
            nx -= 1
            ny += 1

        nx, ny = self.x + 1, self.y - 1
        while nx < self.board_size and ny >= 0:
            piece = self.get_piece(nx, ny, pieces)

            if piece is not None:
                moves.append((nx, ny, piece))
                break
            nx += 1
            ny -= 1

        nx, ny = self.x + 1, self.y + 1
        while nx < self.board_size and ny < self.board_size:
            piece = self.get_piece(nx, ny, pieces)

            if piece is not None:
                moves.append((nx, ny, piece))
                break

            nx += 1
            ny += 1

        return moves
    
class Pawn(Piece):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type = "Pawn"
        self.point = 1

    def get_valid_moves(self, pieces):
        moves = []
        offsets = [(-1, -1), (-1, 1)]

        for dx, dy in offsets:
            nx = self.x + dx
            ny = self.y + dy
            piece = self.get_piece(nx, ny, pieces)

            if piece is not None:
                moves.append((nx, ny, piece))

        return moves
    
class King(Piece):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type = "King"
        self.point = 2

    def get_valid_moves(self, pieces):
        moves = []
        offsets = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, -1)]

        for dx, dy in offsets:
            nx = self.x + dx
            ny = self.y + dy
            piece = self.get_piece(nx, ny, pieces)

            if piece is not None:
                moves.append((nx, ny, piece))

        return moves
    
class Queen(Piece):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type = "Queen"
        self.point = 8

    def get_valid_moves(self, pieces):
        moves = []
        
        # Top-left (offset: -1, -1)
        nx, ny = self.x - 1, self.y - 1
        while nx >= 0 and ny >= 0:
            piece = self.get_piece(nx, ny, pieces)

            if piece is not None:
                moves.append((nx, ny, piece))
                break
            
            nx -= 1
            ny -= 1

        # Top-right (offset: -1, +1)
        nx, ny = self.x - 1, self.y + 1
        while nx >= 0 and ny < self.board_size:
            piece = self.get_piece(nx, ny, pieces)

            if piece is not None:
                moves.append((nx, ny, piece))
                break
            
            nx -= 1
            ny += 1

        # Bottom-left (offset: +1, -1)
        nx, ny = self.x + 1, self.y - 1
        while nx < self.board_size and ny >= 0:
            piece = self.get_piece(nx, ny, pieces)

            if piece is not None:
                moves.append((nx, ny, piece))
                break
            
            nx += 1
            ny -= 1

        # Bottom-right (offset: +1, +1)
        nx, ny = self.x + 1, self.y + 1
        while nx < self.board_size and ny < self.board_size:
            piece = self.get_piece(nx, ny, pieces)

            if piece is not None:
                moves.append((nx, ny, piece))
                break
            
            nx += 1
            ny += 1

        # Left (offset: -1, 0)
        nx = self.x - 1
        while nx >= 0:
            piece = self.get_piece(nx, ny, pieces)
            if piece is not None:
                moves.append((nx, ny, piece))
                break
            nx -= 1

        # Right (offset: +1, 0)
        nx = self.x + 1
        while nx < self.board_size:
            piece = self.get_piece(nx, ny, pieces)
            if piece is not None:
                moves.append((nx, ny, piece))
                break
            nx += 1

        # Up (offset: 0, -1)
        ny = self.y - 1
        while ny >= 0:
            piece = self.get_piece(nx, ny, pieces)
            if piece is not None:
                moves.append((nx, ny, piece))
                break
            ny -= 1

        # Down (offset: 0, +1)
        ny = self.y + 1
        while ny < self.board_size:
            piece = self.get_piece(nx, ny, pieces)
            if piece is not None:
                moves.append((nx, ny, piece))
                break
            ny += 1

        return moves
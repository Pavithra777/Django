import json
import copy
class GameMoves:
    def __init__(self,moves):
        self.moves = moves
        self.piece_position = {}
        self.move_position = []
    def load_piece_position(self):
        with open('static/chess_initial_position.json') as file:
            return json.load(file)

    def find_piece(self,notation):
        if notation[0].islower() :
            return 'P'
        elif notation[0]=='O':
            return 'C'
        return notation[0]

    def update_pawn_move(self, active_player, notation):
        pawn_items = {key: value for key, value in self.piece_position[active_player].items() if key.startswith('P')}
        pawn_item_in_move = {key: value for key, value in pawn_items.items() if value!=None and value.startswith(notation[0])}
        if len(pawn_item_in_move) > 1:
            print('pawn_item_in_move',pawn_item_in_move)
            print(notation[-1])
            print('test',[(v,int(v[-1])-int(notation[-1])) for k,v in pawn_item_in_move.items()])
            pawn_item_in_move = { k:v for k,v in pawn_item_in_move.items() if (abs(int(v[-1])-int(notation[-1])) == 1 or (abs(int(v[-1])-int(notation[-1])) ==2 and v[-1])=='2') }
            print('pawn_item_in_move',pawn_item_in_move)
            if  len(pawn_item_in_move) > 1:
                
                other_player = 'black' if active_player == 'white' else 'white'
                all_piece_pos=list(self.piece_position[active_player].values())+list(self.piece_position[other_player].values())
                print('all_piece_pos',all_piece_pos)
                print('pawn_item_in_move',pawn_item_in_move)
                remove_piece =[]
                for k,v in pawn_item_in_move.items():
                    piece_in_btwn = ''
                    if int(v[-1]) > int(notation[-1]):
                        print('range',range(int(notation[-1])+1,int(v[-1])))
                        for rank_pos in range(int(notation[-1])+1,int(v[-1])):
                            piece_in_btwn = 'v[0]'+str(rank_pos)
                    else:
                        print('range',range(int(v[-1])+1,int(notation[-1])))
                        for rank_pos in range(int(v[-1])+1,int(notation[-1])):
                            piece_in_btwn = v[0]+str(rank_pos)
                    print('piece_in_btwn',piece_in_btwn)
                    if  piece_in_btwn != '':
                        remove_piece.append(k)
                print('remove_piece',remove_piece)
                for k in remove_piece:
                    del pawn_item_in_move[k]
                print('pawn_item_in_move',pawn_item_in_move)
        piece, pos = next(iter(pawn_item_in_move.items()))
        self.piece_position[active_player][piece] = notation[-2:]
    
    def update_castle_move(self, active_player, notation):
        king_items = {key: value for key, value in self.piece_position[active_player].items() if key.startswith('K')}
        rook_items = [[key, value] for key, value in self.piece_position[active_player].items() if key.startswith('R')]
        if notation == 'O-O':      
            if ord(rook_items[0][1][0]) > ord(rook_items[1][1][0]):
                rook_item_in_move = rook_items[0]
            else:
                rook_item_in_move = rook_items[1]
        else:
            if ord(rook_items[0][1][0]) < ord(rook_items[1][1][0]):
                rook_item_in_move = rook_items[0]
            else:
                rook_item_in_move = rook_items[1]
        rook_piece, rook_pos = rook_item_in_move
        king_piece, king_pos = next(iter(king_items.items()))
        if notation == 'O-O':
            self.piece_position[active_player][king_piece] = chr(ord(king_pos[0])+2) + king_pos[1] 
            king_pos = self.piece_position[active_player][king_piece] 
            self.piece_position[active_player][rook_piece] = chr(ord(king_pos[0])-1) + king_pos[1] 
        else:
            self.piece_position[active_player][king_piece] = chr(ord(king_pos[0])-2) + king_pos[1] 
            king_pos = self.piece_position[active_player][king_piece] 
            self.piece_position[active_player][rook_piece] = chr(ord(king_pos[0])+1) + king_pos[1] 
    def get_possible_knight_move(self,pos):
        possible_pos = []
        file_last = 104
        file_first = 97
        rank_last = 8  
        rank_first = 1
        p1 , p2 =pos[0], pos[1]
        if p2.isdigit():
            file = ord(p1)
            rank = int(p2)
        else:
            file = ord(p2)
            rank = int(p1)
        directions = [
            [file, rank],  # Vertical move
            [rank, file]   # Horizontal move
        ]
        first_steps = [2, -2]
        sec_steps = [1, -1]
        for dirc in directions:
            d1, d2 = dirc
            for first_step in first_steps:
                for sec_step in sec_steps:
                    d1temp = d1 + first_step
                    d2temp = d2 + sec_step
                    new_file = d1temp if d1 > 8 else d2temp
                    new_rank = d2temp if d1 > 8 else d1temp
                    if file_first <= new_file <= file_last and rank_first <= new_rank <= rank_last:
                        self.get_pos(new_file, new_rank,possible_pos)
        return possible_pos

    def get_pos(self,new_file, new_rank,possible_pos):
        possible_pos.append(chr(new_file) + str(new_rank))

    def update_bishop_move(self, active_player, notation):
        bishop_items = {key: value for key, value in self.piece_position[active_player].items() if key.startswith('B') and value is not None}
        bishop_item_in_move = {key: value for key, value in bishop_items.items() if self.get_square_color(value)==self.get_square_color(notation[-2:])}
        piece, pos = next(iter(bishop_item_in_move.items()))
        self.piece_position[active_player][piece] = notation[-2:]

    def update_royal_move(self, active_player, notation):
        royal_items = {key: value for key, value in self.piece_position[active_player].items() if key.startswith(notation[0])}
        piece, pos = next(iter(royal_items.items()))
        self.piece_position[active_player][piece] = notation[-2:]

    def update_rook_move(self, active_player, notation):
        notation = notation.replace('R', '').replace('x', '')
        target = notation[-2:]
        rook_items = {key: value for key, value in self.piece_position[active_player].items() if key.startswith('R') and value is not None}
        rook_item_in_move = {key: value for key, value in rook_items.items() if value[0] == target[0] or 
                             value[1] == target[1]}
        other_player = 'black' if active_player == 'white' else 'white'
        all_piece_pos = [v for k, v in self.piece_position[active_player].items()] + [v for k, v in self.piece_position[other_player].items()]
        print('rook_item_in_move',rook_item_in_move)
        if len(notation) > 2:
            rook_item_in_move = {k:v for k,v in rook_item_in_move.items() if notation[0] == v[0]}
        print('rook_item_in_move',rook_item_in_move)
        if len(rook_item_in_move) > 1:
            for rook_pos, rook_move in list(rook_item_in_move.items()):
                rank, file = int(rook_move[1]), rook_move[0]
                rank_range = [target[1]] if rank == int(target[1]) else list(map(str, range(rank + 1, int(target[1]))))
                file_range = [target[0]] if file == target[0] else [chr(f) for f in range(ord(file) + 1, ord(target[0]))]
                if any(f + r in all_piece_pos for f in file_range for r in rank_range):
                    del rook_item_in_move[rook_pos]
        print('rook_item_in_move',rook_item_in_move)
        print('notation',notation)
        piece = next(iter(rook_item_in_move))  
       
        self.piece_position[active_player][piece] = target

    def get_square_color(self,pos):
        f = ord(pos[0])
        r = int(pos[1])
        if (f%2==0 or r%2==0) and (f%2!=0 or r%2!=0):
            return 'black'
        else:
            return 'white'


    def update_knight_move(self, active_player, notation):
        target = notation[-2:]
        knight_items = {key: value for key, value in self.piece_position[active_player].items() if key.startswith('N')}
        player_piece_pos = [ value for key, value in self.piece_position[active_player].items()]
        #p1, p2, file_first, file_last, rank_first, rank_last
        knight_possible_moves = {key:self.get_possible_knight_move(value) for key,value in knight_items.items() if value is not None }
        notation = notation.replace('N','').replace('x','')
        
        if len(notation) >=3:
            possible_active_knight = [k for k,v in knight_items.items() if notation[0] ==  v[0]]
        else:
            for piece,knight_moves in knight_possible_moves.items():
                common_items = set(player_piece_pos) & set(knight_moves)  
                knight_moves = [item for item in knight_moves if item not in common_items]
                knight_possible_moves[piece]=knight_moves
            possible_active_knight = [key for key,value in knight_possible_moves.items() if target in value ]
        
        print('possible_active_knight',possible_active_knight)
        if len(possible_active_knight) == 1:
            active_piece = possible_active_knight[0]
            self.piece_position[active_player][active_piece] = target 
        else:
            active_piece= notation.replace(target,"")
            if len(active_piece) == 1:
                active_piece = [key for key in possible_active_knight if key.startswith(active_piece)][0]
                self.piece_position[active_player][active_piece] = target
            else:
                active_piece = [key for key in possible_active_knight if key==active_piece][0]
                self.piece_position[active_player][active_piece] = target

    def remove_captured_piece(self,notation,active_player):
        inactive_player = 'black' if active_player == 'white' else 'white'
        piece_captured_item = {key: value for key, value in self.piece_position[inactive_player].items() if value == notation[-2:]}
        piece_captured, pos = next(iter(piece_captured_item.items()))
        self.piece_position[inactive_player][piece_captured] = None

    def get_moves(self):
        self.piece_position = self.load_piece_position()
        #moves = ['c3', 'd5', 'c4', 'g5', 'cxd5','Nc6','f4','Bf5','h4','h5','Rh3','Kd7']
        players = ['white', 'black']

        for i, move in enumerate(self.moves):
            player = players[i % 2]
            move = move.replace('+','')
            piece = self.find_piece(move)
            if piece == 'P':
                self.update_pawn_move(player, move)
            elif piece == 'N':
                self.update_knight_move( player, move)
            elif piece == 'B':
                self.update_bishop_move( player, move)
            elif piece == 'R':
                self.update_rook_move(player, move)
            elif piece == 'C':
                self.update_castle_move(player,move)
            else:
                self.update_royal_move( player, move)
            if 'x' in move:
                self.remove_captured_piece(move,player) 
            pos = copy.deepcopy(self.piece_position)
            self.move_position.append(pos)
            #print(player, ' : ', {key: value for key, value in piece_position[player].items() if key.startswith('P')})
        return self.move_position



    # print('-------------------------------------------------------------------------')
    # print(piece_position)

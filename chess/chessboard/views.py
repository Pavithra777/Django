from django.shortcuts import render
from django.http import HttpResponse
import json
from . import game_moves
#load_piece_position()

games={}
step = -1
files=['a','b','c','d','e','f','g','h']
def home(request):
    return render(request,'chessboard/home.html')

def load_piece_position():
    global moves
    with open('static/game1.json') as file:
        moves= json.load(file)
    
def room(request,game,direction):
    #steps = ['c3', 'd5', 'c4', 'g5', 'cxd5','Nc6','f4','Bf5','h4','h5','Rh3','Kd7','e3','Kc8','Bd3','Qd7','Rh1','O-O-O',
     #        'Nh3','Bxd3','O-O','a5','Nxg5','Rh6','Nh7','Rxh7','d6','Qxd6','Na3','Bxf1','Kxf1','Qxa3','bxa3','e5','a4','Nb4']
    steps = ['e4','e5','Nf3','Nc6','Bc4','Nf6','d3','Bc5','a4','d6','O-O','a5',
             'Be3','Bxe3','fxe3','O-O','Nbd2','Ne7','Nh4','c6','Qe1','d5',
             'Bb3','Qd6','Qg3','Nh5','Qg5','g6','Nf5','Bxf5','exf5','Kg7','Kh1','Qf6',
             'Qxf6+','Nxf6','fxg6','hxg6','e4','dxe4','dxe4','Rad8','Rf2','Rd4','Raf1','Neg8',
             'c3','Rd7','Re2','Re7','Bc2','Nd7','Nc4','Ra8','g4','f6','Rg2','Nh6','g5','fxg5',
             'Rxg5','Nf7','Rg2','Re6','Rd2','Rf6','Rxf6','Nxf6','b4','axb4','cxb4','Kf8','Kg2','Ke7',
             'a5','Rh8','Re2','Nh5','Kg1','Nf4']
    global step
    print('in room')
    if game not in games:
        
        game_moves_obj = game_moves.GameMoves(steps)
        games[game]=game_moves_obj.get_moves()
    print('loaded game')
    if direction == 'next':
        if step < len(games[game])-1:
            step = step+1
    elif direction == 'prev':
        if step > 0:
            step = step-1
    elif direction.isdigit():
        st = int(direction)
        if st < len(games[game]) and st >= 0:
            step = st
    moves = games[game][step]
    chess_pos = []
    for j in range(8,0,-1):
        for i in range(8):
            pos = files[i]+str(j)
            box_color = 'dark'
            if (i%2==0 and j%2 ==0) or (i%2!=0 and j%2 !=0):
                box_color = 'light'
            piece = None
            image = None
            for piece_color in ['white', 'black']:
                matching_pieces = [key for key, value in moves[piece_color].items() if value == pos]
                if matching_pieces:
                    piece = matching_pieces[0]
                    break  # Exit the loop if a matching piece is found
            if piece is not None:
                image= 'images/chess_pieces/'+piece_color+'/'+piece[0]+'.png'
            chess_pos.append({'pos': pos,'box_color' : box_color,'piece' : piece, 'image' : image})   
    move_pos=[[{'idx':i,'pos':steps[i]}, {'idx':i+1,'pos':steps[i + 1]}] for i in range(0, len(steps), 2)]
    context = {'range':range(8),'chess_pos':chess_pos,'move_pos':move_pos}
    return render(request,'chessboard/room.html',context)

# Create your views here.

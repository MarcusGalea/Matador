from fastapi import FastAPI

from app.src.model.game_state import GameState
from app.src.model.spiller import Spiller
from app.src.model.felt import Felt
from app.src.model import game_state

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/matador/example_game_start")
def read_item():
    # start example game
    try:
        example_game = create_example_game()
    except Exception as e:
        print("Error creating example game:", e)
        return {"text": "Error creating example game"}
   
    return { "text": "matador started" }
    
    # return {
    #     "players": [
    #         {
    #             "navn": p.navn,
    #             "pos": p.pos,
    #             "penge": p.penge,
    #             "konkurs": p.konkurs,
    #         }
    #         for p in game_state.players
    #     ],
    #     "felter": [
    #         {
    #             "navn": f.navn
    #         }
    #         for f in game_state.felter
    #     ],
    #     "current_player_index": game_state.current_player_index,
    #     "phase": game_state.phase,
    # }
    
def create_example_game() -> GameState:
    
    # Create players
    player1 = Spiller("Alice")
    player2 = Spiller("Bob")
    
    # Create fields (simplified)
    felter = [Felt(f"Felt {i}") for i in range(40)]
    
    # Create game state
    game_state = GameState(players=[player1, player2], felter=felter)
    
    return game_state
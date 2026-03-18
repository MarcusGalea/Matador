
# class GameState:
#     players: list[PlayerState]
#     fields: list[FieldState]
#     current_player_index: int
#     phase: str
#     dice_result: int | None
#     winner_id: str | None
#     pending_decision: dict | None
#     log: list[GameEvent]

from app.src.model.spiller import Spiller
from app.src.model.felt import Felt

class GameState:
    def __init__(self,
                players: list[Spiller],
                felter: list[Felt],
                current_player_index: int = 0,
                phase = "roll"):
        self.players = players
        self.felter = felter
        self.current_player_index = current_player_index
        self.phase = phase
        self.pending_decision = None
        self.dice_result = None
        self.winner_index = None
        self.game_over = False
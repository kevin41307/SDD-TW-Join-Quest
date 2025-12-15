from behave import given, when, then
from src.order_service import OrderService


@given('the board is empty except for a {piece_type} at ({row:d}, {col:d})')
def step_board_empty_except_piece(context, piece_type, row, col):
    """設定棋盤上只有一個棋子"""
    context.order_service = OrderService()
    # 解析棋子顏色和類型
    color = "Red" if piece_type.startswith("Red") else "Black"
    piece_name = piece_type.replace("Red ", "").replace("Black ", "")
    context.board_state = {
        (row, col): {"color": color, "type": piece_name}
    }
    context.current_piece = {"type": piece_name, "color": color, "position": (row, col)}


@given('the board has:')
def step_board_has_pieces(context):
    """設定棋盤上有多個棋子"""
    context.order_service = OrderService()
    context.board_state = {}
    for row in context.table:
        piece_name = row['Piece']
        position_str = row['Position'].strip('()')
        row_pos, col_pos = map(int, position_str.split(', '))
        
        # 解析顏色和類型
        color = "Red" if piece_name.startswith("Red") else "Black"
        piece_type = piece_name.replace("Red ", "").replace("Black ", "")
        
        context.board_state[(row_pos, col_pos)] = {
            "color": color,
            "type": piece_type
        }


@when('{color} moves the {piece_type} from ({from_row:d}, {from_col:d}) to ({to_row:d}, {to_col:d})')
def step_move_piece(context, color, piece_type, from_row, from_col, to_row, to_col):
    """執行棋子移動"""
    from_pos = (from_row, from_col)
    to_pos = (to_row, to_col)
    
    # 檢查移動是否合法
    context.move_result = context.order_service.is_legal_move(
        piece_type, color, from_pos, to_pos, context.board_state
    )
    
    # 同時檢查是否獲勝（用於獲勝相關的 scenario）
    context.win_result = context.order_service.check_game_over(
        piece_type, color, from_pos, to_pos, context.board_state
    )


@then('the move is legal')
def step_move_is_legal(context):
    """檢查移動是否合法"""
    assert context.move_result is True, f"Expected move to be legal, but got {context.move_result}"


@then('the move is illegal')
def step_move_is_illegal(context):
    """檢查移動是否不合法"""
    assert context.move_result is False, f"Expected move to be illegal, but got {context.move_result}"


@then('{color} wins immediately')
def step_wins_immediately(context, color):
    """檢查是否立即獲勝"""
    assert context.win_result is True, f"Expected {color} to win immediately, but got {context.win_result}"


@then('the game is not over just from that capture')
def step_game_not_over(context):
    """檢查遊戲未結束"""
    assert context.win_result is False, f"Expected game to continue, but got win result {context.win_result}"


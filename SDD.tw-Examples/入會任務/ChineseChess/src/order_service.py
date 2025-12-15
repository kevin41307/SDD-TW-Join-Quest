"""
OrderService 類別
處理象棋規則驗證邏輯
"""


class OrderService:
    """象棋規則服務類別，處理棋子移動規則驗證"""
    
    def __init__(self):
        """初始化 OrderService"""
        self.board = None
    
    def is_legal_move(self, piece_type, color, from_pos, to_pos, board_state):
        """
        檢查移動是否合法
        
        Args:
            piece_type: 棋子類型 (General, Guard, Rook, Horse, Cannon, Elephant, Soldier)
            color: 棋子顏色 (Red, Black)
            from_pos: 起始位置 (row, col)
            to_pos: 目標位置 (row, col)
            board_state: 棋盤狀態
        
        Returns:
            bool: 移動是否合法
        """
        if piece_type == "General":
            return self._is_legal_general_move(color, from_pos, to_pos, board_state)
        elif piece_type == "Guard":
            return self._is_legal_guard_move(color, from_pos, to_pos, board_state)
        elif piece_type == "Rook":
            return self._is_legal_rook_move(color, from_pos, to_pos, board_state)
        # 其他棋子類型暫時不實作
        return False
    
    def _is_legal_general_move(self, color, from_pos, to_pos, board_state):
        """
        檢查將/帥的移動是否合法
        
        規則：
        1. 只能在宮內移動（紅方：row 1-3, col 4-6；黑方：row 8-10, col 4-6）
        2. 只能橫向或縱向移動一格
        3. 不能面對面（同一列且中間沒有棋子）
        """
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        # 檢查目標位置是否在宮內
        if color == "Red":
            # 紅方宮：row 1-3, col 4-6
            if not (1 <= to_row <= 3 and 4 <= to_col <= 6):
                return False
        else:  # Black
            # 黑方宮：row 8-10, col 4-6
            if not (8 <= to_row <= 10 and 4 <= to_col <= 6):
                return False
        
        # 檢查是否只移動一格（橫向或縱向）
        row_diff = abs(to_row - from_row)
        col_diff = abs(to_col - from_col)
        if not ((row_diff == 1 and col_diff == 0) or (row_diff == 0 and col_diff == 1)):
            return False
        
        # 檢查是否面對面（同一列且中間沒有棋子）
        if self._generals_face_each_other(color, to_pos, board_state):
            return False
        
        return True
    
    def _generals_face_each_other(self, color, to_pos, board_state):
        """
        檢查將/帥是否面對面（同一列且中間沒有棋子）
        """
        to_row, to_col = to_pos
        
        # 找出兩個將/帥的位置
        red_general_pos = None
        black_general_pos = None
        
        for pos, piece_info in board_state.items():
            if piece_info["type"] == "General":
                if piece_info["color"] == "Red":
                    red_general_pos = pos
                else:
                    black_general_pos = pos
        
        # 如果移動後的位置是將/帥的新位置，需要更新
        # 這裡簡化處理：檢查移動後的列是否與對方將/帥在同一列
        if color == "Red":
            # 紅方移動後，檢查是否與黑方將/帥在同一列
            if black_general_pos and black_general_pos[1] == to_col:
                # 檢查中間是否有棋子
                min_row = min(to_row, black_general_pos[0])
                max_row = max(to_row, black_general_pos[0])
                for row in range(min_row + 1, max_row):
                    if (row, to_col) in board_state:
                        return False  # 中間有棋子，不面對面
                return True  # 中間沒有棋子，面對面
        else:  # Black
            # 黑方移動後，檢查是否與紅方將/帥在同一列
            if red_general_pos and red_general_pos[1] == to_col:
                # 檢查中間是否有棋子
                min_row = min(to_row, red_general_pos[0])
                max_row = max(to_row, red_general_pos[0])
                for row in range(min_row + 1, max_row):
                    if (row, to_col) in board_state:
                        return False  # 中間有棋子，不面對面
                return True  # 中間沒有棋子，面對面
        
        return False
    
    def _is_legal_guard_move(self, color, from_pos, to_pos, board_state):
        """
        檢查士/仕的移動是否合法
        
        規則：
        1. 只能在宮內移動（紅方：row 1-3, col 4-6；黑方：row 8-10, col 4-6）
        2. 只能斜向移動一格（不能橫向或縱向）
        """
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        # 檢查目標位置是否在宮內
        if color == "Red":
            # 紅方宮：row 1-3, col 4-6
            if not (1 <= to_row <= 3 and 4 <= to_col <= 6):
                return False
        else:  # Black
            # 黑方宮：row 8-10, col 4-6
            if not (8 <= to_row <= 10 and 4 <= to_col <= 6):
                return False
        
        # 檢查是否只斜向移動一格
        row_diff = abs(to_row - from_row)
        col_diff = abs(to_col - from_col)
        if not (row_diff == 1 and col_diff == 1):
            return False
        
        return True
    
    def _is_legal_rook_move(self, color, from_pos, to_pos, board_state):
        """
        檢查車的移動是否合法
        
        規則：
        1. 只能橫向或縱向移動
        2. 路徑上不能有其他棋子（不能跳過棋子）
        """
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        # 檢查是否為橫向或縱向移動
        row_diff = abs(to_row - from_row)
        col_diff = abs(to_col - from_col)
        if not ((row_diff == 0 and col_diff > 0) or (row_diff > 0 and col_diff == 0)):
            return False
        
        # 檢查路徑上是否有其他棋子
        if row_diff == 0:  # 橫向移動
            min_col = min(from_col, to_col)
            max_col = max(from_col, to_col)
            for col in range(min_col + 1, max_col):
                if (from_row, col) in board_state:
                    return False  # 路徑上有棋子
        else:  # 縱向移動
            min_row = min(from_row, to_row)
            max_row = max(from_row, to_row)
            for row in range(min_row + 1, max_row):
                if (row, from_col) in board_state:
                    return False  # 路徑上有棋子
        
        return True
    
    def check_game_over(self, piece_type, color, from_pos, to_pos, board_state):
        """
        檢查遊戲是否結束（是否吃掉對方的將/帥）
        
        Args:
            piece_type: 棋子類型
            color: 棋子顏色
            from_pos: 起始位置
            to_pos: 目標位置
            board_state: 棋盤狀態
        
        Returns:
            bool: 是否立即獲勝
        """
        # 暫時不實作，讓測試失敗
        return False


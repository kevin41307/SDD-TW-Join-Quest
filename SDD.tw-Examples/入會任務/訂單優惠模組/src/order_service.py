"""
OrderService 類別
處理訂單和優惠邏輯
"""


class OrderService:
    """訂單服務類別，處理訂單計算和優惠邏輯"""
    
    def __init__(self):
        """初始化 OrderService"""
        self.threshold_config = None
        self.bogo_cosmetics_enabled = False
    
    def set_threshold_discount(self, threshold, discount):
        """
        設定門檻折扣優惠
        
        Args:
            threshold: 達到此金額門檻才能享有折扣
            discount: 折扣金額
        """
        self.threshold_config = {
            'threshold': threshold,
            'discount': discount
        }
    
    def set_bogo_cosmetics(self, enabled):
        """
        設定化妝品買一送一優惠
        
        Args:
            enabled: 是否啟用買一送一優惠
        """
        self.bogo_cosmetics_enabled = enabled
    
    def calculate_order(self, order_items):
        """
        計算訂單總金額和客戶收到的商品
        
        Args:
            order_items: 訂單項目列表，每個項目包含 productName, quantity, unitPrice, 可選 category
        
        Returns:
            dict: 包含 totalAmount, items 等訂單結果，如果有折扣則包含 originalAmount 和 discount
        """
        # 計算原始總金額和處理 BOGO
        original_amount = 0
        received_items = []
        
        for item in order_items:
            quantity = item['quantity']
            unit_price = item['unitPrice']
            product_name = item['productName']
            category = item.get('category', '')
            
            # 處理 BOGO 優惠（化妝品買一送一）
            if self.bogo_cosmetics_enabled and category == 'cosmetics':
                # 買一送一：買1個送1個，買n個則買n個送1個（只送第一個的）
                # 所以買n個 = 收到 n + 1 個
                received_quantity = quantity + 1
                # 只計算購買的數量，送的免費
                item_total = quantity * unit_price
            else:
                # 沒有優惠，正常計算
                received_quantity = quantity
                item_total = quantity * unit_price
            
            original_amount += item_total
            received_items.append({
                'productName': product_name,
                'quantity': received_quantity
            })
        
        # 計算門檻折扣
        discount = 0
        if self.threshold_config and original_amount >= self.threshold_config['threshold']:
            discount = self.threshold_config['discount']
        
        # 計算最終總金額
        total_amount = original_amount - discount
        
        result = {
            'totalAmount': total_amount,
            'items': received_items
        }
        
        # 如果有折扣，加入原始金額和折扣資訊
        if discount > 0:
            result['originalAmount'] = original_amount
            result['discount'] = discount
        
        return result


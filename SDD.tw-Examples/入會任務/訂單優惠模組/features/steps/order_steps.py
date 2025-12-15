from behave import given, when, then
from src.order_service import OrderService


@given('no promotions are applied')
def step_no_promotions(context):
    """設定沒有任何優惠活動"""
    context.order_service = OrderService()


@given('the threshold discount promotion is configured:')
def step_threshold_discount_configured(context):
    """設定門檻折扣優惠"""
    # 解析門檻折扣配置
    for row in context.table:
        threshold = int(row['threshold'])
        discount = int(row['discount'])
        
        # 建立 OrderService 並配置門檻折扣
        context.order_service = OrderService()
        context.order_service.set_threshold_discount(threshold, discount)


@given('the buy one get one promotion for cosmetics is active')
def step_bogo_cosmetics_active(context):
    """設定化妝品買一送一優惠"""
    # 建立 OrderService 並啟用 BOGO 優惠（目前先不實作，讓測試失敗）
    if not hasattr(context, 'order_service'):
        context.order_service = OrderService()
    context.order_service.set_bogo_cosmetics(True)


@given('同一種商品每買 10 件，則該 10 件同種商品的價格總和會享有 20% 的折扣')
def step_double_eleven_promotion(context):
    """設定雙十一優惠：同一種商品每買 10 件，該 10 件享有 20% 折扣"""
    if not hasattr(context, 'order_service'):
        context.order_service = OrderService()
    context.order_service.set_double_eleven_promotion(True)


@given('購買商品 A, B, C, D, E, F, G, H, I, J 各一件')
def step_buy_ten_different_products(context):
    """設定購買 10 件不同商品的情況，啟用雙十一優惠但確認不適用於不同商品"""
    if not hasattr(context, 'order_service'):
        context.order_service = OrderService()
    # 啟用雙十一優惠，但因為是不同商品，所以不應該享有折扣
    context.order_service.set_double_eleven_promotion(True)


@when('a customer places an order with:')
def step_place_order(context):
    """客戶下訂單"""
    # 解析表格資料
    context.order_items = []
    for row in context.table:
        item = {
            'productName': row['productName'],
            'quantity': int(row['quantity']),
            'unitPrice': int(row['unitPrice'])
        }
        # 如果有 category 欄位，加入 item
        if 'category' in row.headings:
            item['category'] = row['category']
        context.order_items.append(item)
    
    # 呼叫 OrderService 處理訂單
    context.order_result = context.order_service.calculate_order(context.order_items)


@then('the order summary should be:')
def step_check_order_summary(context):
    """檢查訂單摘要"""
    # 解析期望的訂單摘要
    expected_summary = {}
    for row in context.table:
        for key in row.headings:
            expected_summary[key] = int(row[key])
    
    # 檢查訂單結果
    assert context.order_result is not None, "Order result is not set"
    
    # 檢查 totalAmount（所有 scenario 都需要）
    if 'totalAmount' in expected_summary:
        actual_total = context.order_result.get('totalAmount')
        assert actual_total == expected_summary['totalAmount'], \
            f"Expected totalAmount {expected_summary['totalAmount']}, but got {actual_total}"
    
    # 檢查 originalAmount（有折扣的 scenario 需要）
    if 'originalAmount' in expected_summary:
        actual_original = context.order_result.get('originalAmount')
        assert actual_original == expected_summary['originalAmount'], \
            f"Expected originalAmount {expected_summary['originalAmount']}, but got {actual_original}"
    
    # 檢查 discount（有折扣的 scenario 需要）
    if 'discount' in expected_summary:
        actual_discount = context.order_result.get('discount', 0)
        assert actual_discount == expected_summary['discount'], \
            f"Expected discount {expected_summary['discount']}, but got {actual_discount}"


@then('the customer should receive:')
def step_check_customer_receives(context):
    """檢查客戶收到的商品"""
    # 解析期望收到的商品
    expected_items = []
    for row in context.table:
        expected_items.append({
            'productName': row['productName'],
            'quantity': int(row['quantity'])
        })
    
    # 檢查訂單結果
    assert context.order_result is not None, "Order result is not set"
    assert 'items' in context.order_result, "Order result should contain items"
    
    # 將收到的商品轉換為字典以便比較
    received_items_dict = {}
    for item in context.order_result['items']:
        product_name = item['productName']
        if product_name in received_items_dict:
            received_items_dict[product_name] += item['quantity']
        else:
            received_items_dict[product_name] = item['quantity']
    
    # 檢查每個期望的商品
    for expected_item in expected_items:
        product_name = expected_item['productName']
        expected_quantity = expected_item['quantity']
        assert product_name in received_items_dict, \
            f"Expected to receive {product_name}, but it's not in the order result"
        assert received_items_dict[product_name] == expected_quantity, \
            f"Expected {product_name} quantity {expected_quantity}, but got {received_items_dict[product_name]}"


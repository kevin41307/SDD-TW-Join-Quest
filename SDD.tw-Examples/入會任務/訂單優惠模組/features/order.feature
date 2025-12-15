@order_pricing
Feature: E-commerce Order Pricing Promotions
  As a shopper
  I want the system to calculate my order total with applicable promotions
  So that I can understand how much to pay and what items I will receive

  Scenario: Single product without promotions
    Given no promotions are applied
    When a customer places an order with:
      | productName | quantity | unitPrice |
      | T-shirt     | 1        | 500       |
    Then the order summary should be:
      | totalAmount |
      | 500         |
    And the customer should receive:
      | productName | quantity |
      | T-shirt     | 1        |

  Scenario: Threshold discount applies when subtotal reaches 1000
    Given the threshold discount promotion is configured:
      | threshold | discount |
      | 1000      | 100      |
    When a customer places an order with:
      | productName | quantity | unitPrice |
      | T-shirt     | 2        | 500       |
      | 褲子          | 1        | 600       |
    Then the order summary should be:
      | originalAmount | discount | totalAmount |
      | 1600           | 100      | 1500        |
    And the customer should receive:
      | productName | quantity |
      | T-shirt     | 2        |
      | 褲子          | 1        |

  Scenario: Buy-one-get-one for cosmetics - multiple products
    Given the buy one get one promotion for cosmetics is active
    When a customer places an order with:
      | productName | category  | quantity | unitPrice |
      | 口紅          | cosmetics | 1        | 300       |
      | 粉底液         | cosmetics | 1        | 400       |
    Then the order summary should be:
      | totalAmount |
      | 700         |
    And the customer should receive:
      | productName | quantity |
      | 口紅          | 2        |
      | 粉底液         | 2        |

  Scenario: Buy-one-get-one for cosmetics - same product twice
    Given the buy one get one promotion for cosmetics is active
    When a customer places an order with:
      | productName | category  | quantity | unitPrice |
      | 口紅          | cosmetics | 2        | 300       |
    Then the order summary should be:
      | totalAmount |
      | 600         |
    And the customer should receive:
      | productName | quantity |
      | 口紅          | 3        |

  Scenario: Buy-one-get-one for cosmetics - mixed categories
    Given the buy one get one promotion for cosmetics is active
    When a customer places an order with:
      | productName | category  | quantity | unitPrice |
      | 襪子          | apparel   | 1        | 100       |
      | 口紅          | cosmetics | 1        | 300       |
    Then the order summary should be:
      | totalAmount |
      | 400         |
    And the customer should receive:
      | productName | quantity |
      | 襪子          | 1        |
      | 口紅          | 2        |

  Scenario: Multiple promotions stacked
    Given the threshold discount promotion is configured:
      | threshold | discount |
      | 1000      | 100      |
    And the buy one get one promotion for cosmetics is active
    When a customer places an order with:
      | productName | category  | quantity | unitPrice |
      | T-shirt     | apparel   | 3        | 500       |
      | 口紅          | cosmetics | 1        | 300       |
    Then the order summary should be:
      | originalAmount | discount | totalAmount |
      | 1800           | 100      | 1700        |
    And the customer should receive:
      | productName | quantity |
      | T-shirt     | 3        |
      | 口紅          | 2        |
Feature 雙十一優惠

  Scenario: 雙十一優惠 - 購買 12 件相同商品
    Given 同一種商品每買 10 件，則該 10 件同種商品的價格總和會享有 20% 的折扣
    When a customer places an order with:
      | productName | category  | quantity | unitPrice |
      | 襪子          | apparel   | 12        | 100       |
    Then the order summary should be:
      | originalAmount | discount | totalAmount |
      | 1200           | 200      | 1000        |    

  Scenario: 雙十一優惠 - 購買 27 件相同商品
    Given 同一種商品每買 10 件，則該 10 件同種商品的價格總和會享有 20% 的折扣
    When a customer places an order with:
      | productName | category  | quantity | unitPrice |
      | 襪子          | apparel   | 27        | 100       |   
    Then the order summary should be:
      | originalAmount | discount | totalAmount |
      | 2700           | 400      | 2300        |          

  Scenario: 雙十一優惠 - 購買 10 件不同商品
    Given 購買商品 A, B, C, D, E, F, G, H, I, J 各一件 
    When a customer places an order with:
      | productName | category  | quantity | unitPrice |
      | A          | apparel   | 1        | 100       | 
      | B          | apparel   | 1        | 100       | 
      | C          | apparel   | 1        | 100       | 
      | D          | apparel   | 1        | 100       | 
      | E          | apparel   | 1        | 100       | 
      | F          | apparel   | 1        | 100       | 
      | G          | apparel   | 1        | 100       | 
      | H          | apparel   | 1        | 100       | 
      | I          | apparel   | 1        | 100       | 
      | J          | apparel   | 1        | 100       |   
    Then the order summary should be:
      | originalAmount | discount | totalAmount |
      | 1000           | 0      | 1000        |    

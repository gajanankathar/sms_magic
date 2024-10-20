DB = {
    "users": [
        {"id": 1, "name": "Rohit"},
        {"id": 2, "name": "Ashish"},
        {"id": 3, "name": "Suraj"}
    ],
    "products": [
        {"id": 1, "name": "Philips 3 in 1 trimmer"},
        {"id": 2, "name": "Boat neck band"},
        {"id": 3, "name": "JBL GO3"},
        {"id": 4, "name": "Puma Sandal"},
    ],
    "orders": [
        {"id": 1, "orderlines": [{"product_id": 2, "qty": 3}, {"product_id": 4, "qty": 1}], "customer_id": 3},
        {"id": 2, "orderlines": [{"product_id": 2, "qty": 2}], "customer_id": 1},
        {"id": 3, "orderlines": [{"product_id": 1, "qty": 4}, {"product_id": 2, "qty": 1}], "customer_id": 3},
        {"id": 4, "orderlines": [{"product_id": 4, "qty": 2}, {"product_id": 3, "qty": 1}], "customer_id": 2},
    ],
    # In the form of {user_id: [product_ids]}
    "browse_history": {
        1: {4, 2},
        2: {3, 1, 2},
        3: {4, 3, 2, 1}
    },
    # In the form of {user_id: [product_ids]}
    "purchase_history": {
        1: {2},
        2: {4, 3},
        3: {2, 4, 1},
    }
}

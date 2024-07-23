CREATE_TABLE_STORE = """
    CREATE TABLE IF NOT EXISTS online_store
    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
    name VARCHAR(255),
    size VARCHAR(255),
    price VARCHAR(255), 
    productid VARCHAR(255),
    photo TEXT
    )
"""

INSERT_STORE = """
    INSERT INTO online_store(name, size, price, productid, photo)
    VALUES (?, ?, ?, ?, ?)
"""


CREATE_TABLE_PRODUCT_DETAILS = """
    CREATE TABLE IF NOT EXISTS products_detail
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    productid VARCHAR(255),
    category VARCHAR(255),
    infoproduct VARCHAR(255)
    )
"""

INSERT_DETAIL_PRODUCT = """
    INSERT INTO products_detail(productid, category, infoproduct)
    VALUES (?, ?, ?)
"""


GET_PRODUCTS = """
    SELECT * FROM online_store
    INNER JOIN products_detail
    ON online_store.productid = products_detail.productid
"""

GET_PRODUCT_BY_ID = """
    SELECT * FROM online_store 
    INNER JOIN products_detail
    ON online_store.productid = products_detail.productid
    WHERE online_store.id = ?
"""

COUNT_PRODUCTS = """
    SELECT COUNT(*) FROM online_store
"""
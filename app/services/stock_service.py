"""
Stock service
"""
from datetime import datetime
from app.models.stock import Stock
from mongoengine.errors import NotUniqueError, ValidationError
from app.utils.logging_config import logger, log_error, log_stock_change, log_db_operation

import uuid

def create_stock(item_name, amount, price=0):
    """Create a stock"""
    try:
        stock = Stock(product_name=item_name, available_quantity=amount, price=price).save()
        logger.info(f"Stock created | product={item_name} | amount={amount} | price={price} | id={stock.id}")
        log_db_operation("CREATE", "stocks", str(stock.id))
    except NotUniqueError as err:
        logger.warning(f"Duplicate stock creation attempt | product={item_name}")
        return {
            "ok": False,
            "error": "NOT_UNIQUE_ERROR",
            "message": str(err)
        }
    except ValidationError as err:
        log_error("create_stock", err, {"product": item_name})
        return {
            "ok": False,
            "error": "VALIDATION_ERROR",
            "message": str(err)
        }
    except Exception as err:
        log_error("create_stock", err, {"product": item_name})
        return{
            "ok": False,
            "message": str(err)
        }
    return {
        "ok": True,
        "message": f"item: {item_name} added successfully with amount: {amount} and price: {price}"
    }


def get_all_stock():
    """Get all products in stock"""
    try:
        stocks = Stock.objects()
        logger.debug(f"Retrieved all stock | count={len(stocks)}")
        return {
            "ok": True,
            "products": [stock.to_dict() for stock in stocks]
        }
    except Exception as err:
        log_error("get_all_stock", err)
        return {
            "ok": False,
            "message": str(err)
        }


def get_stock_by_id(product_id):
    """Get a specific product by id"""
    try:
        stock = Stock.objects(id=product_id).first()

        if not stock:
            logger.warning(f"Stock not found | product_id={product_id}")
            return {
                "ok": False,
                "error": "NOT_FOUND",
                "message": "Product not found"
            }

        logger.debug(f"Stock retrieved | product_id={product_id}")
        return {
            "ok": True,
            "product": stock.to_dict()
        }
    except Exception as err:
        log_error("get_stock_by_id", err, {"product_id": product_id})
        return {
            "ok": False,
            "message": str(err)
        }


def update_stock(product_id, data):
    """Update a product's stock quantity and/or price"""
    try:
        stock = Stock.objects(id=product_id).first()

        if not stock:
            logger.warning(f"Stock not found for update | product_id={product_id}")
            return {
                "ok": False,
                "error": "NOT_FOUND",
                "message": "Product not found"
            }

        updated_fields = []

        if 'available_quantity' in data:
            old_qty = stock.available_quantity
            stock.available_quantity = data['available_quantity']
            updated_fields.append(f"quantity: {old_qty} -> {data['available_quantity']}")
            log_stock_change(product_id, "UPDATE", data['available_quantity'] - old_qty, stock.available_quantity, stock.reserved_quantity)

        if 'price' in data:
            old_price = stock.price
            stock.price = data['price']
            updated_fields.append(f"price: {old_price} -> {data['price']}")
            logger.info(f"Stock price updated | product_id={product_id} | old_price={old_price} | new_price={data['price']}")

        if updated_fields:
            stock.save()
            logger.info(f"Stock updated | product_id={product_id} | changes: {', '.join(updated_fields)}")

        return {
            "ok": True,
            "message": "Product updated successfully",
            "product": stock.to_dict()
        }
    except Exception as err:
        log_error("update_stock", err, {"product_id": product_id})
        return {
            "ok": False,
            "message": str(err)
        }

def reserve_stock(product_id, amount):
    """
    Reserve stock for a product during checkout.

    Moves quantity from available_quantity to reserved_quantity.
    Called when a cart begins checkout to hold items.

    Args:
        product_id: ID of the product to reserve
        amount: Quantity to reserve
    """
    try:
        logger.info(f"Reserving stock | product_id={product_id} | amount={amount}")
        stock = Stock.objects(id=product_id).first()

        if not stock:
            logger.warning(f"Stock not found for reservation | product_id={product_id}")
            return {
                "ok": False,
                "error": "NOT_FOUND",
                "message": "Product not found"
            }

        if amount<=0:
            logger.warning(f"Invalid reservation amount | product_id={product_id} | amount={amount}")
            return {
                "ok": False,
                "error": "",
                "message": "cannot reserve with 0 or less"
            }

        if stock.available_quantity < amount:
            logger.warning(f"Insufficient stock for reservation | product_id={product_id} | available={stock.available_quantity} | requested={amount}")
            return {
                "ok": False,
                "error": "INSUFFICIENT_STOCK",
                "message": f"Insufficient stock. Available: {stock.available_quantity}, Requested: {amount}"
            }

        stock.available_quantity-=amount
        stock.reserved_quantity+=amount
        stock.save()

        log_stock_change(product_id, "RESERVE", amount, stock.available_quantity, stock.reserved_quantity)
        logger.info(f"Stock reserved successfully | product_id={product_id} | amount={amount} | available={stock.available_quantity} | reserved={stock.reserved_quantity}")

        return {
            "ok": True,
            "message": "Product updated successfully",
            "product": stock.to_dict()
        }
    except Exception as err:
        log_error("reserve_stock", err, {"product_id": product_id, "amount": amount})
        return {
            "ok": False,
            "message": str(err)
        }

def unreserve_stock(product_id, amount):
    """
    Release reserved stock back to available.

    Moves quantity from reserved_quantity back to available_quantity.
    Called when a transaction fails or cart item is removed.

    Args:
        product_id: ID of the product to unreserve
        amount: Quantity to release back to available
    """
    try:
        logger.info(f"Unreserving stock | product_id={product_id} | amount={amount}")
        stock = Stock.objects(id=product_id).first()

        if not stock:
            logger.warning(f"Stock not found for unreserve | product_id={product_id}")
            return {
                "ok": False,
                "error": "NOT_FOUND",
                "message": "Product not found"
            }

        if amount<=0:
            logger.warning(f"Invalid unreserve amount | product_id={product_id} | amount={amount}")
            return {
                "ok": False,
                "error": "",
                "message": "cannot unreserve with 0 or less"
            }
        if stock.reserved_quantity < amount:
            logger.warning(f"Cannot unreserve more than reserved | product_id={product_id} | reserved={stock.reserved_quantity} | requested={amount}")
            return {
                "ok": False,
                "error": "",
                "message": "cannot unreserve more than reserved"
            }

        stock.available_quantity+=amount
        stock.reserved_quantity-=amount
        stock.save()

        log_stock_change(product_id, "UNRESERVE", amount, stock.available_quantity, stock.reserved_quantity)
        logger.info(f"Stock unreserved successfully | product_id={product_id} | amount={amount} | available={stock.available_quantity} | reserved={stock.reserved_quantity}")

        return {
            "ok": True,
            "message": "Product updated successfully",
            "product": stock.to_dict()
        }
    except Exception as err:
        log_error("unreserve_stock", err, {"product_id": product_id, "amount": amount})
        return {
            "ok": False,
            "message": str(err)
        }

def delete_stock(product_id):
    """Delete a product from stock"""
    try:
        stock = Stock.objects(id=product_id).first()

        if not stock:
            logger.warning(f"Stock not found for deletion | product_id={product_id}")
            return {
                "ok": False,
                "error": "NOT_FOUND",
                "message": "Product not found"
            }

        product_name = stock.product_name
        stock.delete()
        logger.info(f"Stock deleted | product_id={product_id} | product_name={product_name}")
        log_db_operation("DELETE", "stocks", product_id)

        return {
            "ok": True,
            "message": "Product deleted successfully"
        }
    except Exception as err:
        log_error("delete_stock", err, {"product_id": product_id})
        return {
            "ok": False,
            "message": str(err)
        }



# Finalizing stock purchases after successful transaction
def finalise_stock_purchase(product_id, amount):
    """
    Finalize a stock purchase after successful transaction.

    Deducts the amount from reserved_quantity (not available_quantity)
    since items were already reserved during checkout.
    Called when a transaction is completed successfully.

    Args:
        product_id: ID of the product purchased
        amount: Quantity that was purchased
    """
    try:
        logger.info(f"Finalizing stock purchase | product_id={product_id} | amount={amount}")
        stock = Stock.objects(id=product_id).first()

        if not stock:
            logger.warning(f"Stock not found for finalization | product_id={product_id}")
            return {
                "ok": False,
                "error": "NOT_FOUND",
                "message": "Product not found"
            }

        if stock.reserved_quantity<amount:
            logger.error(f"Finalize amount exceeds reserved | product_id={product_id} | reserved={stock.reserved_quantity} | amount={amount}")
            return {
                "ok": False,
                "message": "finalised amount doesn't match reserved stock"
            }
        stock.reserved_quantity=stock.reserved_quantity - amount

        stock.save()

        log_stock_change(product_id, "FINALIZE_PURCHASE", amount, stock.available_quantity, stock.reserved_quantity)
        logger.info(f"Stock purchase finalized | product_id={product_id} | amount={amount} | remaining_reserved={stock.reserved_quantity}")

        return {
            "ok": True,
            "message": "Stock purchase finalized successfully"
        }
    except Exception as err:
        log_error("finalise_stock_purchase", err, {"product_id": product_id, "amount": amount})
        return {
            "ok": False,
            "message": str(err)
        }


def add_stock(product_id, amount):
    """Add stock for a product (used for refunds)"""
    try:
        logger.info(f"Adding stock | product_id={product_id} | amount={amount}")
        stock = Stock.objects(id=product_id).first()

        if not stock:
            logger.warning(f"Stock not found for adding stock | product_id={product_id}")
            return {
                "ok": False,
                "error": "NOT_FOUND",
                "message": "Product not found"
            }

        if amount<=0:
            logger.warning(f"Invalid add stock amount | product_id={product_id} | amount={amount}")
            return {
                "ok": False,
                "error": "",
                "message": "cannot add 0 or less stock"
            }

        old_qty = stock.available_quantity
        stock.available_quantity+=amount
        stock.save()

        log_stock_change(product_id, "ADD_STOCK", amount, stock.available_quantity, stock.reserved_quantity)
        logger.info(f"Stock added successfully | product_id={product_id} | amount={amount} | available: {old_qty} -> {stock.available_quantity}")

        return {
            "ok": True,
            "message": "Stock added successfully",
            "product": stock.to_dict()
        }
    except Exception as err:
        log_error("add_stock", err, {"product_id": product_id, "amount": amount})
        return {
            "ok": False,
            "message": str(err)
        }
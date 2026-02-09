from celery import Celery
from mongoengine import connect
import os
import logging
from dotenv import load_dotenv
load_dotenv()

# Set up logging for Celery worker
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | stock_worker | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger('stock_worker')

celery = Celery(
    'stock',
    broker=f"redis://{os.getenv('CELERY_BROKER_HOST', 'localhost')}:{os.getenv('CELERY_BROKER_PORT', 6379)}/0",
    backend=f"redis://{os.getenv('CELERY_BROKER_HOST', 'localhost')}:{os.getenv('CELERY_BROKER_PORT', 6379)}/0",
    # include=['stock.unreserve_stock','stock.reserve_stock', 'stock.finalise_stock_purchase','transaction.create','cart.completeCheckout','cart.unfreeze'],
)
celery.conf.task_routes = {
    'transaction.*': {'queue': 'transaction_queue'},
    'cart.*': {'queue': 'cart_queue'},
    'stock.*': {'queue': 'stock_queue'},
}
celery.autodiscover_tasks()


# Initialize MongoDB connection
connect(
    db=os.getenv('MONGODB_DB', 'devopsshowcase'),
    username=os.getenv('MONGODB_USERNAME'),
    password=os.getenv('MONGODB_PASSWORD'),
    host=os.getenv('MONGODB_HOST', 'localhost'),
    port=int(os.getenv('MONGODB_PORT', 27017)),
    authentication_source=os.getenv('MONGODB_AUTH_SOURCE', 'devopsshowcase')
)
logger.info(f"Stock Celery worker connected to MongoDB")

from app.services.stock_service import reserve_stock
@celery.task(name="stock.reserve_stock")
def reserve_stock_task(product_id, amount):
    """
    Reserve stock for a product during checkout.

    Called by cart service when checkout is initiated.
    """
    logger.info(f"TASK RECEIVED | stock.reserve_stock | product_id={product_id} | amount={amount}")

    result = reserve_stock(product_id, amount)
    if result.get("ok"):
        logger.info(f"TASK SUCCESS | stock.reserve_stock | product_id={product_id} | amount={amount}")
    else:
        logger.error(f"TASK FAILED | stock.reserve_stock | product_id={product_id} | error={result.get('message')}")
    return result


from app.services.stock_service import unreserve_stock
@celery.task(name="stock.unreserve_stock")
def unreserve_stock_task(product_id, amount):
    """
    Unreserve stock for a product.

    Called by cart service if transaction fails and stock needs to be restored.
    """
    logger.info(f"TASK RECEIVED | stock.unreserve_stock | product_id={product_id} | amount={amount}")
    result = unreserve_stock(product_id, amount)
    if result.get("ok"):
        logger.info(f"TASK SUCCESS | stock.unreserve_stock | product_id={product_id} | amount={amount}")
    else:
        logger.error(f"TASK FAILED | stock.unreserve_stock | product_id={product_id} | error={result.get('message')}")
    return result


from app.services.stock_service import finalise_stock_purchase
@celery.task(name="stock.finalise_stock_purchase")
def finalise_stock_purchase_task(product_id, amount):
    """
    Finalize a stock purchase after successful transaction.

    Called by cart service when transaction is completed.
    """
    logger.info(f"TASK RECEIVED | stock.finalise_stock_purchase | product_id={product_id} | amount={amount}")
    result = finalise_stock_purchase(product_id, amount)
    if result.get("ok"):
        logger.info(f"TASK SUCCESS | stock.finalise_stock_purchase | product_id={product_id} | amount={amount}")
    else:
        logger.error(f"TASK FAILED | stock.finalise_stock_purchase | product_id={product_id} | error={result.get('message')}")
    return result

from app.services.stock_service import add_stock
@celery.task(name="stock.add_stock")
def add_stock_task(product_id, amount):
    """
    Add stock for a product.

    Called by cart service when a refund is processed.
    """
    logger.info(f"TASK RECEIVED | stock.add_stock | product_id={product_id} | amount={amount}")
    result = add_stock(product_id, amount)
    if result.get("ok"):
        logger.info(f"TASK SUCCESS | stock.add_stock | product_id={product_id} | amount={amount}")
    else:
        logger.error(f"TASK FAILED | stock.add_stock | product_id={product_id} | error={result.get('message')}")
    return result
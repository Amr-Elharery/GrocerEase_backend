from fastapi import Depends, HTTPException, status
from app.modules.orders.infrastructure.orders_repository_supabase import OrdersRepositorySupabase
from app.modules.addresses.application.services.addresses_service import AddressesService
from app.modules.shops.infrastructure.shops_repository_supabase import ShopsRepositorySupabase
from app.modules.shop_products.infrastructure.shop_products_repository_supabase import ShopProductsRepositorySupabase
from app.modules.notifications.application.services.notifications_service import NotificationsService
from app.modules.auth.infrastructure.auth_repository_supabase import AuthRepositorySupabase

DELIVERY_FEE = 25.00


class OrdersService:
    def __init__(
        self,
        repository: OrdersRepositorySupabase = Depends(OrdersRepositorySupabase),
        addresses_service: AddressesService = Depends(AddressesService),
        shops_repository: ShopsRepositorySupabase = Depends(ShopsRepositorySupabase),
        shop_products_repository: ShopProductsRepositorySupabase = Depends(ShopProductsRepositorySupabase),
        notifications_service: NotificationsService = Depends(NotificationsService),
        auth_repository: AuthRepositorySupabase = Depends(AuthRepositorySupabase),
    ) -> None:
        self.repository = repository
        self.addresses_service = addresses_service
        self.shops_repository = shops_repository
        self.shop_products_repository = shop_products_repository
        self.notifications_service = notifications_service
        self.auth_repository = auth_repository

    async def get_all_orders(self, customer_id: str, limit: int = 10, offset: int = 0):
        try:
            return await self.repository.get_all_orders(customer_id, limit, offset)
        except Exception as e:
            raise e

    async def get_order(self, order_id: int, current_user: dict):
        try:
            order = await self.repository.get_order(order_id)
            if not order:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

            roles = current_user.get("roles", [])
            user_id = current_user.get("id")

            if "admin" in roles:
                return order
            elif "vendor" in roles:
                shop = await self.shops_repository.get_shop_by_owner(user_id)
                if not shop or order.get("shop_id") != shop["id"]:
                    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="This order does not belong to your shop")
            else:
                if order.get("customer_id") != user_id:
                    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not the owner of this order")

            return order
        except Exception as e:
            raise e

    async def create_order(self, payload, customer_id: str):
        try:
            active_order = await self.repository.get_active_order_for_customer(customer_id)
            if active_order:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You already have an active order. Wait until it is delivered or completed before placing a new one.")

            await self.addresses_service.get_address(payload.customer_address_id, customer_id)

            subtotal, items_to_insert = await self._validate_and_calculate(payload.items, payload.shop_id)

            order_data = {
                "customer_id": customer_id,
                "shop_id": payload.shop_id,
                "customer_address_id": payload.customer_address_id,
                "payment_method": payload.payment_method,
                "status": "pending",
                "subtotal": subtotal,
                "delivery_fee": DELIVERY_FEE,
                "order_group_id": None,
            }

            order = await self.repository.create_order(order_data)

            for item in items_to_insert:
                item["order_id"] = order["id"]
            await self.repository.create_order_items(items_to_insert)

            for item in items_to_insert:
                await self.shop_products_repository.decrement_stock(item["shop_product_id"], item["quantity"])

            await self._notify_delivery_users(order["id"])

            return await self.repository.get_order(order["id"])
        except Exception as e:
            raise e

    async def create_optimization_order(self, payload, customer_id: str):
        try:
            active_order = await self.repository.get_active_order_for_customer(customer_id)
            if active_order:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You already have an active order. Wait until it is delivered or completed before placing a new one.")

            await self.addresses_service.get_address(payload.customer_address_id, customer_id)

            order_group = await self.repository.create_order_group(customer_id)
            order_group_id = order_group["id"]

            created_orders = []
            for order_payload in payload.orders:
                subtotal, items_to_insert = await self._validate_and_calculate(order_payload.items, order_payload.shop_id)

                order_data = {
                    "customer_id": customer_id,
                    "shop_id": order_payload.shop_id,
                    "customer_address_id": payload.customer_address_id,
                    "payment_method": payload.payment_method,
                    "status": "pending",
                    "subtotal": subtotal,
                    "delivery_fee": DELIVERY_FEE,
                    "order_group_id": order_group_id,
                }

                order = await self.repository.create_order(order_data)

                for item in items_to_insert:
                    item["order_id"] = order["id"]
                await self.repository.create_order_items(items_to_insert)

                for item in items_to_insert:
                    await self.shop_products_repository.decrement_stock(item["shop_product_id"], item["quantity"])

                created_orders.append(order)

            for created_order in created_orders:
                await self._notify_delivery_users(created_order["id"])

            return await self.repository.get_order_group(order_group_id)
        except Exception as e:
            raise e

    async def cancel_order(self, order_id: int, customer_id: str):
        try:
            order = await self.repository.get_order(order_id)
            if not order:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
            if order.get("customer_id") != customer_id:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not the owner of this order")
            if order.get("status") != "pending":
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only pending orders can be cancelled")
            return await self.repository.update_order_status(order_id, "cancelled")
        except Exception as e:
            raise e

    async def update_order_status(self, order_id: int, new_status: str):
        try:
            order = await self.repository.get_order(order_id)
            if not order:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
            return await self.repository.update_order_status(order_id, new_status)
        except Exception as e:
            raise e

    async def get_order_group(self, order_group_id: int, customer_id: str):
        try:
            group = await self.repository.get_order_group(order_group_id)
            if not group:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order group not found")
            if group.get("customer_id") != customer_id:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not the owner of this order group")
            return group
        except Exception as e:
            raise e

    async def get_all_orders_admin(self, limit: int = 10, offset: int = 0):
        return await self.repository.get_all_orders_admin(limit, offset)

    async def get_shop_orders(self, owner_id: str, limit: int = 10, offset: int = 0):
        shop = await self.shops_repository.get_shop_by_owner(owner_id)
        if not shop:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You do not have a shop")
        return await self.repository.get_orders_by_shop(shop["id"], limit, offset)

    async def _notify_delivery_users(self, order_id: int):
        try:
            delivery_user_ids = await self.auth_repository.get_users_by_role("delivery")
            for user_id in delivery_user_ids:
                try:
                    await self.notifications_service.send_to_user(
                        user_id=user_id,
                        title="New Order Available",
                        body="A new order is available for pickup. Open the app to accept it.",
                        data={"order_id": order_id},
                    )
                except Exception:
                    pass
        except Exception:
            pass

    async def _validate_and_calculate(self, items, shop_id: int):
        items_to_insert = []
        subtotal = 0.0

        for item in items:
            shop_product = await self.repository.get_shop_product(item.shop_product_id)
            if not shop_product:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Shop product {item.shop_product_id} not found")
            if not shop_product.get("is_active"):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Shop product {item.shop_product_id} is not available")
            if shop_product.get("shop_id") != shop_id:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Shop product {item.shop_product_id} does not belong to shop {shop_id}")
            if shop_product.get("available_stock") is not None and item.quantity > shop_product["available_stock"]:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Insufficient stock for product {item.shop_product_id}")

            item_total = shop_product["price"] * item.quantity
            subtotal += item_total
            items_to_insert.append({
                "shop_product_id": item.shop_product_id,
                "quantity": item.quantity,
                "total": item_total,
            })

        return subtotal, items_to_insert

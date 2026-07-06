from supabase import AsyncClient
from fastapi import Depends
from app.db.supabase_client import get_admin_client


class OrdersRepositorySupabase:
    def __init__(self, admin_client: AsyncClient = Depends(get_admin_client)) -> None:
        self.client = admin_client

    async def get_all_orders(self, customer_id: str, limit: int = 10, offset: int = 0):
        try:
            response = await self.client.from_("orders").select("""
                id,
                customer_id,
                shop_id,
                order_group_id,
                status,
                subtotal,
                delivery_fee,
                payment_method,
                created_at,
                customer_address_id,
                order_items (
                    id,
                    shop_product_id,
                    quantity,
                    total
                )
            """).eq("customer_id", customer_id).order("created_at", desc=True).range(offset, offset + limit - 1).execute()
            return response.data
        except Exception as e:
            print(f"Error fetching orders: {e}")
            raise e

    async def get_order(self, order_id: int):
        try:
            response = await self.client.from_("orders").select("""
                id,
                customer_id,
                shop_id,
                order_group_id,
                status,
                subtotal,
                delivery_fee,
                payment_method,
                created_at,
                customer_address_id,
                order_items (
                    id,
                    shop_product_id,
                    quantity,
                    total
                )
            """).eq("id", order_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error fetching order: {e}")
            raise e

    async def get_order_for_delivery(self, order_id: int):
        try:
            response = await self.client.from_("orders").select("""
                id,
                customer_id,
                shop_id,
                order_group_id,
                status,
                subtotal,
                delivery_fee,
                payment_method,
                created_at,
                order_items (
                    id,
                    shop_product_id,
                    quantity,
                    total
                ),
                customer_address:customer_address_id (
                    id,
                    street,
                    building,
                    floor,
                    apt_number,
                    latitude,
                    longitude,
                    additional_directions,
                    label,
                    area:area_id (
                        id,
                        area_name,
                        city_name
                    )
                ),
                shop:shop_id (
                    id,
                    shop_name,
                    address,
                    latitude,
                    longitude,
                    phone_number
                )
            """).eq("id", order_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error fetching order for delivery: {e}")
            raise e

    async def create_order(self, payload: dict):
        try:
            response = await self.client.from_("orders").insert(payload).execute()
            if response.data:
                return await self.get_order(response.data[0]["id"])
            return None
        except Exception as e:
            print(f"Error creating order: {e}")
            raise e

    async def create_order_items(self, items: list[dict]):
        try:
            response = await self.client.from_("order_items").insert(items).execute()
            return response.data
        except Exception as e:
            print(f"Error creating order items: {e}")
            raise e

    async def update_order_status(self, order_id: int, status: str):
        try:
            response = await self.client.from_("orders").update({"status": status}).eq("id", order_id).execute()
            if response.data:
                return await self.get_order(order_id)
            return None
        except Exception as e:
            print(f"Error updating order status: {e}")
            raise e

    async def create_order_group(self, customer_id: str):
        try:
            response = await self.client.from_("order_group").insert({"customer_id": customer_id}).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error creating order group: {e}")
            raise e

    async def get_order_group(self, order_group_id: int):
        try:
            response = await self.client.from_("order_group").select("""
                id,
                customer_id,
                created_at,
                orders (
                    id,
                    customer_id,
                    shop_id,
                    order_group_id,
                    status,
                    subtotal,
                    delivery_fee,
                    payment_method,
                    created_at,
                    customer_address_id,
                    order_items (
                        id,
                        shop_product_id,
                        quantity,
                        total
                    )
                )
            """).eq("id", order_group_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error fetching order group: {e}")
            raise e

    async def get_available_orders_for_delivery(self, limit: int = 10, offset: int = 0):
        try:
            response = await self.client.from_("orders").select("""
                id,
                customer_id,
                shop_id,
                order_group_id,
                status,
                subtotal,
                delivery_fee,
                payment_method,
                created_at,
                customer_address_id,
                order_items (
                    id,
                    shop_product_id,
                    quantity,
                    total
                ),
                customer_address:customer_address_id (
                    id,
                    street,
                    building,
                    floor,
                    apt_number,
                    latitude,
                    longitude,
                    label,
                    area:area_id (
                        id,
                        area_name,
                        city_name
                    )
                ),
                shop:shop_id (
                    id,
                    shop_name,
                    address,
                    latitude,
                    longitude,
                    phone_number
                )
            """).eq("status", "pending").order("created_at", desc=True).range(offset, offset + limit - 1).execute()
            return response.data
        except Exception as e:
            print(f"Error fetching available orders: {e}")
            raise e

    async def get_all_orders_admin(self, limit: int = 10, offset: int = 0):
        try:
            response = await self.client.from_("orders").select("""
                id,
                shop_id,
                order_group_id,
                status,
                subtotal,
                delivery_fee,
                payment_method,
                created_at,
                customer_address_id,
                order_items (
                    id,
                    shop_product_id,
                    quantity,
                    total
                ),
                customer_name:customer_id (
                    full_name
                )
            """).order("created_at", desc=True).range(offset, offset + limit - 1).execute()
            return response.data
        except Exception as e:
            print(f"Error fetching all orders: {e}")
            raise e

    async def get_orders_by_shop(self, shop_id: int, limit: int = 10, offset: int = 0):
        try:
            response = await self.client.from_("orders").select("""
                id,
                shop_id,
                order_group_id,
                status,
                subtotal,
                delivery_fee,
                payment_method,
                created_at,
                customer_address_id,
                order_items (
                    id,
                    shop_product_id,
                    quantity,
                    total
                ),
                customer_name:customer_id (
                    full_name
                )
            """).eq("shop_id", shop_id).order("created_at", desc=True).range(offset, offset + limit - 1).execute()
            return response.data
        except Exception as e:
            print(f"Error fetching shop orders: {e}")
            raise e

    async def get_active_order_for_customer(self, customer_id: str):
        try:
            response = await self.client.from_("orders").select("id, status").eq("customer_id", customer_id).not_.in_("status", ["delivered", "cancelled"]).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error checking active order: {e}")
            raise e

    async def get_shop_product(self, shop_product_id: int):
        try:
            response = await self.client.from_("shop_product").select("id, price, available_stock, shop_id, is_active").eq("id", shop_product_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error fetching shop product: {e}")
            raise e

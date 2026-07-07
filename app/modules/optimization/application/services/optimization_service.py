from fastapi import Depends
from app.modules.shops.infrastructure.shops_repository_supabase import ShopsRepositorySupabase
from app.modules.shop_products.infrastructure.shop_products_repository_supabase import ShopProductsRepositorySupabase
from app.modules.addresses.application.services.addresses_service import AddressesService
from app.modules.optimization.domain.optimizer import find_optimal_trip
from app.modules.optimization.domain.errors import NoValidRouteError


class OptimizationService:
    def __init__(
        self,
        shops_repository: ShopsRepositorySupabase = Depends(ShopsRepositorySupabase),
        shop_products_repository: ShopProductsRepositorySupabase = Depends(ShopProductsRepositorySupabase),
        addresses_service: AddressesService = Depends(AddressesService),
    ) -> None:
        self.shops_repository = shops_repository
        self.shop_products_repository = shop_products_repository
        self.addresses_service = addresses_service

    async def optimize_trip(
        self,
        shopping_list: dict,
        customer_address_id: int,
        customer_id: str,
        max_stores: int = 3,
    ) -> dict:
        address = await self.addresses_service.get_address(customer_address_id, customer_id)
        area_id = address.get("area_id")
        customer_coords = (address["latitude"], address["longitude"])

        shops = await self.shops_repository.get_all_shops(limit=1000, area_id=area_id)
        if not shops:
            raise NoValidRouteError()

        shops = [s for s in shops if s.get("latitude") and s.get("longitude")]
        if not shops:
            raise NoValidRouteError()

        shop_ids = [s["id"] for s in shops]
        products = await self.shop_products_repository.get_products_for_shops(shop_ids)

        store_locations = {s["shop_name"]: (s["latitude"], s["longitude"]) for s in shops}
        shop_id_to_name = {s["id"]: s["shop_name"] for s in shops}
        shop_name_to_id = {s["shop_name"]: s["id"] for s in shops}

        
        catalog: dict[str, dict] = {s["shop_name"]: {} for s in shops}
        id_lookup: dict[tuple, int] = {}
        for row in products:
            name = shop_id_to_name.get(row["shop_id"])
            if name:
                product_id = row["product_id"]
                catalog[name][product_id] = row["price"]
                id_lookup[(name, product_id)] = row["id"]

        result = find_optimal_trip(
            shopping_list=shopping_list,
            catalog=catalog,
            store_locations=store_locations,
            customer=customer_coords,
            max_stores=max_stores,
        )

        if result is None:
            raise NoValidRouteError()

        for product_id, assignment in result["item_assignment"].items():
            store_name = assignment["store"]
            assignment["shop_id"] = shop_name_to_id[store_name]
            assignment["shop_product_id"] = id_lookup.get((store_name, product_id))

        return result

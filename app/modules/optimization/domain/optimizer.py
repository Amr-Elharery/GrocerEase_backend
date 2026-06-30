from itertools import combinations, permutations
import openrouteservice
from app.core.config import settings

COST_PER_KM = 2.5
PER_STOP_COST = 15

_ors_client = openrouteservice.Client(key=settings.ORS_API_KEY)


def _build_matrix(locations: list) -> list:
    coords = [(lon, lat) for lat, lon in locations]
    response = _ors_client.distance_matrix(
        locations=coords,
        profile="driving-car",
        metrics=["distance"],
        units="m",
    )
    return response["distances"]


def _best_route(stop_indices: list, matrix: list, customer: int) -> tuple:
    best_path, best_dist = None, float("inf")
    for order in permutations(stop_indices):
        path = [*order, customer]
        dist = sum(matrix[path[k]][path[k + 1]] for k in range(len(path) - 1))
        if dist < best_dist:
            best_dist, best_path = dist, path
    return best_path, best_dist


def calculate_delivery_cost(distance_meters: int, num_stops: int) -> float:
    return distance_meters / 1000 * COST_PER_KM + num_stops * PER_STOP_COST


def find_optimal_trip(
    shopping_list: dict,
    catalog: dict,
    store_locations: dict,
    customer: tuple,
    max_stores: int = 3,
) -> dict | None:
    store_names = list(catalog.keys())

    all_points = [store_locations[s] for s in store_names] + [customer]
    all_names  = store_names + ["Customer"]
    full_matrix = _build_matrix(all_points)

    customer_idx = len(all_points) - 1
    store_idx = {name: i for i, name in enumerate(store_names)}

    best = None

    for num_stores in range(1, max_stores + 1):
        for subset in combinations(store_names, num_stores):

            item_assignment = {}
            all_covered = True
            for item, qty in shopping_list.items():
                cheapest_price, cheapest_store = None, None
                for store in subset:
                    if item in catalog.get(store, {}):
                        price = catalog[store][item] * qty
                        if cheapest_price is None or price < cheapest_price:
                            cheapest_price, cheapest_store = price, store
                if cheapest_store is None:
                    all_covered = False
                    break
                item_assignment[item] = {"store": cheapest_store, "price": round(cheapest_price, 2)}

            if not all_covered:
                continue

            item_cost = sum(v["price"] for v in item_assignment.values())

            subset_indices = [store_idx[s] for s in subset]
            best_path, best_dist = _best_route(subset_indices, full_matrix, customer_idx)

            legs = []
            for k in range(len(best_path) - 1):
                a, b = best_path[k], best_path[k + 1]
                legs.append({
                    "from": all_names[a],
                    "to": all_names[b],
                    "distance_km": round(full_matrix[a][b] / 1000, 2),
                })

            num_stops = len(best_path) - 1
            delivery_cost = round(calculate_delivery_cost(best_dist, num_stops), 2)
            total_cost    = round(item_cost + delivery_cost, 2)

            route_result = {
                "route": [all_names[i] for i in best_path],
                "route_indices": best_path,
                "legs": legs,
                "total_distance_meters": best_dist,
                "total_distance_km": round(best_dist / 1000, 2),
                "estimated_cost": delivery_cost,
                "num_stops": num_stops,
            }

            if best is None or total_cost < best["total_cost"]:
                best = {
                    "stores_to_visit": list(subset),
                    "item_assignment": item_assignment,
                    "item_cost": round(item_cost, 2),
                    "delivery_cost": delivery_cost,
                    "total_cost": total_cost,
                    "route": route_result,
                }

    return best

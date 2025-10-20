import requests
from collections import defaultdict

API_BASE = "https://d30r5p5favh3z8.cloudfront.net"
USERNAME = "brickfan35"

def get_json(url):
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()

def get_user_inventory(username):
    user_summary = get_json(f"{API_BASE}/api/user/by-username/{username}")
    user_id = user_summary["id"]
    user_data = get_json(f"{API_BASE}/api/user/by-id/{user_id}")
    # Collection: list of pieces with variants (colors and counts)
    inventory = defaultdict(int)
    for piece in user_data["collection"]:
        piece_id = piece["pieceId"]
        for variant in piece["variants"]:
            color_id = variant["color"]
            count = variant["count"]
            key = (piece_id, color_id)
            inventory[key] += count
    return inventory

def get_all_sets():
    sets_response = get_json(f"{API_BASE}/api/sets")
    return sets_response["Sets"]

def get_set_requirements(set_id):
    set_data = get_json(f"{API_BASE}/api/set/by-id/{set_id}")
    # Requirements: list of pieces with part info and quantity
    requirements = defaultdict(int)
    for item in set_data["pieces"]:
        piece_id = item["part"]["designID"]
        color_id = str(item["part"]["material"])  # Convert to string to match collection format
        quantity = item["quantity"]
        key = (piece_id, color_id)
        requirements[key] += quantity
    return requirements, set_data["name"]

def can_build_set(inventory, requirements):
    for key, needed in requirements.items():
        if inventory.get(key, 0) < needed:
            return False
    return True

def main():
    print(f"Checking which sets {USERNAME} can build...")
    inventory = get_user_inventory(USERNAME)
    sets = get_all_sets()
    buildable = []
    
    print(f"User has {sum(inventory.values())} total pieces across {len(inventory)} unique piece/color combinations")
    print(f"Checking {len(sets)} available sets...\n")
    
    for s in sets:
        set_id = s["id"]
        requirements, set_name = get_set_requirements(set_id)
        if can_build_set(inventory, requirements):
            buildable.append((set_name, s["totalPieces"]))
    
    print(f"Sets that can be built ({len(buildable)} out of {len(sets)}):")
    for name, total_pieces in sorted(buildable, key=lambda x: x[1]):
        print(f"- {name} ({total_pieces} pieces)")

if __name__ == "__main__":
    main()
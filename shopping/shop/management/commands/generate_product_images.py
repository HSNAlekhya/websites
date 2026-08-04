import json
import urllib.parse
import urllib.request
from django.core.management.base import BaseCommand
from shop.models import Product  # adjust import

PEXELS_API_KEY = "qhBVPpQP57ZGGn7nEHH8fPLwXKnckHwtbOuQxIxZcz4cpOkVuKDkL5z4"

CATEGORY_SEARCH_TERMS = {
    "kurti": "indian kurti woman fashion",
    "dress": "party dress woman fashion",
    "top": "casual top woman fashion",
    "skirt": "elegant skirt woman fashion",
    "festive set": "ethnic wear set woman fashion",
    "shirt": "men shirt fashion",
    "jacket": "men casual jacket fashion",
    "trousers": "men formal trousers fashion",
    "polo": "men polo shirt fashion",
    "hoodie": "men hoodie fashion",
    "bag": "fashion handbag accessory",
    "sunglasses": "fashion sunglasses accessory",
    "necklace": "fashion necklace jewelry",
    "wallet": "leather wallet accessory",
    "scarf": "silk scarf fashion accessory",
    "play set": "kids playing set",
    "tee": "kids printed tshirt",
    "soft jacket": "kids soft jacket",
    "romper": "baby romper clothing",
    "mini dress": "kids mini dress",
    "frock": "kids party frock",
    "jogger": "kids jogger set clothing",
    "cap": "kids sun cap fashion",
    "shorts": "kids shorts clothing",
}
DEFAULT_SEARCH = "women fashion clothing"


class Command(BaseCommand):
    help = "Assign free real photos to products using Pexels (no cost, no installs)"

    def fetch_json(self, url):
        req = urllib.request.Request(url, headers={
            "Authorization": PEXELS_API_KEY, 
            "User-Agent": "Mozilla/5.0"
        })
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read())

    def download_image(self, url):
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as response:
            return response.read()

    def handle(self, *args, **kwargs):
        # Pre-fetch a pool of image URLs per category (only 5 API calls total)
        image_pools = {}
        for keyword, query in CATEGORY_SEARCH_TERMS.items():
            self.stdout.write(f"Fetching photos for '{query}'...")
            url = f"https://api.pexels.com/v1/search?query={urllib.parse.quote(query)}&per_page=21"
            try:
                data = self.fetch_json(url)
                image_pools[keyword] = [p["src"]["large"] for p in data.get("photos", [])]
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Failed fetching '{query}': {e}"))
                image_pools[keyword] = []

        products = Product.objects.all()
        assigned = 0

        for product in products:
            name_lower = product.name.lower()
            matched_keyword = next((k for k in CATEGORY_SEARCH_TERMS if k in name_lower), None)
            pool = image_pools.get(matched_keyword, [])

            if not pool:
                self.stdout.write(self.style.WARNING(f"No images found for {product.name}, skipping"))
                continue

            product.image_url = pool[assigned % len(pool)]   # ← just store the URL string
            product.save(update_fields=['image_url'])
            assigned += 1
            self.stdout.write(self.style.SUCCESS(f"Assigned image to {product.name}"))
            
        self.stdout.write(self.style.SUCCESS(f"\nDone! Assigned images to {assigned} products."))
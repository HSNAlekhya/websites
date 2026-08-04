import os

images = {
    "kurti": ("https://images.openai.com/thumbnails/url/fWpL-XicDcltCoIwAADQE02jjJUQoZZWopKbWr9E5_xC3WwTq9t0rG5T7-_7fmopudBVlQ7k8eKSFkDmw0qphMxkQxTCelXUjPNmqPbj7n-64Rdbh4RpCwmQCERXEs2BjbgI5vdkoaN_qzYAumNpQg2ItruYGsTQq4bQSfr2yaY-z7FnneJmLtEBx_S-plpjM4H7PDCiLC2DuFskPDSXLj2LHwtBOZQ"),
    "lehenga": ("#f472b6", "Lehenga"),
    "saree": ("#fb7185", "Saree"),
    "skirt": ("#fda4af", "Skirt"),
    "dress": ("#fbbf24", "Dress"),
    "jacket": ("#60a5fa", "Jacket"),
    "hoodie": ("#818cf8", "Hoodie"),
    "coat": ("#38bdf8", "Coat"),
    "bag": ("#fcd34d", "Bag"),
    "shirt": ("#93c5fd", "Shirt"),
    "trousers": ("#a5b4fc", "Trousers"),
    "top": ("#c4b5fd", "Top"),
    "kids": ("#fdba74", "Kids"),
    "womens": ("#f9a8d4", "Womens"),
    "mens": ("#93c5fd", "Mens"),
    "accessories": ("#fcd34d", "Accessories"),
    "default": ("#e5e7eb", "StyleHub"),
}

out_dir = os.path.join("shop", "static", "shop", "images")
os.makedirs(out_dir, exist_ok=True)

svg_template = '''<svg xmlns="http://www.w3.org/2000/svg" width="400" height="400">
  <rect width="100%" height="100%" fill="{color}"/>
  <text x="50%" y="50%" text-anchor="middle" dominant-baseline="middle" font-family="Arial" font-size="32" fill="#1f2937">{label}</text>
</svg>'''

for key, (color, label) in images.items():
    path = os.path.join(out_dir, f"{key}.svg")
    with open(path, "w") as f:
        f.write(svg_template.format(color=color, label=label))
    print(f"Created {path}")

print(f"\nDone — {len(images)} images created in {out_dir}")
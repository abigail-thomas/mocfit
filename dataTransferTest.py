import json

with open("mydata.json") as f1, open("teammate.json") as f2:
    data1 = json.load(f1)
    data2 = json.load(f2)

# optional: handle duplicates (by model + pk)
seen = set()
merged = []
for obj in data1 + data2:
    key = (obj["model"], obj["pk"])
    if key not in seen:
        seen.add(key)
        merged.append(obj)

with open("combined.json", "w") as out:
    json.dump(merged, out, indent=2)

print("Merged data saved to combined.json")

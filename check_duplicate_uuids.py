import csv
from collections import defaultdict
import os

# Files to check
concept_files = [
    'configuration/backend_configuration/concepts/master_new_concepts.csv',
    'configuration/backend_configuration/concepts/HC_non-ESV-ICD-11-diagnosis_concepts.csv',
    'configuration/backend_configuration/concepts/HC_diagnosis_concept.csv',
    'configuration/backend_configuration/concepts/queue_service_concepts.csv',
    'configuration/backend_configuration/concepts/patient_transfer_note.csv'
]

uuid_tracker = defaultdict(list)

# Read all UUIDs from all files
for filepath in concept_files:
    if not os.path.exists(filepath):
        print(f"⚠️  File not found: {filepath}")
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row_num, row in enumerate(reader, start=2):
            # Try common UUID column names
            uuid = row.get('Uuid') or row.get('uuid') or row.get('UUID')
            if uuid and uuid.strip():
                uuid_tracker[uuid.strip()].append({
                    'file': os.path.basename(filepath),
                    'row': row_num,
                    'name': row.get('Fully specified name') or row.get('name') or 'N/A'
                })

# Find duplicates
duplicates = {uuid: locations for uuid, locations in uuid_tracker.items() if len(locations) > 1}

if duplicates:
    print(f"🚨 Found {len(duplicates)} duplicate UUID(s):\n")
    for uuid, locations in duplicates.items():
        print(f"UUID: {uuid}")
        for loc in locations:
            print(f"  - {loc['file']} (row {loc['row']}): {loc['name']}")
        print()
else:
    print("✅ No duplicate UUIDs found!")

print(f"\nTotal UUIDs checked: {len(uuid_tracker)}")

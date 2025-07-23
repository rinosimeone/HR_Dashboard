import csv
import pandas as pd

def validate_csv_structure(filename):
    """Validate CSV file structure and check for parsing issues."""
    print(f"🔍 Validating CSV file: {filename}")
    
    # First, let's check line by line for field count consistency
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    # Get expected field count from header
    header_fields = len(lines[0].strip().split(','))
    print(f"📊 Expected fields per line: {header_fields}")
    
    issues_found = []
    
    for i, line in enumerate(lines[1:], start=2):  # Skip header, start counting from line 2
        field_count = len(line.strip().split(','))
        if field_count != header_fields:
            issues_found.append((i, field_count, line.strip()))
    
    if issues_found:
        print(f"❌ Found {len(issues_found)} lines with incorrect field count:")
        for line_num, field_count, line_content in issues_found:
            print(f"   Line {line_num}: {field_count} fields - {line_content[:100]}...")
        return False
    else:
        print("✅ All lines have correct field count")
    
    # Now try to load with pandas
    try:
        df = pd.read_csv(filename)
        print(f"✅ Successfully loaded CSV with pandas")
        print(f"📈 Dataset shape: {df.shape[0]} rows, {df.shape[1]} columns")
        print(f"📋 Columns: {list(df.columns)}")
        return True
    except Exception as e:
        print(f"❌ Pandas loading failed: {str(e)}")
        return False

if __name__ == "__main__":
    validate_csv_structure("hr_data.csv")

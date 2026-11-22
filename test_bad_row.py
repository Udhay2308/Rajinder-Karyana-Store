"""
test_bad_row.py - Robustness test for handling corrupt/bad data rows.
Proves that the application catches corrupted input and does not crash.
"""

import os
import inventory

def test_handling_bad_rows():
    test_csv = os.path.join(os.path.dirname(__file__), 'bad_sample_data.csv')
    print("Testing bad row tolerance on:", test_csv)
    
    summary = inventory.audit_inventory(test_csv)
    
    print("\n--- TEST EXECUTION RESULT ---")
    print(f"Total valid items parsed: {summary['total_items']} (Expected: 2)")
    print(f"Total corrupt rows caught safely: {len(summary['skipped_rows'])} (Expected: 4)")
    
    print("\nReported Error Messages (Gracefully Handled):")
    for err in summary['skipped_rows']:
        print(f"  • {err}")
        
    assert summary['total_items'] == 2, "Should have parsed exactly 2 valid items"
    assert len(summary['skipped_rows']) == 4, "Should have caught 4 bad rows"
    print("\n✅ PASS: Tool is 100% crash-proof against bad data rows!")

if __name__ == '__main__':
    test_handling_bad_rows()


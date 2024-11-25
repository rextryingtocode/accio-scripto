import os
from lxml import etree

# Paths to the input and output directories
input_folder = r" " #insert path
output_folder = r" " #insert path

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Item ID to search for and the new price
target_item_id = "52501-022-03"
new_price = "63.2"

# Iterate over all XML files in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith(".xml"):  # Process only XML files
        file_path = os.path.join(input_folder, filename)
        try:
            # Parse the XML file with lxml
            tree = etree.parse(file_path)
            root = tree.getroot()

            # Define namespaces
            namespaces = {
                'cbc': "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
                'cac': "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2"
            }

            # Find all <cac:Item> elements
            items = root.xpath(".//cac:Item", namespaces=namespaces)
            modified = False

            for item in items:
                # Find the <cbc:ID> element within <cac:SellersItemIdentification>
                item_id = item.xpath(".//cac:SellersItemIdentification/cbc:ID", namespaces=namespaces)
                if item_id and item_id[0].text == target_item_id:
                    # Find the <cbc:PriceAmount> element within <cac:Price> and update its value
                    price_element = item.xpath("../cac:Price/cbc:PriceAmount", namespaces=namespaces)
                    if price_element:
                        price_element[0].text = new_price
                        modified = True

            if modified:
                # Save the modified XML to the output folder
                output_file_path = os.path.join(output_folder, filename)
                tree.write(output_file_path, encoding="utf-8", pretty_print=True, xml_declaration=True)
                print(f"Modified and saved: {filename}")
            else:
                print(f"No changes made to: {filename}")

        except Exception as e:
            print(f"Error processing {filename}: {e}")

print("Processing complete. Check the output folder for modified files.")

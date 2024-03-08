#продолжите решение здесь
import xml.etree.ElementTree as ET
tree = ET.parse('inventory.xml')
root = tree.getroot()
total = 0
for item in root.findall('./ценности/предмет'):
    total += int(item.find('ценность').text) * int(item.find('количество').text)
print(total)
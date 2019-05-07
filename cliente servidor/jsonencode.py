import base64
import json

with open("escher.jpg", 'rb') as open_file:
    byte_content = open_file.read()
    base64_bytes = base64.b64encode(byte_content)
    base64_string = base64_bytes.decode('utf-8')

    raw_data = {'file': base64_string, 'file name': 'escher.jpg'}
    json_data = json.dumps(raw_data, indent=2)

    with open("escher.json", 'w') as output:
        output.write(json_data)


with open("escher.json", 'r') as input:
    new_json_data = json.load(input)
    fstring = new_json_data['file']
    fbytes = base64.b64decode(fstring)
    with open("escher2.jpg", 'wb') as output:
        output.write(fbytes)

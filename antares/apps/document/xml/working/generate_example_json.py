#!/Users/leobelen/.virtualenvs/antares/bin/python

from datetime import datetime
import json

if __name__ == "__main__":
    file = {}
    general = {}
    documents = []
    document = {}
    general["type"] = "uploaded_file"
    general["author"] = "leobelen"
    general["creation_date"] = str(datetime.now())
    document["anAmount"] = 100
    document["aPeriod"] = 201010
    documents.append(document)
    file['general'] = general
    file['documents'] = documents
    json_string = json.dumps(file)
    print(json_string)

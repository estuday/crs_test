import requests

url = "http://172.31.99.9:8011/test"

payload = {"property": "name"}
files = [
    (
        "file",
        (
            "/data/external/资源/课程资源(V2.0版本)/智能语音/讲义/IS-1.1-B-语音产生的声学理论.docx",
            open(
                "/data/external/资源/课程资源(V2.0版本)/智能语音/讲义/IS-1.1-B-语音产生的声学理论.docx",
                "rb",
            ),
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ),
    )
]
from dto import CRSDocumentExtractRequest

request = CRSDocumentExtractRequest(property="name", type_constraint="str")

response = requests.request("POST", url, data=request, files=files)

print(response.text)

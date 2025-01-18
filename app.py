import os
import roboflow
from dotenv import load_dotenv

# init Roboflow
load_dotenv('.env.api.local')
API_KEY = os.getenv('ROBOFLOW_KEY')
PROJECT_NAME = "your_project_name"
MODEL_VERSION = "gui-detection-uz7l4/1"

roboflow.login()
rf = roboflow.Roboflow(api_key=API_KEY)

# APIエンドポイント
url = f"https://detect.roboflow.com/{PROJECT_NAME}/{MODEL_VERSION}?api_key={API_KEY}"

# 画像を読み込み
image_path = "./assets/G1.jpg"
with open(image_path, "rb") as image_file:
    image_data = image_file.read()

# リクエスト送信
response = requests.post(url, files={"file": image_data})

# 結果を取得
if response.status_code == 200:
    predictions = response.json()["predictions"]
    for prediction in predictions:
        print(f"Label: {prediction['class']}, Confidence: {prediction['confidence']}")
else:
    print("Error:", response.status_code, response.text)








"""
# create a project
rf.create_project(
    project_name="project name",
    project_type="project-type",
    license="project-license" # "private" for private projects
)

workspace = rf.workspace("WORKSPACE_URL")
project = workspace.project("PROJECT_URL")
version = project.version("VERSION_NUMBER")

# upload a dataset
workspace.upload_dataset(
    dataset_path="./dataset/",
    num_workers=10,
    dataset_format="yolov8", # supports yolov8, yolov5, and Pascal VOC
    project_license="MIT",
    project_type="object-detection"
)

# upload model weights
version.deploy(model_type="yolov8", model_path=f”{HOME}/runs/detect/train/”)

# upload model weights - yolov10
# Before attempting to upload YOLOv10 models install ultralytics like this:
# pip install git+https://github.com/THU-MIG/yolov10.git
version.deploy(model_type="yolov10", model_path=f”{HOME}/runs/detect/train/”, filename="weights.pt")

# run inference
model = version.model

img_url = "https://media.roboflow.com/quickstart/aerial_drone.jpeg"

predictions = model.predict(img_url, hosted=True).json()

print(predictions)
"""
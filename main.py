from fastapi import FastAPI, UploadFile, File
import face_recognition

app = FastAPI()

@app.get("/health")
def health_check():
    # SRE 必備：提供給負載均衡器確認服務是否存活
    return {"status": "it's testing"}

@app.post("/face-detect")
async def detect_face(file: UploadFile = File(...)):
    image = face_recognition.load_image_file(file.file)
    face_locations = face_recognition.face_locations(image)
    return {"face_count": len(face_locations), "locations": face_locations}
#hello
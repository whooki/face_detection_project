1. Clone the Repository
bash
Skopiuj kod
git clone https://github.com/your-username/face-detection-system.git
cd face-detection-system

2. Set Up a Virtual Environment
bash
Skopiuj kod
python -m venv face_detection_env

Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned

Windows:
bash
Skopiuj kod
face_detection_env\Scripts\activate

macOS/Linux:
bash
Skopiuj kod
source face_detection_env/bin/activate

3. Install Dependencies
bash
Skopiuj kod
pip install -r requirements.txt

4. Run the Backend Server
Navigate to the server/ directory:

bash
Skopiuj kod
cd server
uvicorn main:app --reload
The server will start at http://localhost:8000

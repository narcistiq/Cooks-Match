# Cooks-Match

A receipt-to-recipe generator that uses Python's EasyOCR library to extract ingredients from grocery receipts and generates personalized recipes using Google Gemini.

## 📋 Prerequisites

Make sure you have the following installed on your system:

- **Python 3.8+**
- **Node.js 16+** 
- **npm** as the package manager
- **MongoDB** (for recipe storage)

Before running, please make sure to download the [MongoDB Community Server](https://www.mongodb.com/try/download/community) and [Node.js](https://nodejs.org/en/download).

## 🚀 Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/narcistiq/FoodTracker.git
cd Cooks-Match
```

### 2. Backend Setup

#### Navigate to Backend Directory
```bash
cd receipt-recipes/backend
```

#### Create a Python virtual environment and activate
```bash
python3 -m venv venv

source venv/bin/activate (Mac/Linux)
venv\Scripts\Activate.ps1(Windows)
```

#### Install Python Dependencies
```bash
pip3 install -r requirements.txt
```

#### Environment Configuration
Create `.env` file with your Gemini API key at project root:

**Backend configuration:**
```bash
GEMINI_API_KEY=your_gemini_api_key_here
```

#### Start the Backend Server
```bash
uvicorn main:app --reload --port 8000
```

The backend will be available at: `http://127.0.0.1:8000`

### 3. Frontend Setup

#### Navigate to Frontend Directory (in a new terminal)
```bash
cd receipt-recipes/frontend
```

#### Install Node Dependencies
```bash
npm install
```

#### Start the Frontend Development Server
```bash
npm run dev
```

The frontend will be available at: `http://localhost:5173`

## 🧪 Testing

1. **Backend API**: Visit `http://127.0.0.1:8000/docs` for FastAPI interactive documentation
2. **Upload Test**: Use the frontend to upload a receipt image
3. **Example Files**: Test with images in `receipt-recipes/backend/uploads/`
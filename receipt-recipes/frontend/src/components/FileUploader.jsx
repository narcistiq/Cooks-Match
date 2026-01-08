import { useRef, useState } from 'react';
import './FileUploader.css';
import RecipeDisplay from './RecipeDisplay';

const UploadStatus = {
    IDLE: 'idle',
    UPLOADING: 'uploading',
    SUCCESS: 'success',
    ERROR: 'error',
};

export default function FileUploader() {
    const [file, setFile] = useState(null);
    const [status, setStatus] = useState(UploadStatus.IDLE);
    const [recipes, setRecipes] = useState(null);
    const fileInputRef = useRef();

    function handleFileChange(e) {
        if (e.target.files) {
            setFile(e.target.files[0]);
        }
    }

    const handleFileUpload = () => {
        setStatus(UploadStatus.UPLOADING);
        setRecipes(null); // Clear previous recipes
        
        const formData = new FormData();
        formData.append("file", file, file.name);
        const requestOptions = {
            method: 'POST',
            body: formData,
        };
        
        fetch('http://127.0.0.1:8000/uploads/', requestOptions)
            .then(response => response.json())
            .then(function(response) {
                console.log('Recipes received:', response);
                setRecipes(response);
                setStatus(UploadStatus.SUCCESS);
            })
            .catch(error => {
                console.error('Upload error:', error);
                setStatus(UploadStatus.ERROR);
            });
    };

    function handleButtonClick() {
        fileInputRef.current.click();
    }

    return (
        <div className="flex flex-col items-center justify-center min-h-screen w-full p-8 space-y-12">
            <h1 className="text-3xl font-bold text-gray-800 mb-16 text-center w-full">Receipt Recipe</h1>
            <div className="flex flex-col items-center space-y-12 max-w-md mx-auto text-center">

            <input 
                type="file" 
                ref={fileInputRef} 
                onChange={handleFileChange} 
                style={{ display: "none" }}
            />

                {file && (
                    <div className="uploads-section rounded-lg bg-white p-6 shadow-md w-full max-w-sm text-center mb-24">
                        <p className="font-semibold">File name: {file.name}</p>
                        <p>Size: {(file.size / 1024).toFixed(2)} KB</p>
                        <p>Type: {file.type}</p>
                    </div>
                )}

                <button 
                    className="upload-btn w-full max-w-xs mt-20 mb-24" 
                    onClick={handleButtonClick}
                >
                    {file ? `Selected: ${file.name}` : "Choose File"}
                </button>

                {file && status !== UploadStatus.UPLOADING && (
                    <button className="w-full max-w-xs mt-32" onClick={handleFileUpload}>
                        {status === UploadStatus.UPLOADING ? 'Processing...' : 'Upload & Generate Recipes'}
                    </button>
                )}

                {status === UploadStatus.UPLOADING && (
                    <div className="loading-container mt-8">
                        <div className="loading-spinner"></div>
                        <p className="text-lg font-semibold text-gray-700">Processing your receipt...</p>
                    </div>
                )}

                {status === UploadStatus.SUCCESS && recipes && (
                    <p style={{ color: '#16a34a', textAlign: 'center'}} className="text-sm font-semibold mt-8">
                        Recipes generated successfully!
                    </p>
                )}
                {status === UploadStatus.ERROR && (
                    <p style={{ color: '#ff2929ff', textAlign: 'center'}} className="text-sm font-semibold mt-8">
                        Upload Failed. Please try again.
                    </p>
                )}
            </div>
            
            {recipes && <RecipeDisplay recipes={recipes} />}
        </div>
    );
}

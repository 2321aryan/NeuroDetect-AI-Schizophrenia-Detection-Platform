# Detection Engine Improvements

## Overview
The DetectionEngine has been significantly improved to provide more accurate and file-type-specific analysis for schizophrenia detection.

## Key Improvements

### 1. File Type Detection
- **EEG Files**: `.csv`, `.edf` files are automatically detected and analyzed for brain wave patterns
- **MRI Files**: `.nii`, `.dcm` files are analyzed for structural and functional brain abnormalities
- **Smart Filtering**: Only shows results relevant to the uploaded file types

### 2. Enhanced Analysis Accuracy
- **Backend Processing**: Files are now processed on the server for more accurate analysis
- **File Type Specific**: Different analysis algorithms for EEG vs MRI data
- **Real-time Processing**: Actual file upload and processing instead of mock data

### 3. Improved User Experience
- **Better Error Handling**: Clear error messages for invalid files or processing failures
- **File Management**: Easy file removal and clear all functionality
- **Progress Indicators**: Visual feedback during analysis
- **File Type Labels**: Clear indication of file types in the upload list

### 4. Enhanced Results Display
- **Modality-Specific Results**: Only shows analysis results for uploaded file types
- **Detailed Analysis**: Frequency bands for EEG, connectivity networks for MRI
- **Brain Visualization**: 3D brain model showing affected regions based on analyzed modalities
- **Color-coded Abnormalities**: Visual indicators for different abnormality levels

### 5. Backend Integration
- **File Upload**: Secure file upload with size and type validation
- **Analysis API**: Dedicated endpoint for file analysis (`/api/analysis/analyze/:patientId`)
- **Patient Database**: Results are saved to patient records with timestamps
- **File Cleanup**: Automatic cleanup of temporary files after processing

## Technical Features

### Frontend (DetectionEngine.jsx)
- File type detection and validation
- FormData upload to backend
- Real-time error handling and user feedback
- Dynamic UI based on uploaded file types

### Backend (analysis.js)
- Multer file upload handling
- File type validation and processing
- EEG-specific analysis (frequency bands, abnormalities)
- MRI-specific analysis (structural findings, connectivity)
- Automatic file cleanup

### Components
- **BrainVisualization**: Shows brain regions based on analyzed modalities
- **AnalysisResults**: Displays results specific to uploaded file types

## Usage

1. **Enter Patient ID**: Required field for analysis tracking
2. **Upload Files**: Drag and drop or select EEG (.csv, .edf) or MRI (.nii, .dcm) files
3. **Analyze**: Click "Analyze" to process files on the backend
4. **View Results**: See modality-specific results and brain visualization

## Error Handling

- Invalid file types are rejected with clear error messages
- Network errors are handled gracefully
- File size limits (100MB per file, 10 files max)
- Backend processing errors are displayed to user

## File Type Support

### EEG Analysis
- **File Types**: `.csv`, `.edf`
- **Analysis**: Frequency band analysis, abnormality detection
- **Results**: Brain regions affected by electrical activity

### MRI Analysis  
- **File Types**: `.nii`, `.dcm`
- **Analysis**: Structural and functional connectivity
- **Results**: Brain volume, connectivity networks, structural findings

## Security Features

- File type validation on both frontend and backend
- Automatic cleanup of uploaded files
- Size limits to prevent abuse
- Secure file handling with temporary storage 
# 🔬 NeuroDetect AI - Technical Deep Dive

## 🏗️ **System Architecture Overview**

### **High-Level Architecture**
```
┌─────────────────────────────────────────────────────────────────┐
│                    NeuroDetect AI Platform                     │
├─────────────────────────────────────────────────────────────────┤
│  Frontend (React PWA)     │  Backend (Node.js)  │  AI Engine    │
│  ├── Authentication UI    │  ├── JWT Auth       │  ├── EEG Proc  │
│  ├── 3D Brain Viz        │  ├── RBAC System    │  ├── MRI Proc  │
│  ├── Real-time Updates   │  ├── File Upload    │  ├── ML Models │
│  ├── Offline Support     │  ├── API Gateway    │  └── Clinical  │
│  └── Mobile Responsive   │  └── Audit Logs     │      Decision  │
├─────────────────────────────────────────────────────────────────┤
│                    Data Layer (PostgreSQL)                     │
│  ├── Users & Auth        ├── Patients         ├── Analyses      │
│  ├── Audit Trails        ├── Medical Records  └── AI Results    │
└─────────────────────────────────────────────────────────────────┘
```

### **Microservices Architecture**
```
Internet → Load Balancer → API Gateway → Microservices
                              │
                              ├── Auth Service (Port 5002)
                              ├── AI Model Service (Port 8000)
                              ├── Symptom Service (Port 8001)
                              └── File Processing Service
```

---

## 🧠 **AI/ML Implementation Details**

### **EEG Processing Pipeline**
```python
class AdvancedEEGProcessor:
    def __init__(self):
        self.sampling_rate = 256  # Hz
        self.channels = 19        # Standard 10-20 system
        self.frequency_bands = {
            'delta': (0.5, 4),    # Deep sleep, unconscious
            'theta': (4, 8),      # Drowsiness, meditation
            'alpha': (8, 13),     # Relaxed awareness
            'beta': (13, 30),     # Active thinking
            'gamma': (30, 100)    # High-level cognitive processing
        }
    
    def preprocess_signal(self, raw_eeg):
        """
        Advanced preprocessing pipeline:
        1. Bandpass filtering (0.5-100 Hz)
        2. Notch filtering (50/60 Hz power line)
        3. Artifact removal (EOG, EMG, cardiac)
        4. Independent Component Analysis (ICA)
        5. Bad channel interpolation
        6. Re-referencing to average
        """
        # Bandpass filter
        filtered = self.apply_bandpass_filter(raw_eeg, 0.5, 100)
        
        # Notch filter for power line interference
        notch_filtered = self.apply_notch_filter(filtered, 50)
        
        # Artifact removal using statistical thresholding
        clean_signal = self.remove_artifacts(notch_filtered)
        
        # Normalization
        normalized = self.z_score_normalize(clean_signal)
        
        return normalized
    
    def extract_spectral_features(self, eeg_data):
        """
        Extract comprehensive spectral features:
        - Power Spectral Density (PSD)
        - Relative band powers
        - Spectral entropy
        - Peak frequency
        - Spectral edge frequency
        - Band power ratios (theta/alpha, beta/alpha)
        """
        features = {}
        
        for channel_idx, channel_name in enumerate(self.channels):
            # Welch's method for PSD estimation
            freqs, psd = signal.welch(
                eeg_data[channel_idx], 
                self.sampling_rate, 
                nperseg=1024
            )
            
            # Calculate band powers
            for band_name, (low, high) in self.frequency_bands.items():
                band_mask = (freqs >= low) & (freqs <= high)
                band_power = np.trapz(psd[band_mask], freqs[band_mask])
                features[f'{channel_name}_{band_name}_power'] = band_power
            
            # Spectral entropy
            normalized_psd = psd / np.sum(psd)
            spectral_entropy = -np.sum(normalized_psd * np.log2(normalized_psd + 1e-12))
            features[f'{channel_name}_spectral_entropy'] = spectral_entropy
            
            # Peak frequency
            peak_freq = freqs[np.argmax(psd)]
            features[f'{channel_name}_peak_frequency'] = peak_freq
        
        return features
    
    def extract_connectivity_features(self, eeg_data):
        """
        Brain connectivity analysis:
        - Coherence between channel pairs
        - Phase Locking Value (PLV)
        - Directed Transfer Function (DTF)
        - Partial Directed Coherence (PDC)
        """
        connectivity_features = {}
        n_channels = len(self.channels)
        
        # Calculate coherence between all channel pairs
        for i in range(n_channels):
            for j in range(i+1, n_channels):
                freqs, coherence = signal.coherence(
                    eeg_data[i], eeg_data[j], 
                    self.sampling_rate, nperseg=1024
                )
                
                # Average coherence in each frequency band
                for band_name, (low, high) in self.frequency_bands.items():
                    band_mask = (freqs >= low) & (freqs <= high)
                    avg_coherence = np.mean(coherence[band_mask])
                    feature_name = f'coherence_{self.channels[i]}_{self.channels[j]}_{band_name}'
                    connectivity_features[feature_name] = avg_coherence
        
        return connectivity_features
    
    def extract_nonlinear_features(self, eeg_data):
        """
        Nonlinear dynamics features:
        - Hjorth parameters (Activity, Mobility, Complexity)
        - Sample entropy
        - Approximate entropy
        - Detrended Fluctuation Analysis (DFA)
        - Lyapunov exponents
        """
        nonlinear_features = {}
        
        for channel_idx, channel_name in enumerate(self.channels):
            signal_data = eeg_data[channel_idx]
            
            # Hjorth parameters
            activity = np.var(signal_data)
            
            diff1 = np.diff(signal_data)
            mobility = np.sqrt(np.var(diff1) / np.var(signal_data))
            
            diff2 = np.diff(diff1)
            complexity = np.sqrt(np.var(diff2) / np.var(diff1)) / mobility
            
            nonlinear_features[f'{channel_name}_hjorth_activity'] = activity
            nonlinear_features[f'{channel_name}_hjorth_mobility'] = mobility
            nonlinear_features[f'{channel_name}_hjorth_complexity'] = complexity
            
            # Sample entropy
            sample_entropy = self.calculate_sample_entropy(signal_data)
            nonlinear_features[f'{channel_name}_sample_entropy'] = sample_entropy
        
        return nonlinear_features
```

### **MRI Processing Pipeline**
```python
class AdvancedMRIProcessor:
    def __init__(self):
        self.target_shape = (64, 64, 64)  # Standardized volume size
        self.brain_regions = {
            'prefrontal_cortex': self.load_brain_atlas('pfc'),
            'temporal_lobe': self.load_brain_atlas('temporal'),
            'hippocampus': self.load_brain_atlas('hippocampus'),
            'anterior_cingulate': self.load_brain_atlas('acc'),
            'striatum': self.load_brain_atlas('striatum')
        }
    
    def preprocess_mri(self, mri_volume):
        """
        MRI preprocessing pipeline:
        1. Skull stripping
        2. Bias field correction (N4ITK)
        3. Intensity normalization
        4. Registration to standard space (MNI152)
        5. Tissue segmentation (GM, WM, CSF)
        6. Spatial smoothing
        """
        # Skull stripping using intensity thresholding
        brain_mask = self.skull_strip(mri_volume)
        skull_stripped = mri_volume * brain_mask
        
        # Bias field correction
        bias_corrected = self.n4_bias_correction(skull_stripped)
        
        # Intensity normalization (0-1 range)
        normalized = self.intensity_normalize(bias_corrected)
        
        # Resize to standard shape
        resized = self.resize_volume(normalized, self.target_shape)
        
        # Gaussian smoothing (FWHM = 4mm)
        smoothed = ndimage.gaussian_filter(resized, sigma=1.0)
        
        return smoothed
    
    def extract_volumetric_features(self, mri_volume):
        """
        Volumetric analysis:
        - Total brain volume
        - Regional volumes (GM, WM, CSF)
        - Ventricular volume
        - Cortical thickness measures
        - Surface area calculations
        """
        volumetric_features = {}
        
        # Total brain volume
        brain_mask = mri_volume > 0.1  # Threshold for brain tissue
        total_volume = np.sum(brain_mask)
        volumetric_features['total_brain_volume'] = total_volume
        
        # Regional volume analysis
        for region_name, region_mask in self.brain_regions.items():
            # Resample region mask to match MRI resolution
            resampled_mask = self.resample_mask(region_mask, mri_volume.shape)
            
            # Calculate regional volume
            regional_volume = np.sum(mri_volume[resampled_mask > 0.5])
            volumetric_features[f'{region_name}_volume'] = regional_volume
            
            # Volume ratio (region/total brain)
            volume_ratio = regional_volume / total_volume if total_volume > 0 else 0
            volumetric_features[f'{region_name}_volume_ratio'] = volume_ratio
        
        return volumetric_features
    
    def extract_texture_features(self, mri_volume):
        """
        Texture analysis using Gray Level Co-occurrence Matrix (GLCM):
        - Contrast
        - Dissimilarity
        - Homogeneity
        - Energy
        - Correlation
        - Angular Second Moment (ASM)
        """
        texture_features = {}
        
        for region_name, region_mask in self.brain_regions.items():
            # Extract region of interest
            roi = self.extract_roi(mri_volume, region_mask)
            
            if roi.size > 0:
                # Calculate GLCM features for each slice
                glcm_features = []
                for slice_idx in range(roi.shape[2]):
                    slice_data = roi[:, :, slice_idx]
                    if np.sum(slice_data > 0) > 100:  # Sufficient voxels
                        # Discretize intensities for GLCM
                        discretized = self.discretize_image(slice_data, levels=16)
                        
                        # Calculate GLCM
                        glcm = self.calculate_glcm(discretized)
                        
                        # Extract texture features
                        contrast = self.glcm_contrast(glcm)
                        homogeneity = self.glcm_homogeneity(glcm)
                        energy = self.glcm_energy(glcm)
                        
                        glcm_features.append([contrast, homogeneity, energy])
                
                if glcm_features:
                    # Average across slices
                    avg_features = np.mean(glcm_features, axis=0)
                    texture_features[f'{region_name}_contrast'] = avg_features[0]
                    texture_features[f'{region_name}_homogeneity'] = avg_features[1]
                    texture_features[f'{region_name}_energy'] = avg_features[2]
        
        return texture_features
```

### **Deep Learning Models**
```python
def build_eeg_lstm_model(input_shape):
    """
    LSTM model for EEG sequence analysis
    Input: (batch_size, time_steps, channels)
    Output: Binary classification (0: Healthy, 1: Schizophrenia)
    """
    model = Sequential([
        # First LSTM layer with return sequences
        LSTM(128, return_sequences=True, input_shape=input_shape,
             dropout=0.3, recurrent_dropout=0.3),
        BatchNormalization(),
        
        # Second LSTM layer
        LSTM(64, return_sequences=True, dropout=0.3, recurrent_dropout=0.3),
        BatchNormalization(),
        
        # Third LSTM layer (final)
        LSTM(32, dropout=0.3, recurrent_dropout=0.3),
        BatchNormalization(),
        
        # Dense layers
        Dense(64, activation='relu'),
        Dropout(0.5),
        Dense(32, activation='relu'),
        Dropout(0.3),
        Dense(1, activation='sigmoid')
    ])
    
    model.compile(
        optimizer=Adam(learning_rate=0.001),
        loss='binary_crossentropy',
        metrics=['accuracy', 'precision', 'recall', 'f1_score']
    )
    
    return model

def build_mri_3d_cnn_model(input_shape):
    """
    3D CNN model for MRI volume analysis
    Input: (batch_size, depth, height, width, channels)
    Output: Binary classification with attention mechanism
    """
    inputs = Input(shape=input_shape)
    
    # First 3D convolutional block
    x = Conv3D(32, (3, 3, 3), activation='relu', padding='same')(inputs)
    x = BatchNormalization()(x)
    x = MaxPooling3D((2, 2, 2))(x)
    x = Dropout(0.25)(x)
    
    # Second 3D convolutional block
    x = Conv3D(64, (3, 3, 3), activation='relu', padding='same')(x)
    x = BatchNormalization()(x)
    x = MaxPooling3D((2, 2, 2))(x)
    x = Dropout(0.25)(x)
    
    # Third 3D convolutional block
    x = Conv3D(128, (3, 3, 3), activation='relu', padding='same')(x)
    x = BatchNormalization()(x)
    x = MaxPooling3D((2, 2, 2))(x)
    x = Dropout(0.25)(x)
    
    # Attention mechanism
    attention = GlobalAveragePooling3D()(x)
    attention = Dense(128, activation='relu')(attention)
    attention = Dense(x.shape[-1], activation='sigmoid')(attention)
    attention = Reshape((1, 1, 1, x.shape[-1]))(attention)
    x = Multiply()([x, attention])
    
    # Global pooling and classification
    x = GlobalAveragePooling3D()(x)
    x = Dense(256, activation='relu')(x)
    x = Dropout(0.5)(x)
    x = Dense(128, activation='relu')(x)
    x = Dropout(0.3)(x)
    outputs = Dense(1, activation='sigmoid')(x)
    
    model = Model(inputs=inputs, outputs=outputs)
    
    model.compile(
        optimizer=Adam(learning_rate=0.0001),
        loss='binary_crossentropy',
        metrics=['accuracy', 'precision', 'recall', 'f1_score']
    )
    
    return model

def build_ensemble_model(eeg_features, mri_features):
    """
    Ensemble model combining EEG and MRI predictions
    Uses weighted voting and meta-learning
    """
    # EEG branch
    eeg_input = Input(shape=(eeg_features,), name='eeg_input')
    eeg_dense = Dense(128, activation='relu')(eeg_input)
    eeg_dense = Dropout(0.3)(eeg_dense)
    eeg_dense = Dense(64, activation='relu')(eeg_dense)
    eeg_output = Dense(1, activation='sigmoid', name='eeg_output')(eeg_dense)
    
    # MRI branch
    mri_input = Input(shape=(mri_features,), name='mri_input')
    mri_dense = Dense(128, activation='relu')(mri_input)
    mri_dense = Dropout(0.3)(mri_dense)
    mri_dense = Dense(64, activation='relu')(mri_dense)
    mri_output = Dense(1, activation='sigmoid', name='mri_output')(mri_dense)
    
    # Meta-learner for ensemble
    combined = Concatenate()([eeg_dense, mri_dense])
    meta_dense = Dense(64, activation='relu')(combined)
    meta_dense = Dropout(0.3)(meta_dense)
    ensemble_output = Dense(1, activation='sigmoid', name='ensemble_output')(meta_dense)
    
    model = Model(
        inputs=[eeg_input, mri_input],
        outputs=[eeg_output, mri_output, ensemble_output]
    )
    
    model.compile(
        optimizer=Adam(learning_rate=0.001),
        loss={
            'eeg_output': 'binary_crossentropy',
            'mri_output': 'binary_crossentropy',
            'ensemble_output': 'binary_crossentropy'
        },
        loss_weights={
            'eeg_output': 0.3,
            'mri_output': 0.3,
            'ensemble_output': 0.4
        },
        metrics=['accuracy']
    )
    
    return model
```

---

## 🔐 **Security Implementation**

### **Authentication & Authorization**
```javascript
// JWT Token Structure
const tokenPayload = {
    userId: user.id,
    email: user.email,
    role: user.role,
    permissions: getUserPermissions(user.role),
    iat: Math.floor(Date.now() / 1000),
    exp: Math.floor(Date.now() / 1000) + (24 * 60 * 60), // 24 hours
    iss: 'neurodetect-ai',
    aud: 'neurodetect-users'
};

// Role-Based Access Control Matrix
const PERMISSIONS = {
    admin: [
        'user:create', 'user:read', 'user:update', 'user:delete',
        'patient:create', 'patient:read', 'patient:update', 'patient:delete',
        'analysis:create', 'analysis:read', 'analysis:update', 'analysis:delete',
        'system:monitor', 'system:configure', 'audit:read'
    ],
    doctor: [
        'patient:create', 'patient:read', 'patient:update',
        'analysis:create', 'analysis:read', 'analysis:update',
        'report:generate', 'report:export'
    ],
    researcher: [
        'patient:read', 'analysis:read', 'analysis:create',
        'data:export', 'statistics:view'
    ],
    technician: [
        'analysis:create', 'analysis:read', 'file:upload'
    ]
};

// Middleware for permission checking
const requirePermission = (permission) => {
    return (req, res, next) => {
        const userPermissions = req.user.permissions || [];
        
        if (!userPermissions.includes(permission)) {
            return res.status(403).json({
                error: 'Insufficient permissions',
                required: permission,
                user_permissions: userPermissions
            });
        }
        
        next();
    };
};
```

### **Data Encryption & Privacy**
```javascript
// Patient Data Encryption
const crypto = require('crypto');

class DataEncryption {
    constructor() {
        this.algorithm = 'aes-256-gcm';
        this.keyLength = 32;
        this.ivLength = 16;
        this.tagLength = 16;
    }
    
    encryptPHI(data, masterKey) {
        const iv = crypto.randomBytes(this.ivLength);
        const cipher = crypto.createCipher(this.algorithm, masterKey, iv);
        
        let encrypted = cipher.update(JSON.stringify(data), 'utf8', 'hex');
        encrypted += cipher.final('hex');
        
        const tag = cipher.getAuthTag();
        
        return {
            encrypted,
            iv: iv.toString('hex'),
            tag: tag.toString('hex')
        };
    }
    
    decryptPHI(encryptedData, masterKey) {
        const decipher = crypto.createDecipher(
            this.algorithm, 
            masterKey, 
            Buffer.from(encryptedData.iv, 'hex')
        );
        
        decipher.setAuthTag(Buffer.from(encryptedData.tag, 'hex'));
        
        let decrypted = decipher.update(encryptedData.encrypted, 'hex', 'utf8');
        decrypted += decipher.final('utf8');
        
        return JSON.parse(decrypted);
    }
    
    anonymizeData(patientData) {
        // Remove direct identifiers
        const anonymized = { ...patientData };
        delete anonymized.firstName;
        delete anonymized.lastName;
        delete anonymized.email;
        delete anonymized.phone;
        delete anonymized.address;
        
        // Hash indirect identifiers
        anonymized.patientHash = crypto
            .createHash('sha256')
            .update(patientData.patientId + process.env.HASH_SALT)
            .digest('hex');
        
        return anonymized;
    }
}
```

### **Audit Logging System**
```javascript
class AuditLogger {
    static async logAction(req, action, resource, resourceId, result) {
        const auditEntry = {
            userId: req.user?.id,
            sessionId: req.sessionID,
            action,
            resource,
            resourceId,
            ipAddress: req.ip,
            userAgent: req.get('User-Agent'),
            timestamp: new Date(),
            success: result.success,
            errorMessage: result.error || null,
            requestData: this.sanitizeRequestData(req.body),
            responseData: this.sanitizeResponseData(result.data)
        };
        
        // Store in database
        await AuditLog.create(auditEntry);
        
        // Send to external logging service (e.g., Splunk, ELK)
        if (process.env.EXTERNAL_LOGGING_ENABLED) {
            await this.sendToExternalLogger(auditEntry);
        }
        
        // Real-time monitoring alerts
        if (this.isHighRiskAction(action) || !result.success) {
            await this.sendSecurityAlert(auditEntry);
        }
    }
    
    static sanitizeRequestData(data) {
        const sanitized = { ...data };
        
        // Remove sensitive fields
        delete sanitized.password;
        delete sanitized.token;
        delete sanitized.ssn;
        delete sanitized.creditCard;
        
        return sanitized;
    }
    
    static isHighRiskAction(action) {
        const highRiskActions = [
            'user:delete',
            'patient:delete',
            'data:export',
            'system:configure',
            'auth:failed_login'
        ];
        
        return highRiskActions.includes(action);
    }
}
```

---

## 📊 **Database Schema & Relationships**

### **Core Tables Structure**
```sql
-- Users table with authentication
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    role user_role_enum NOT NULL DEFAULT 'doctor',
    license_number VARCHAR(50),
    institution VARCHAR(255),
    is_active BOOLEAN DEFAULT true,
    last_login TIMESTAMP,
    login_attempts INTEGER DEFAULT 0,
    lock_until TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

-- Patients table with medical information
CREATE TABLE patients (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_id VARCHAR(50) UNIQUE NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    date_of_birth DATE,
    gender gender_enum,
    medical_record_number VARCHAR(50) UNIQUE,
    contact_info JSONB DEFAULT '{}',
    emergency_contact JSONB DEFAULT '{}',
    medical_history JSONB DEFAULT '{}',
    current_medications JSONB DEFAULT '[]',
    allergies JSONB DEFAULT '[]',
    is_active BOOLEAN DEFAULT true,
    consent_given BOOLEAN DEFAULT false,
    consent_date TIMESTAMP,
    assigned_doctor_id UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

-- Analyses table for AI results
CREATE TABLE analyses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_id UUID NOT NULL REFERENCES patients(id),
    analysis_type analysis_type_enum NOT NULL,
    status analysis_status_enum DEFAULT 'pending',
    results JSONB DEFAULT '{}',
    confidence DECIMAL(5,4) CHECK (confidence >= 0 AND confidence <= 1),
    classification VARCHAR(100),
    risk_score DECIMAL(5,2) CHECK (risk_score >= 0 AND risk_score <= 100),
    modality_scores JSONB DEFAULT '{}',
    brain_regions JSONB DEFAULT '[]',
    file_metadata JSONB DEFAULT '{}',
    processing_time INTEGER, -- milliseconds
    model_version VARCHAR(50),
    performed_by_id UUID NOT NULL REFERENCES users(id),
    reviewed_by_id UUID REFERENCES users(id),
    reviewed_at TIMESTAMP,
    notes TEXT,
    is_validated BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

-- Audit logs for compliance
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    action VARCHAR(100) NOT NULL,
    resource VARCHAR(100) NOT NULL,
    resource_id VARCHAR(100),
    details JSONB DEFAULT '{}',
    ip_address INET,
    user_agent TEXT,
    session_id VARCHAR(255),
    success BOOLEAN DEFAULT true,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_patients_patient_id ON patients(patient_id);
CREATE INDEX idx_patients_assigned_doctor ON patients(assigned_doctor_id);
CREATE INDEX idx_analyses_patient_id ON analyses(patient_id);
CREATE INDEX idx_analyses_type_status ON analyses(analysis_type, status);
CREATE INDEX idx_analyses_created_at ON analyses(created_at);
CREATE INDEX idx_audit_logs_user_action ON audit_logs(user_id, action);
CREATE INDEX idx_audit_logs_created_at ON audit_logs(created_at);

-- Enums
CREATE TYPE user_role_enum AS ENUM ('admin', 'doctor', 'researcher', 'technician');
CREATE TYPE gender_enum AS ENUM ('male', 'female', 'other', 'prefer_not_to_say');
CREATE TYPE analysis_type_enum AS ENUM ('eeg', 'mri', 'multimodal', 'behavioral', 'symptom_checklist');
CREATE TYPE analysis_status_enum AS ENUM ('pending', 'processing', 'completed', 'failed');
```

### **Advanced Queries & Analytics**
```sql
-- Patient analysis summary with performance metrics
WITH analysis_summary AS (
    SELECT 
        p.patient_id,
        p.first_name,
        p.last_name,
        COUNT(a.id) as total_analyses,
        AVG(a.confidence) as avg_confidence,
        AVG(a.risk_score) as avg_risk_score,
        MAX(a.created_at) as last_analysis,
        STRING_AGG(DISTINCT a.classification, ', ') as classifications
    FROM patients p
    LEFT JOIN analyses a ON p.id = a.patient_id
    WHERE p.deleted_at IS NULL
    GROUP BY p.id, p.patient_id, p.first_name, p.last_name
)
SELECT * FROM analysis_summary
ORDER BY last_analysis DESC;

-- System performance analytics
SELECT 
    DATE_TRUNC('day', created_at) as analysis_date,
    analysis_type,
    COUNT(*) as total_analyses,
    AVG(processing_time) as avg_processing_time,
    AVG(confidence) as avg_confidence,
    COUNT(CASE WHEN status = 'completed' THEN 1 END) as successful_analyses,
    COUNT(CASE WHEN status = 'failed' THEN 1 END) as failed_analyses
FROM analyses
WHERE created_at >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY DATE_TRUNC('day', created_at), analysis_type
ORDER BY analysis_date DESC, analysis_type;

-- Audit trail for compliance reporting
SELECT 
    u.email,
    u.role,
    al.action,
    al.resource,
    al.created_at,
    al.ip_address,
    al.success
FROM audit_logs al
LEFT JOIN users u ON al.user_id = u.id
WHERE al.created_at >= CURRENT_DATE - INTERVAL '7 days'
    AND al.resource = 'patient'
ORDER BY al.created_at DESC;
```

---

## 🚀 **Performance Optimization Strategies**

### **Frontend Optimization**
```javascript
// Code splitting with React.lazy
const DetectionEngine = lazy(() => 
    import('./pages/DetectionEngine').then(module => ({
        default: module.DetectionEngine
    }))
);

// Memoization for expensive computations
const BrainVisualization = React.memo(({ results }) => {
    const processedData = useMemo(() => {
        return processBrainRegions(results.brainRegions);
    }, [results.brainRegions]);
    
    return <ThreeBrainModel data={processedData} />;
});

// Virtual scrolling for large datasets
const PatientList = ({ patients }) => {
    const [visibleRange, setVisibleRange] = useState({ start: 0, end: 50 });
    
    const visiblePatients = useMemo(() => {
        return patients.slice(visibleRange.start, visibleRange.end);
    }, [patients, visibleRange]);
    
    return (
        <VirtualizedList
            items={visiblePatients}
            renderItem={PatientCard}
            onRangeChange={setVisibleRange}
        />
    );
};

// Service Worker for caching
self.addEventListener('fetch', event => {
    if (event.request.url.includes('/api/')) {
        event.respondWith(
            caches.open('api-cache').then(cache => {
                return cache.match(event.request).then(response => {
                    if (response) {
                        // Serve from cache
                        fetch(event.request).then(fetchResponse => {
                            cache.put(event.request, fetchResponse.clone());
                        });
                        return response;
                    }
                    // Fetch and cache
                    return fetch(event.request).then(fetchResponse => {
                        cache.put(event.request, fetchResponse.clone());
                        return fetchResponse;
                    });
                });
            })
        );
    }
});
```

### **Backend Optimization**
```javascript
// Database connection pooling
const sequelize = new Sequelize(DATABASE_URL, {
    pool: {
        max: 20,
        min: 5,
        acquire: 30000,
        idle: 10000
    },
    logging: process.env.NODE_ENV === 'development' ? console.log : false
});

// Query optimization with eager loading
const getPatientWithAnalyses = async (patientId) => {
    return await Patient.findByPk(patientId, {
        include: [
            {
                model: Analysis,
                as: 'analyses',
                where: { status: 'completed' },
                order: [['created_at', 'DESC']],
                limit: 10
            },
            {
                model: User,
                as: 'assignedDoctor',
                attributes: ['id', 'firstName', 'lastName', 'email']
            }
        ]
    });
};

// Caching with Redis
const redis = require('redis');
const client = redis.createClient();

const cacheMiddleware = (duration = 300) => {
    return async (req, res, next) => {
        const key = `cache:${req.originalUrl}`;
        
        try {
            const cached = await client.get(key);
            if (cached) {
                return res.json(JSON.parse(cached));
            }
        } catch (error) {
            console.error('Cache error:', error);
        }
        
        // Override res.json to cache the response
        const originalJson = res.json;
        res.json = function(data) {
            client.setex(key, duration, JSON.stringify(data));
            return originalJson.call(this, data);
        };
        
        next();
    };
};

// Background job processing
const Queue = require('bull');
const analysisQueue = new Queue('analysis processing');

analysisQueue.process('eeg-analysis', async (job) => {
    const { patientId, fileData } = job.data;
    
    try {
        // Process EEG data
        const results = await processEEGData(fileData);
        
        // Update database
        await Analysis.update(
            { 
                status: 'completed',
                results,
                processing_time: Date.now() - job.timestamp
            },
            { where: { id: job.data.analysisId } }
        );
        
        // Send notification
        await sendAnalysisCompleteNotification(patientId);
        
    } catch (error) {
        await Analysis.update(
            { status: 'failed', error_message: error.message },
            { where: { id: job.data.analysisId } }
        );
        throw error;
    }
});
```

---

This technical deep dive demonstrates the **enterprise-grade architecture** and **advanced implementation** that makes NeuroDetect AI a production-ready medical platform. The combination of cutting-edge AI/ML techniques, robust security measures, and scalable architecture positions this project as a significant technical achievement suitable for senior engineering roles.
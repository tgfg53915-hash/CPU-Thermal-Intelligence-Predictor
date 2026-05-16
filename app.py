import os
import joblib
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# تحميل النموذج الذكي المحفوظ
MODEL_PATH = 'project_analysis_1.joblib'

if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
    print("✅ Model loaded successfully!")
else:
    model = None
    print("❌ Model file not found! Please run the training script first.")

# مسار لعرض صفحة الويب الأساسية
@app.route('/', methods=['GET'])
def serve_index():
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), 'site.html')

# مسار استقبال البيانات والتنبؤ
@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Model not trained or saved yet.'}), 500
    
    try:
        # استقبال البيانات القادمة من صفحة الويب (JSON)
        data = request.json
        
        # ترتيب البيانات بناءً على الفيتشرز التي تدرب عليها النموذج
        features_list = [
            float(data['CPU_Usage']),
            float(data['Memory_Usage']),
            float(data['Disk_Usage']),
            float(data['Process_Count']),
            float(data['Thread_Count']),
            float(data['GPU_Temperature'])
        ]
        
        # تحويلها إلى مصفوفة وإجراء التنبؤ
        prediction = model.predict([features_list])
        predicted_temp = round(prediction[0], 2)
        
        # تحديد مستوى الخطورة بناءً على التنبؤ
        status = "Normal"
        if predicted_temp > 85:
            status = "🔥 Danger Zone (>85°C)"
        elif predicted_temp > 70:
            status = "⚠️ Warning (High Temp)"
            
        return jsonify({
            'predicted_temperature': predicted_temp,
            'status': status
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400
# @app.route('/')
# def home():
#     return render_template('site.html')
if __name__ == '__main__':
    # تشغيل السيرفر على الهوست المحلي
    app.run(debug=True, port=5000)





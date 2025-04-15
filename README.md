# **Smart Agriculture Advisory System Using Machine Learning**

## **Overview**
Smart Agriculture Advisory System is a machine learning-powered platform that provides farmers with actionable, data-driven insights to optimize crop selection and profitability. The system analyzes soil data, district-level weather trends, and market price data to recommend the most suitable crops while ensuring sustainable farming practices.

---

## **Features**
- **Real-time Crop Recommendation**: Suggests optimal crops based on soil pH, NPK values, rainfall, temperature, and market conditions.
- **Profitability Prediction**: Achieves **92% accuracy** in predicting profitability metrics for various crops.
- **Dynamic Sustainability Checks**: Ensures district-level sustainability thresholds are met using real-time updates.
- **Dockerized Deployment**: Includes a Dockerfile for easy deployment of the Flask application.
- **REST API Integration**: Provides endpoints for crop recommendations and profitability analysis.

---

## **Getting Started**

### **Prerequisites**
- Python 3.11
- Flask
- Docker installed (optional for containerized deployment)

### **Installation**
1. Clone the repository:
   ```bash
   git clone https://github.com/thiru2612/agri-grow.git
   cd agri-grow

   ```
2. Set up a virtual environment (optional):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application locally:
   ```bash
   python app.py
   ```

### **Run with Docker**
1. Build the Docker image:
   ```bash
   docker build -t agri-grow:v1 .
   ```
2. Run the container:
   ```bash
   docker run -p 5000:5000 agri-grow:v1
   ```

---

## **API Endpoints**

### **Crop Recommendation**
- **URL**: `/recommend`
- **Method**: `POST`
- **Input**: JSON object with:
  ```json
  {
      "District": "Coimbatore",
      "Crop": "Rice",
      "Acres Cultivated": 120,
      "Rainfall (mm)": 1100,
      "Avg Temp (°C)": 28.0,
      "Previous Price": 5700
  }
  ```
- **Response**:
  ```json
  {
      "District": "Coimbatore",
      "Crop": "Rice",
      "Predicted Market Price": 6000.0,
      "Total Acres Cultivated": 350,
      "Sustainability Message": "Warning: Total cultivated acres exceed the sustainable threshold."
  }
  ```

---

## **Future Improvements**
1. **Integration with Government Data**:
   - Utilize real-time data from agricultural and meteorological government agencies to enhance predictions.
   - Collaborate on policy-level insights for sustainable farming practices.

2. **Advanced Research & Development**:
   - Develop machine learning models with deep learning techniques for weather forecasting and yield prediction.
   - Integrate advanced soil health parameters to improve recommendations.

3. **Scalability**:
   - Expand the system to support multi-region datasets and crop-specific recommendations.
   - Optimize database structures for high-performance querying and analytics.

4. **Mobile Application**:
   - Launch a farmer-friendly mobile application for easy access to recommendations and analysis.

---

## **Contributing**
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-name
   ```
3. Make your changes and test them.
4. Submit a pull request.

---

## **License**
This project is licensed under the [Apache License 2.0](LICENSE), allowing modification and redistribution with proper attribution to the original authors.

---

## **Contact**
For any questions or collaborations, contact **Thiruppathi** at [rthiruppathi618@gmail.com](mailto:rthiruppathi618@gmail.com).
```

---

You can copy this content directly into a `README.md` file in your Git repository. Markdown syntax ensures that it renders beautifully on platforms like GitHub, making the project easy to understand for users and contributors. Let me know if you need additional edits! 😊

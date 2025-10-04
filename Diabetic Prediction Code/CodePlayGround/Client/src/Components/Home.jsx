import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

function Home() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    Pregnancies: "",
    Glucose: "",
    BloodPressure: "",
    SkinThickness: "",
    Insulin: "",
    BMI: "",
    DiabetesPedigreeFunction: "",
    Age: "",
  });

  const [prediction, setPrediction] = useState("");

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    axios.post("http://localhost:3001/predict", formData)
      .then((res) => {
        console.log(res)
        console.log("Akash")
        if (res.data.prediction === "Positive") {
          navigate("/diabetic");
        } else {
          navigate("/nondiabetic");
        }
      })
      .catch((err) => {
        console.error(err);
        setPrediction("Prediction failed. Please try again.");
        alert("Failed Prediction")
      });
  };

  return (
    <div className="container d-flex justify-content-center align-items-center min-vh-100 bg-light">
      <div
        className="card p-4 shadow-lg"
        style={{ width: "100%", maxWidth: "500px" }}
      >
        <h2 className="text-center text-primary mb-3">Diabetes Prediction</h2>
        <p className="text-center text-muted mb-4">
          Enter your details to check your risk
        </p>

        <form onSubmit={handleSubmit}>
          {[
            { name: "Pregnancies", label: "Number of Pregnancies" },
            { name: "Glucose", label: "Glucose Level", step: "0.1" },
            { name: "BloodPressure", label: "Blood Pressure", step: "0.1" },
            { name: "SkinThickness", label: "Skin Thickness", step: "0.1" },
            { name: "Insulin", label: "Insulin Level", step: "0.1" },
            { name: "BMI", label: "Body Mass Index (BMI)", step: "0.1" },
            {
              name: "DiabetesPedigreeFunction",
              label: "Diabetes Pedigree Function",
              step: "0.01",
            },
            { name: "Age", label: "Age" },
          ].map((field) => (
            <div className="mb-3" key={field.name}>
              <label htmlFor={field.name} className="form-label">
                {field.label}
              </label>
              <input
                type="number"
                className="form-control"
                id={field.name}
                name={field.name}
                step={field.step || "1"}
                value={formData[field.name]}
                onChange={handleChange}
                required
              />
            </div>
          ))}

          <button type="submit" className="btn btn-primary w-100">
            Predict
          </button>
        </form>

        {prediction && (
          <div className="alert alert-info mt-4 text-center" role="alert">
            {prediction}
          </div>
        )}
      </div>
    </div>
  );
}

export default Home;

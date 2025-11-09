# Concise Technical Report

## 1. Regression Analysis – Diabetes Dataset

### Observed Results
| Model | RMSE (↓) | R² (↑) |
|-------|-----------|--------|
| **Kernel Ridge (RBF)** | **50.8** | **0.51** |
| SVR (RBF) | 51.8 | 0.49 |
| Lasso (α=1.0) | 53.1 | 0.47 |
| Ridge (α=10.0) | 53.6 | 0.46 |
| Linear Regression (OLS) | 53.9 | 0.45 |
| Polynomial (deg=2) | 53.7 | 0.45 |
| Gaussian Process (RBF) | 59.6 | 0.33 |
| Polynomial (deg=3) | 76.7 | −0.11 |

### Interpretation
- The **Kernel Ridge Regression (RBF)** model achieved the **best fit**, showing that the dataset exhibits **nonlinear relationships**.  
- Linear models (OLS, Ridge, Lasso) performed reasonably but lacked flexibility.  
- Polynomial regression with **degree 3** heavily **overfitted**, as seen from negative R².  
- Regularization helped reduce variance but excessive α (in Ridge) or high-degree polynomial features caused underfitting.

### Plot Analysis
- **RMSE Bar Plot:** Kernel Ridge and SVR have the lowest RMSE.  
- **R² Bar Plot:** Kernel Ridge again ranks highest, confirming optimal bias-variance tradeoff.  


## 2. Classification Analysis – Digits Dataset

### Observed Results
| Model | Accuracy |
|--------|-----------|
| **SVC (RBF, C=10)** | **0.981** |
| MLP (100 neurons) | 0.975 |
| Logistic Regression (C=1.0) | 0.972 |
| Logistic Regression (C=0.1)** | 0.969 |

### Interpretation
- **SVC (RBF)** produced the **highest accuracy (~98%)**, forming flexible, nonlinear decision boundaries.  
- **MLP** was close behind, needing more hyperparameter tuning.  
- **Logistic Regression** performed strongly but underfit slightly with higher regularization (smaller C).

### Confusion Matrices
- **SVC:** Nearly perfect diagonal – minimal misclassifications.  
- **MLP:** Occasional confusion between visually similar digits like **3 ↔ 8** and **4 ↔ 9**.  
- **Logistic Regression:** More off-diagonal elements between **curved digits (3, 8, 9)** due to linear limitations.

### Plot Analysis
- **Accuracy Bar Plot:** SVC leads, followed by MLP and Logistic Regression.  
- **Confusion Matrices:** Clear diagonal pattern for SVC confirms superior classification consistency.  


## 3. Overall Summary

| Task | Best Model | Reason |
|-------|-------------|--------|
| **Regression** | **Kernel Ridge (RBF)** | Captures nonlinear trends; best RMSE and R² |
| **Classification** | **SVC (RBF)** | Highest accuracy and clean confusion matrix |

**Key Insight:**  
Both tasks favor **nonlinear kernel-based models (RBF)**. They deliver the best bias–variance tradeoff when paired with proper **regularization tuning (α, C, γ)**.

---
*Prepared by: Automated Technical Analysis Engine (GPT-5)*

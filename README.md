# ⬡ ClusterNova - Customer Segmentation & Basket Analysis

Machine Learning II project developed by **Lucas Casemiro**, **Lourenço Lima**, and **Afonso Lince** (undergraduate students in Data Science at NOVA IMS).

This platform features a professional customer intelligence dashboard implementing:

* **Customer Segmentation**: Unsupervised K-Means clustering ($k=8$ using `RobustScaler` on demographic & behavioral features, combined with an isolated `Vegans` cluster, yielding **9 final segments**).

* **Market Basket Analysis**: decopled Apriori association rules mined per segment to support personalized campaigns and real-time checkout cross-selling.
* **Interactive Simulator**: A live simulator featuring customer lookups, promotions campaigns, evaluation scoring, and a shopping checkout simulator.

---

## 🚀 How to Run the Project (Como Executar o Projeto)

### Prerequisites

Make sure you have **Python 3.10+** and **Node.js (v18+)** installed.

---

### Step 1: Start the Flask Backend Server (Passo 1: Iniciar o Servidor Flask)

The backend manages real-time customer lookups, retrieves historical carts, and serves the mined association rules.

1. Open your terminal at the project root directory.
2. Activate the virtual environment:
   * **Windows (PowerShell)**:

     ```powershell
     .\.venv\Scripts\Activate.ps1

     ```

   * **macOS/Linux**:

     ```bash

     source .venv/bin/activate

     ```

3. Install the dependencies (if not already installed):

   ```bash
   pip install -r requirements.txt

   ```

4. Run the Flask server:

   ```bash

   python server.py

   ```

   *The server will start running on **`http://localhost:5000`**.*

---

### Step 2: Start the React Frontend Dashboard (Passo 2: Iniciar o Dashboard React)

The dashboard provides a visual, interactive interface to explore segment distributions, view clustering metrics, and run simulator actions.

1. Open a new terminal window and navigate to the `dashboard/` directory:

   ```bash

   cd dashboard

   ```

2. Install the frontend dependencies:

   ```bash
   npm install

   ```

3. Run the Vite development server:

   ```bash

   npm run dev

   ```

   *Open your browser and navigate to the local link shown (typically **`http://localhost:5173`**).*

*(Optional)* Alternatively, you can preview the compiled production build:

```bash
npm run preview
```

---

## 📂 Project Structure

* `notebooks/`: Contains the Jupyter notebooks for Exploratory Data Analysis (`eda.ipynb`), Customer Segmentation (`segmentation.ipynb`), and Market Basket Analysis (`basket.ipynb`).
* `functions/`: Reusable Python helpers for preprocessing, clustering calculations, and visualizations.
* `data/`:
  * `ci_clustering.csv`: Raw cleaned customer dataset.
  * `ci_clustered.csv`: Clustered customer dataset containing K-Means labels (0 to 8).
  * `customer_basket.csv`: Recorded shopping cart transactions.
  * `cluster_association_rules.json`: Decoupled single-product Apriori association rules per cluster.
* `dashboard/`: React + Vite frontend source code.
* `server.py`: Flask REST API serving predictions, propensity scores, rules, and simulated checkouts.

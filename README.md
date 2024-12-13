# API Gateway Project

## 🚀 Overview

Welcome to the **API Gateway Project** built with **FastAPI**! This gateway integrates multiple powerful services, each handled by dedicated routers. The core services available through this gateway are:

- **LawGPT**: Get legal advice and assistance powered by AI.
- **Bail Reckoner**: Estimate bail amounts based on specific parameters.
- **Generate FIR**: Generate a First Information Report (FIR) in PDF format.

Each of these services is accessible through distinct routes, ensuring modularity and ease of use.

---

## 🛠️ Installation

Follow these steps to get the API Gateway up and running locally:

### 1. Clone the Repository

```bash
git clone https://github.com/Aniudupa15/Judica-API.git
cd Judica-API
```

### 2. Create a Virtual Environment (Recommended)

It's recommended to use a virtual environment to isolate the dependencies.

**For Linux/MacOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

**For Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

Install the required Python libraries using pip:

```bash
pip install -r requirements.txt
```

### 4. Run the Application

To start the server:

```bash
python main.py
```

By default, the server will run on port 8000. You can change this by setting the `PORT` environment variable.

---

## 🌐 Accessing the API

Once the server is running, the following routes will be available:

- **`/lawgpt`**: Interact with the LawGPT module.
- **`/bail-reckoner`**: Use the Bail Reckoner for bail estimations.
- **`/generate-fir`**: Generate an FIR in PDF format.


## 📡 API Endpoints

### `/lawgpt`
- **Prefix**: `/lawgpt`
- **Tag**: LawGPT
- Handles legal advice requests powered by AI.

### `/bail-reckoner`
- **Prefix**: `/bail-reckoner`
- **Tag**: Bail Reckoner
- Used for estimating bail amounts based on given parameters.

### `/generate-fir`
- **Prefix**: `/generate-fir`
- **Tag**: Generate FIR
- Generates an FIR in PDF format for legal purposes.

## ⚙️ Environment Variables

- `PORT`: The port where the server runs (defaults to `8000`).

To change the port, set the `PORT` variable:

**On Linux/MacOS:**

```bash
export PORT=5000
```

**On Windows:**

```bash
set PORT=5000
```

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

---

## 🧑‍💻 Contribution

Feel free to fork this repository and create pull requests. Contributions are welcome to improve the functionality and features of this API Gateway!

Happy coding! 🎉

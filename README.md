# TP-Link Watch

A FastAPI application to monitor and retrieve status information from TP-Link smart home devices using the TP-Link Cloud API.

## Features

- **List Devices**: Retrieve a list of all devices associated with your TP-Link account.
- **Device Details**: Get detailed information about a specific device using its MAC address.
- **Device Status**: Check the online/offline status of a specific device.
- **Dockerized**: Easy deployment with Docker and Docker Compose.

## Prerequisites

- **Python 3.11+** (for local execution)
- **Docker & Docker Compose** (for containerized execution)
- **TP-Link Account**

## Configuration

Create a `.env` file in the root directory (you can use `.env.example` as a template):

```bash
cp .env.example .env
```

Edit `.env` and add your TP-Link credentials:

```env
TPLINK_USERNAME=your_email@example.com
TPLINK_PASSWORD=your_password
```

## Running the Application

### Using Docker (Recommended)

Build and run the container:

```bash
docker compose up --build -d
```

The API will be available at `http://localhost:8000`.

To stop the application:

```bash
docker compose down
```

### Running Locally

1.  **Install Dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

2.  **Start the Server**:

    ```bash
    uvicorn app:app --reload
    ```

    The API will be available at `http://localhost:8000`.

## API Endpoints

### Interactive Documentation

You can explore and test the API using the automatic interactive documentation:

-   **Swagger UI**: `http://localhost:8000/docs`
-   **ReDoc**: `http://localhost:8000/redoc`

### 1. List All Devices

*   **URL**: `/devices`
*   **Method**: `GET`
*   **Description**: Returns a list of all devices with their alias, model type, and detailed info.

### 2. Get Device Details

*   **URL**: `/devices/{mac_addr}`
*   **Method**: `GET`
*   **Description**: Returns details for a specific device identified by its MAC address.

### 3. Get Device Status

*   **URL**: `/devices/{mac_addr}/status`
*   **Method**: `GET`
*   **Description**: Returns the online status of the device.
*   **Response**:
    *   `200 OK`: `{"status": "online"}`
    *   `503 Service Unavailable`: Device is offline.

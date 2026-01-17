from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class DeviceInfo(BaseModel):
  device_type: str
  role: int
  fw_ver: str
  app_server_url: str
  device_region: str
  device_id: str
  device_name: str
  device_hw_ver: str
  alias: str
  device_mac: str
  oem_id: str
  device_model: str
  hw_id: str
  fw_id: str
  is_same_region: bool
  status: int
    
class DeviceResponse(BaseModel):
  alias: str
  model_type: str
  info: DeviceInfo

class DeviceStatus(BaseModel):
  status: str

# Mock Data
MOCK_DEVICE_INFO = {
  "device_type": "WIRELESSROUTER",
  "role": 0,
  "fw_ver": "1.0.0 Build 20230101 Rel. 12345",
  "app_server_url": "https://api.tplinkcloud.com",
  "device_region": "us-east-1",
  "device_id": "1234567890ABCDEF1234567890ABCDEF12345678",
  "device_name": "Mock Router 1",
  "device_hw_ver": "1.0",
  "alias": "Living Room",
  "device_mac": "AA:BB:CC:DD:EE:FF",
  "oem_id": "11223344556677889900AABBCCDDEEFF",
  "device_model": "Archer AX50",
  "hw_id": "1A2B3C4D5E6F78901A2B3C4D5E6F7890",
  "fw_id": "9876543210FEDCBA9876543210FEDCBA",
  "is_same_region": True,
  "status": 1
}

list_devices_responses = {
  200: {
    "description": "List of devices",
    "content": {
      "application/json": {
        "example": [
          {
            "alias": "Living Room",
            "model_type": "UNKNOWN",
            "info": MOCK_DEVICE_INFO
          }
        ]
      }
    }
  }
}

get_device_responses = {
  200: {
    "description": "Device details",
    "content": {
      "application/json": {
        "example": {
          "alias": "Living Room",
          "model_type": "UNKNOWN",
          "info": MOCK_DEVICE_INFO
        }
      }
    }
  },
  404: {"description": "Device not found"}
}

get_device_status_responses = {
  200: {
    "description": "Device status",
    "content": {
      "application/json": {
        "example": {"status": "online"}
      }
    }
  },
  404: {"description": "Device not found"},
  503: {"description": "Device offline"}
}

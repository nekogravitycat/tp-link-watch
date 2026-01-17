import os
import asyncio
from typing import List, Optional
from fastapi import FastAPI, HTTPException, status as http_status
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from tplinkcloud import TPLinkDeviceManager
from schemas import (
  DeviceInfo, DeviceResponse, DeviceStatus,
  list_devices_responses, get_device_responses, get_device_status_responses
)

# Load environment variables
load_dotenv()

username = os.getenv("TPLINK_USERNAME")
password = os.getenv("TPLINK_PASSWORD")

if not username or not password:
  raise ValueError("Please set TPLINK_USERNAME and TPLINK_PASSWORD in .env file")

app = FastAPI()
device_manager = TPLinkDeviceManager(
  username=username,
  password=password,
  prefetch=False,
  cache_devices=False,
)

def serialize_device_info(obj):
  if hasattr(obj, "__dict__"):
    return {k: serialize_device_info(v) for k, v in vars(obj).items()}
  if isinstance(obj, list):
    return [serialize_device_info(i) for i in obj]
  if hasattr(obj, "name"):
    return obj.name
  return obj

async def get_device_by_mac(mac_addr: str):
  devices = await device_manager.get_devices()
  for device in devices:
    # Check if mac address matches in device or device_info
    d_mac = getattr(device, 'mac', None)
    
    # Check device_info for mac address
    if hasattr(device, 'device_info'):
      d_info = device.device_info
      if isinstance(d_info, dict):
        d_mac = d_info.get('device_mac') or d_info.get('mac') or d_info.get('macAddress')
      elif hasattr(d_info, 'device_mac'):
        d_mac = d_info.device_mac
      elif hasattr(d_info, 'mac'):
        d_mac = d_info.mac
    
    # Normalize match
    if d_mac and d_mac.replace(':', '').replace('-', '').lower() == mac_addr.replace(':', '').replace('-', '').lower():
      return device
          
  return None

@app.get("/devices", response_model=List[DeviceResponse], responses=list_devices_responses)
async def list_devices():
  devices = await device_manager.get_devices()
  results = []
  for device in devices:
    dev_data = {
      "alias": device.get_alias(),
      "model_type": device.model_type.name if hasattr(device.model_type, 'name') else str(device.model_type),
      "info": device.device_info
    }
    results.append(dev_data)
      
  for r in results:
    r['info'] = serialize_device_info(r['info'])
      
  return results

@app.get("/devices/{mac_addr}", response_model=DeviceResponse, responses=get_device_responses)
async def get_device(mac_addr: str):
  device = await get_device_by_mac(mac_addr)
  if not device:
    raise HTTPException(status_code=404, detail="Device not found")
  
  return {
    "alias": device.get_alias(),
    "model_type": device.model_type.name if hasattr(device.model_type, 'name') else str(device.model_type),
    "info": serialize_device_info(device.device_info)
  }

@app.get("/devices/{mac_addr}/status", response_model=DeviceStatus, responses=get_device_status_responses)
async def get_device_status(mac_addr: str):
  device = await get_device_by_mac(mac_addr)
  if not device:
    raise HTTPException(status_code=404, detail="Device not found")
  
  # Check status attribute
  status_val = 0
  
  info = device.device_info
  if hasattr(info, 'status'):
    status_val = info.status
  elif isinstance(info, dict):
    status_val = info.get('status', 0)
      
  # Return 200 if "status" is 1; 503 if 0.
  if status_val == 1:
    return {"status": "online"}
  else:
    raise HTTPException(status_code=503, detail="Device offline or status 0")

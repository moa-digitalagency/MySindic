#!/usr/bin/env python3
"""Test rapide de l'API maintenance"""
import requests

base_url = "http://localhost:5000"

# Test l'API sans authentification
print("=== Test GET /api/admin/maintenance ===")
response = requests.get(f"{base_url}/api/admin/maintenance")
print(f"Status: {response.status_code}")
print(f"Response: {response.text[:500]}")

print("\n=== Test GET /api/resident/maintenance ===")
response = requests.get(f"{base_url}/api/resident/maintenance")
print(f"Status: {response.status_code}")
print(f"Response: {response.text[:500]}")

print("\n=== Test Health endpoint ===")
response = requests.get(f"{base_url}/health")
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")

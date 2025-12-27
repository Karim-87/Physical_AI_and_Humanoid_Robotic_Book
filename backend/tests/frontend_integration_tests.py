import asyncio
import requests
import pytest
from main import app
import uvicorn
import threading
import time
from fastapi.testclient import TestClient

# Create a test client for the FastAPI app
client = TestClient(app)

def test_frontend_integration_chat_endpoint():
    """Test for frontend calling /chat endpoint and receiving formatted response"""
    print("Testing frontend integration with /chat endpoint...")

    # Test the chat endpoint
    response = client.post(
        "/api/v1/chat",
        json={
            "message": "What is Physical AI?",
            "selected_text": None,
            "session_id": None
        }
    )

    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

    # Check that the response is successful
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    # Check that the response has the expected fields
    data = response.json()
    assert "response" in data, "Response should contain 'response' field"
    assert "session_id" in data, "Response should contain 'session_id' field"
    assert "mode" in data, "Response should contain 'mode' field"
    assert "retrieved_chunks_count" in data, "Response should contain 'retrieved_chunks_count' field"
    assert "response_time" in data, "Response should contain 'response_time' field"

    print("✓ Chat endpoint test passed")


def test_cors_middleware():
    """Test for CORS middleware allowing frontend domain access"""
    print("\nTesting CORS middleware...")

    # Test preflight request (OPTIONS) to check CORS headers
    headers = {
        "Origin": "https://physical-ai-and-humanoid-robotic-bo-three.vercel.app",
        "Access-Control-Request-Method": "POST",
        "Access-Control-Request-Headers": "Content-Type",
    }

    response = client.options("/api/v1/chat", headers=headers)

    # Check that CORS headers are present
    cors_headers = [
        "access-control-allow-origin",
        "access-control-allow-credentials",
        "access-control-allow-methods",
        "access-control-allow-headers",
    ]

    for header in cors_headers:
        assert header in response.headers, f"Missing CORS header: {header}"

    print(f"Access-Control-Allow-Origin: {response.headers.get('access-control-allow-origin')}")
    print("✓ CORS middleware test passed")


def test_session_management():
    """Test for frontend integration with session management"""
    print("\nTesting session management integration...")

    # Test creating a new session
    response1 = client.post(
        "/api/v1/chat",
        json={
            "message": "Hello, I'm a test user.",
            "selected_text": None,
            "session_id": None  # Should create a new session
        }
    )

    assert response1.status_code == 200
    data1 = response1.json()
    session_id = data1.get("session_id")
    assert session_id is not None, "Should return a session ID"

    print(f"Created session: {session_id}")

    # Test using the existing session
    response2 = client.post(
        "/api/v1/chat",
        json={
            "message": "What was my first message?",
            "selected_text": None,
            "session_id": session_id  # Use the existing session
        }
    )

    assert response2.status_code == 200
    data2 = response2.json()
    assert data2["session_id"] == session_id, "Should return the same session ID"

    print("✓ Session management test passed")


def run_integration_tests():
    """Run all frontend integration tests"""
    print("Running frontend integration tests...\n")

    test_frontend_integration_chat_endpoint()
    test_cors_middleware()
    test_session_management()

    print("\n✓ All frontend integration tests passed!")


if __name__ == "__main__":
    run_integration_tests()
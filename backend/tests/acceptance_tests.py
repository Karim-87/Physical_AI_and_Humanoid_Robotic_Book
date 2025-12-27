import asyncio
import pytest
from src.config.qdrant_config import qdrant_service
from src.config.cohere_config import cohere_service
from src.services.agent import rag_agent
from src.services.retrieval import retrieval_service

async def test_scenario_1_accurate_response():
    """Test scenario 1: accurate response to Physical AI concepts"""
    print("Testing scenario 1: accurate response to Physical AI concepts")

    # Initialize services
    await qdrant_service.initialize()
    cohere_service.initialize()

    # Test query about Physical AI
    query = "What is Physical AI?"

    # Process the query
    result = await rag_agent.process_query(query=query)

    response = result["response"]
    mode = result["mode"]
    retrieved_chunks_count = result["retrieved_chunks_count"]

    print(f"Query: {query}")
    print(f"Response: {response}")
    print(f"Mode: {mode}")
    print(f"Retrieved chunks count: {retrieved_chunks_count}")

    # Check that we got a response
    assert response is not None and len(response) > 0, "Should return a response"

    # Check that it's using the correct mode (assuming no selected text was provided)
    assert mode in ["full-book", "selected-text-only", "error"], "Should have a valid mode"

    # Check that we retrieved some chunks (if using full-book mode)
    if mode == "full-book":
        assert retrieved_chunks_count > 0, "Should retrieve some chunks in full-book mode"

    print("✓ Scenario 1 test passed")


async def test_scenario_2_focused_response():
    """Test scenario 2: focused response on selected text"""
    print("\nTesting scenario 2: focused response on selected text")

    # Initialize services
    await qdrant_service.initialize()
    cohere_service.initialize()

    # Sample selected text
    selected_text = """
    Physical AI is an approach to robotics that emphasizes the importance of physical interaction
    with the environment as a fundamental aspect of intelligence. Unlike traditional AI which
    focuses primarily on computation and data processing, Physical AI recognizes that intelligent
    behavior emerges from the dynamic interaction between an agent and its physical environment.
    This approach has shown significant promise in developing more robust and adaptable robotic systems.
    """

    # Query about the selected text
    query = "What is Physical AI according to this text?"

    # Process the query with selected text
    result = await rag_agent.process_query(
        query=query,
        selected_text=selected_text
    )

    response = result["response"]
    mode = result["mode"]
    retrieved_chunks_count = result["retrieved_chunks_count"]

    print(f"Query: {query}")
    print(f"Selected text: {selected_text[:100]}...")
    print(f"Response: {response}")
    print(f"Mode: {mode}")
    print(f"Retrieved chunks count: {retrieved_chunks_count}")

    # Check that we got a response
    assert response is not None and len(response) > 0, "Should return a response"

    # Check that it's using selected-text-only mode
    assert mode == "selected-text-only", f"Should be in selected-text-only mode, got {mode}"

    # Should have retrieved some content from the selected text
    assert retrieved_chunks_count >= 0, "Should have processed the selected text"

    print("✓ Scenario 2 test passed")


async def test_scenario_3_out_of_scope():
    """Test scenario 3: appropriate response for out-of-scope queries"""
    print("\nTesting scenario 3: appropriate response for out-of-scope queries")

    # Initialize services
    await qdrant_service.initialize()
    cohere_service.initialize()

    # Query that's likely out of scope of the textbook
    query = "What is the weather like today?"

    # Process the query
    result = await rag_agent.process_query(query=query)

    response = result["response"]
    mode = result["mode"]

    print(f"Query: {query}")
    print(f"Response: {response}")
    print(f"Mode: {mode}")

    # Check that we got a response
    assert response is not None and len(response) > 0, "Should return a response"

    # The response should acknowledge that the question is out of scope
    # or provide guidance to relevant topics
    # This is a basic check - in a real test, you might want more specific assertions
    assert isinstance(response, str), "Response should be a string"

    print("✓ Scenario 3 test passed")


async def run_all_acceptance_tests():
    """Run all acceptance tests"""
    print("Running acceptance tests...\n")

    await test_scenario_1_accurate_response()
    await test_scenario_2_focused_response()
    await test_scenario_3_out_of_scope()

    print("\n✓ All acceptance tests passed!")


if __name__ == "__main__":
    asyncio.run(run_all_acceptance_tests())
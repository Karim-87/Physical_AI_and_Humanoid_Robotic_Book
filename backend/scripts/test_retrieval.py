import asyncio
import logging
from src.config.qdrant_config import qdrant_service
from src.config.cohere_config import cohere_service
from src.services.retrieval import retrieval_service

logger = logging.getLogger(__name__)

async def test_retrieval():
    """Test the retrieval pipeline with sample queries"""
    print("Initializing services...")

    # Initialize services
    await qdrant_service.initialize()
    cohere_service.initialize()

    print("Services initialized successfully!")

    # Test queries
    test_queries = [
        "What is Physical AI?",
        "Explain VLA models",
        "ROS2 fundamentals",
        "Humanoid robotics control"
    ]

    print("\nTesting retrieval pipeline...")

    for query in test_queries:
        print(f"\nQuery: {query}")
        print("-" * 50)

        try:
            # Test full-book retrieval
            results = await retrieval_service.retrieve(query, top_k=3)

            if results:
                print(f"Found {len(results)} relevant chunks:")
                for i, result in enumerate(results, 1):
                    print(f"\n{i}. Source: {result['source']}")
                    print(f"   Title: {result['title']}")
                    print(f"   Score: {result['score']:.3f}")
                    print(f"   Text preview: {result['text'][:200]}...")
            else:
                print("No relevant chunks found.")

        except Exception as e:
            print(f"Error retrieving for query '{query}': {e}")

    # Test selected-text-only mode
    print(f"\nTesting selected-text-only mode...")
    print("-" * 50)

    selected_text = """
    Physical AI is an approach to robotics that emphasizes the importance of physical interaction
    with the environment as a fundamental aspect of intelligence. Unlike traditional AI which
    focuses primarily on computation and data processing, Physical AI recognizes that intelligent
    behavior emerges from the dynamic interaction between an agent and its physical environment.
    """

    query = "What is Physical AI?"

    try:
        results = await retrieval_service.retrieve(query, selected_text=selected_text, top_k=1)

        if results:
            print(f"Query: {query}")
            print(f"Mode: Selected-text-only")
            print(f"Found {len(results)} relevant chunks:")
            for i, result in enumerate(results, 1):
                print(f"\n{i}. Source: {result['source']}")
                print(f"   Score: {result['score']:.3f}")
                print(f"   Text: {result['text'][:300]}...")
        else:
            print("No relevant chunks found in selected text.")

    except Exception as e:
        print(f"Error in selected-text retrieval: {e}")

if __name__ == "__main__":
    asyncio.run(test_retrieval())
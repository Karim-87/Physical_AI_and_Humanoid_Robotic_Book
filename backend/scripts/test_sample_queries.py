import asyncio
import logging
from src.config.qdrant_config import qdrant_service
from src.config.cohere_config import cohere_service
from src.services.retrieval import retrieval_service
from src.services.agent import rag_agent

logger = logging.getLogger(__name__)

async def test_sample_queries():
    """Test sample queries to verify the RAG pipeline"""
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

    print("\nTesting sample queries...")

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

                # Test the full agent pipeline
                print(f"\nTesting full agent pipeline...")
                agent_response = await rag_agent.process_query(query=query)
                print(f"Agent response: {agent_response['response'][:300]}...")
                print(f"Mode: {agent_response['mode']}")
                print(f"Response time: {agent_response['response_time']:.2f}s")
            else:
                print("No relevant chunks found.")

        except Exception as e:
            print(f"Error processing query '{query}': {e}")

    # Test selected-text-only mode
    print(f"\n" + "="*60)
    print(f"Testing selected-text-only mode...")
    print("="*60)

    selected_text = """
    Physical AI is an approach to robotics that emphasizes the importance of physical interaction
    with the environment as a fundamental aspect of intelligence. Unlike traditional AI which
    focuses primarily on computation and data processing, Physical AI recognizes that intelligent
    behavior emerges from the dynamic interaction between an agent and its physical environment.
    This approach has shown significant promise in developing more robust and adaptable robotic systems.
    """

    query = "What is Physical AI?"

    try:
        print(f"Query: {query}")
        print(f"Selected text: {selected_text[:100]}...")
        print("-" * 50)

        # Test the full agent pipeline with selected text
        agent_response = await rag_agent.process_query(
            query=query,
            selected_text=selected_text
        )

        print(f"Agent response: {agent_response['response']}")
        print(f"Mode: {agent_response['mode']}")
        print(f"Retrieved chunks count: {agent_response['retrieved_chunks_count']}")
        print(f"Response time: {agent_response['response_time']:.2f}s")

    except Exception as e:
        print(f"Error in selected-text test: {e}")

    print(f"\nSample query testing completed!")

if __name__ == "__main__":
    asyncio.run(test_sample_queries())
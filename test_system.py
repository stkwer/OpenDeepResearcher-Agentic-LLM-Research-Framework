# #!/usr/bin/env python3
# """
# Test script for OpenDeepResearcher
# Runs basic functionality tests to ensure system is working
# """

# import os
# import sys
# from pathlib import Path

# def test_imports():
#     """Test if all required modules can be imported"""
#     print("🧪 Testing imports...")
    
#     try:
#         import streamlit
#         print("✅ Streamlit imported")
#     except ImportError as e:
#         print(f"❌ Streamlit import failed: {e}")
#         return False
    
#     try:
#         from langchain_openai import ChatOpenAI
#         from langchain_core.messages import HumanMessage
#         print("✅ LangChain imported")
#     except ImportError as e:
#         print(f"❌ LangChain import failed: {e}")
#         return False
    
#     try:
#         from tavily import TavilyClient
#         print("✅ Tavily imported")
#     except ImportError as e:
#         print(f"❌ Tavily import failed: {e}")
#         return False
    
#     try:
#         from dotenv import load_dotenv
#         print("✅ Python-dotenv imported")
#     except ImportError as e:
#         print(f"❌ Python-dotenv import failed: {e}")
#         return False
    
#     return True

# def test_project_structure():
#     """Test if all required files exist"""
#     print("\n📁 Testing project structure...")
    
#     required_files = [
#         "app.py",
#         "main.py", 
#         "planner.py",
#         "search.py",
#         "writer.py",
#         "config.py",
#         "utils.py",
#         ".env",
#         "requirements.txt",
#         "graph/research_graph.py"
#     ]
    
#     missing_files = []
#     for file_path in required_files:
#         if not Path(file_path).exists():
#             missing_files.append(file_path)
#         else:
#             print(f"✅ {file_path}")
    
#     if missing_files:
#         print(f"❌ Missing files: {missing_files}")
#         return False
    
#     return True

# def test_env_file():
#     """Test if .env file is properly configured"""
#     print("\n🔧 Testing environment configuration...")
    
#     from dotenv import load_dotenv
#     load_dotenv()
    
#     tavily_key = os.getenv("TAVILY_API_KEY")
#     if not tavily_key or tavily_key == "your_tavily_api_key_here":
#         print("⚠️  Tavily API key not configured in .env file")
#         return False
#     else:
#         print("✅ Tavily API key configured")
#         return True

# def test_lm_studio_connection():
#     """Test connection to LM Studio"""
#     print("\n🤖 Testing LM Studio connection...")
    
#     try:
#         from langchain_openai import ChatOpenAI
#         from langchain_core.messages import HumanMessage
        
#         llm = ChatOpenAI(
#             openai_api_key=\"lm-studio\",
#             base_url=\"http://127.0.0.1:1234/v1\",
#             model=\"qwen2.5-7b-instruct\"
#         )
        
#         response = llm.invoke([HumanMessage(content=\"Hello, are you working?\")])
        
#         if response and response.content:\n            print(\"✅ LM Studio connection successful\")\n            print(f\"   Response: {response.content[:50]}...\")\n            return True\n        else:\n            print(\"❌ LM Studio responded but no content\")\n            return False\n            \n    except Exception as e:\n        print(f\"❌ LM Studio connection failed: {e}\")\n        return False\n\ndef test_tavily_connection():\n    \"\"\"Test connection to Tavily API\"\"\"\n    print(\"\\n🔍 Testing Tavily API connection...\")\n    \n    try:\n        from dotenv import load_dotenv\n        from tavily import TavilyClient\n        \n        load_dotenv()\n        tavily_key = os.getenv(\"TAVILY_API_KEY\")\n        \n        if not tavily_key or tavily_key == \"your_tavily_api_key_here\":\n            print(\"⚠️  Tavily API key not configured\")\n            return False\n        \n        client = TavilyClient(api_key=tavily_key)\n        response = client.search(\n            query=\"test search\",\n            max_results=1,\n            timeout=5\n        )\n        \n        if response and \"results\" in response:\n            print(\"✅ Tavily API connection successful\")\n            return True\n        else:\n            print(\"❌ Tavily API responded but no results\")\n            return False\n            \n    except Exception as e:\n        print(f\"❌ Tavily API connection failed: {e}\")\n        return False\n\ndef test_research_pipeline():\n    \"\"\"Test the complete research pipeline with a simple topic\"\"\"\n    print(\"\\n🔬 Testing research pipeline...\")\n    \n    try:\n        from planner import planner_agent\n        from search import search_agent\n        from writer import writer_agent\n        \n        # Test with a simple topic\n        topic = \"What is artificial intelligence?\"\n        \n        # Test planner\n        print(\"   Testing planner agent...\")\n        sub_questions = planner_agent(topic, num_subquestions=2)\n        if not sub_questions or len(sub_questions) == 0:\n            print(\"❌ Planner agent failed\")\n            return False\n        print(f\"   ✅ Generated {len(sub_questions)} sub-questions\")\n        \n        # Test search (only if Tavily is configured)\n        tavily_key = os.getenv(\"TAVILY_API_KEY\")\n        if tavily_key and tavily_key != \"your_tavily_api_key_here\":\n            print(\"   Testing search agent...\")\n            search_results = search_agent(sub_questions[:1], max_results_per_query=1)\n            if not search_results:\n                print(\"❌ Search agent failed\")\n                return False\n            print(\"   ✅ Search agent working\")\n            \n            # Test writer\n            print(\"   Testing writer agent...\")\n            content_blocks = []\n            for q, items in search_results.items():\n                content_blocks.append(q)\n                for item in items:\n                    content_blocks.append(item.get(\"content\", \"\"))\n            \n            research_text = \"\\n\".join(content_blocks)\n            final_report = writer_agent(topic, research_text)\n            \n            if not final_report:\n                print(\"❌ Writer agent failed\")\n                return False\n            print(\"   ✅ Writer agent working\")\n        else:\n            print(\"   ⚠️  Skipping search/writer tests (Tavily not configured)\")\n        \n        print(\"✅ Research pipeline test completed\")\n        return True\n        \n    except Exception as e:\n        print(f\"❌ Research pipeline test failed: {e}\")\n        return False\n\ndef main():\n    \"\"\"Run all tests\"\"\"\n    print(\"🧠 OpenDeepResearcher Test Suite\")\n    print(\"=\" * 40)\n    \n    tests = [\n        (\"Import Test\", test_imports),\n        (\"Project Structure\", test_project_structure),\n        (\"Environment Config\", test_env_file),\n        (\"LM Studio Connection\", test_lm_studio_connection),\n        (\"Tavily Connection\", test_tavily_connection),\n        (\"Research Pipeline\", test_research_pipeline)\n    ]\n    \n    results = []\n    for test_name, test_func in tests:\n        try:\n            result = test_func()\n            results.append((test_name, result))\n        except Exception as e:\n            print(f\"❌ {test_name} crashed: {e}\")\n            results.append((test_name, False))\n    \n    # Summary\n    print(\"\\n\" + \"=\" * 40)\n    print(\"📊 Test Results Summary:\")\n    \n    passed = 0\n    for test_name, result in results:\n        status = \"✅ PASS\" if result else \"❌ FAIL\"\n        print(f\"   {test_name}: {status}\")\n        if result:\n            passed += 1\n    \n    print(f\"\\n🎯 {passed}/{len(results)} tests passed\")\n    \n    if passed == len(results):\n        print(\"🎉 All tests passed! System is ready to use.\")\n        print(\"   Run: streamlit run app.py\")\n    else:\n        print(\"⚠️  Some tests failed. Check the issues above.\")\n\nif __name__ == \"__main__\":\n    main()", "oldStr": "#!/usr/bin/env python3\n\"\"\"\nTest script for OpenDeepResearcher\nRuns basic functionality tests to ensure system is working\n\"\"\"\n\nimport os\nimport sys\nfrom pathlib import Path\n\ndef test_imports():\n    \"\"\"Test if all required modules can be imported\"\"\"\n    print(\"🧪 Testing imports...\")\n    \n    try:\n        import streamlit\n        print(\"✅ Streamlit imported\")\n    except ImportError as e:\n        print(f\"❌ Streamlit import failed: {e}\")\n        return False\n    \n    try:\n        from langchain_openai import ChatOpenAI\n        from langchain_core.messages import HumanMessage\n        print(\"✅ LangChain imported\")\n    except ImportError as e:\n        print(f\"❌ LangChain import failed: {e}\")\n        return False\n    \n    try:\n        from tavily import TavilyClient\n        print(\"✅ Tavily imported\")\n    except ImportError as e:\n        print(f\"❌ Tavily import failed: {e}\")\n        return False\n    \n    try:\n        from dotenv import load_dotenv\n        print(\"✅ Python-dotenv imported\")\n    except ImportError as e:\n        print(f\"❌ Python-dotenv import failed: {e}\")\n        return False\n    \n    return True\n\ndef test_project_structure():\n    \"\"\"Test if all required files exist\"\"\"\n    print(\"\\n📁 Testing project structure...\")\n    \n    required_files = [\n        \"app.py\",\n        \"main.py\", \n        \"planner.py\",\n        \"search.py\",\n        \"writer.py\",\n        \"config.py\",\n        \"utils.py\",\n        \".env\",\n        \"requirements.txt\",\n        \"graph/research_graph.py\"\n    ]\n    \n    missing_files = []\n    for file_path in required_files:\n        if not Path(file_path).exists():\n            missing_files.append(file_path)\n        else:\n            print(f\"✅ {file_path}\")\n    \n    if missing_files:\n        print(f\"❌ Missing files: {missing_files}\")\n        return False\n    \n    return True\n\ndef test_env_file():\n    \"\"\"Test if .env file is properly configured\"\"\"\n    print(\"\\n🔧 Testing environment configuration...\")\n    \n    from dotenv import load_dotenv\n    load_dotenv()\n    \n    tavily_key = os.getenv(\"TAVILY_API_KEY\")\n    if not tavily_key or tavily_key == \"your_tavily_api_key_here\":\n        print(\"⚠️  Tavily API key not configured in .env file\")\n        return False\n    else:\n        print(\"✅ Tavily API key configured\")\n        return True\n\ndef test_lm_studio_connection():\n    \"\"\"Test connection to LM Studio\"\"\"\n    print(\"\\n🤖 Testing LM Studio connection...\")\n    \n    try:\n        from langchain_openai import ChatOpenAI\n        from langchain_core.messages import HumanMessage\n        \n        llm = ChatOpenAI(\n            openai_api_key=\"lm-studio\",\n            base_url=\"http://127.0.0.1:1234/v1\",\n            model=\"qwen2.5-7b-instruct\"\n        )\n        \n        response = llm.invoke([HumanMessage(content=\"Hello, are you working?\")])\n        \n        if response and response.content:\n            print(\"✅ LM Studio connection successful\")\n            print(f\"   Response: {response.content[:50]}...\")\n            return True\n        else:\n            print(\"❌ LM Studio responded but no content\")\n            return False\n            \n    except Exception as e:\n        print(f\"❌ LM Studio connection failed: {e}\")\n        return False\n\ndef test_tavily_connection():\n    \"\"\"Test connection to Tavily API\"\"\"\n    print(\"\\n🔍 Testing Tavily API connection...\")\n    \n    try:\n        from dotenv import load_dotenv\n        from tavily import TavilyClient\n        \n        load_dotenv()\n        tavily_key = os.getenv(\"TAVILY_API_KEY\")\n        \n        if not tavily_key or tavily_key == \"your_tavily_api_key_here\":\n            print(\"⚠️  Tavily API key not configured\")\n            return False\n        \n        client = TavilyClient(api_key=tavily_key)\n        response = client.search(\n            query=\"test search\",\n            max_results=1,\n            timeout=5\n        )\n        \n        if response and \"results\" in response:\n            print(\"✅ Tavily API connection successful\")\n            return True\n        else:\n            print(\"❌ Tavily API responded but no results\")\n            return False\n            \n    except Exception as e:\n        print(f\"❌ Tavily API connection failed: {e}\")\n        return False\n\ndef test_research_pipeline():\n    \"\"\"Test the complete research pipeline with a simple topic\"\"\"\n    print(\"\\n🔬 Testing research pipeline...\")\n    \n    try:\n        from planner import planner_agent\n        from search import search_agent\n        from writer import writer_agent\n        \n        # Test with a simple topic\n        topic = \"What is artificial intelligence?\"\n        \n        # Test planner\n        print(\"   Testing planner agent...\")\n        sub_questions = planner_agent(topic, num_subquestions=2)\n        if not sub_questions or len(sub_questions) == 0:\n            print(\"❌ Planner agent failed\")\n            return False\n        print(f\"   ✅ Generated {len(sub_questions)} sub-questions\")\n        \n        # Test search (only if Tavily is configured)\n        tavily_key = os.getenv(\"TAVILY_API_KEY\")\n        if tavily_key and tavily_key != \"your_tavily_api_key_here\":\n            print(\"   Testing search agent...\")\n            search_results = search_agent(sub_questions[:1], max_results_per_query=1)\n            if not search_results:\n                print(\"❌ Search agent failed\")\n                return False\n            print(\"   ✅ Search agent working\")\n            \n            # Test writer\n            print(\"   Testing writer agent...\")\n            content_blocks = []\n            for q, items in search_results.items():\n                content_blocks.append(q)\n                for item in items:\n                    content_blocks.append(item.get(\"content\", \"\"))\n            \n            research_text = \"\\n\".join(content_blocks)\n            final_report = writer_agent(topic, research_text)\n            \n            if not final_report:\n                print(\"❌ Writer agent failed\")\n                return False\n            print(\"   ✅ Writer agent working\")\n        else:\n            print(\"   ⚠️  Skipping search/writer tests (Tavily not configured)\")\n        \n        print(\"✅ Research pipeline test completed\")\n        return True\n        \n    except Exception as e:\n        print(f\"❌ Research pipeline test failed: {e}\")\n        return False\n\ndef main():\n    \"\"\"Run all tests\"\"\"\n    print(\"🧠 OpenDeepResearcher Test Suite\")\n    print(\"=\" * 40)\n    \n    tests = [\n        (\"Import Test\", test_imports),\n        (\"Project Structure\", test_project_structure),\n        (\"Environment Config\", test_env_file),\n        (\"LM Studio Connection\", test_lm_studio_connection),\n        (\"Tavily Connection\", test_tavily_connection),\n        (\"Research Pipeline\", test_research_pipeline)\n    ]\n    \n    results = []\n    for test_name, test_func in tests:\n        try:\n            result = test_func()\n            results.append((test_name, result))\n        except Exception as e:\n            print(f\"❌ {test_name} crashed: {e}\")\n            results.append((test_name, False))\n    \n    # Summary\n    print(\"\\n\" + \"=\" * 40)\n    print(\"📊 Test Results Summary:\")\n    \n    passed = 0\n    for test_name, result in results:\n        status = \"✅ PASS\" if result else \"❌ FAIL\"\n        print(f\"   {test_name}: {status}\")\n        if result:\n            passed += 1\n    \n    print(f\"\\n🎯 {passed}/{len(results)} tests passed\")\n    \n    if passed == len(results):\n        print(\"🎉 All tests passed! System is ready to use.\")\n        print(\"   Run: streamlit run app.py\")\n    else:\n        print(\"⚠️  Some tests failed. Check the issues above.\")\n\nif __name__ == \"__main__\":\n    main()"}]
#!/usr/bin/env python3
"""
Test script for OpenDeepResearcher
Runs basic functionality tests to ensure system is working
"""

import os
from pathlib import Path


def test_imports():
    """Test if all required modules can be imported"""
    print("🧪 Testing imports...")

    try:
        import streamlit
        print("✅ Streamlit imported")
    except ImportError as e:
        print(f"❌ Streamlit import failed: {e}")
        return False

    try:
        from langchain_openai import ChatOpenAI
        from langchain_core.messages import HumanMessage
        print("✅ LangChain imported")
    except ImportError as e:
        print(f"❌ LangChain import failed: {e}")
        return False

    try:
        from tavily import TavilyClient
        print("✅ Tavily imported")
    except ImportError as e:
        print(f"❌ Tavily import failed: {e}")
        return False

    try:
        from dotenv import load_dotenv
        print("✅ Python-dotenv imported")
    except ImportError as e:
        print(f"❌ Python-dotenv import failed: {e}")
        return False

    return True


def test_project_structure():
    """Test if all required files exist"""
    print("\n📁 Testing project structure...")

    required_files = [
        "app.py",
        "main.py",
        "planner.py",
        "search.py",
        "writer.py",
        "config.py",
        "utils.py",
        ".env",
        "requirements.txt",
        "graph/research_graph.py",
    ]

    missing = []
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            missing.append(file_path)

    if missing:
        print(f"❌ Missing files: {missing}")
        return False

    return True


def test_env_file():
    """Test if .env file is properly configured"""
    print("\n🔧 Testing environment configuration...")

    from dotenv import load_dotenv

    load_dotenv()

    tavily_key = os.getenv("TAVILY_API_KEY")
    if not tavily_key or tavily_key == "your_tavily_api_key_here":
        print("⚠️  Tavily API key not configured in .env file")
        return False

    print("✅ Tavily API key configured")
    return True


def test_lm_studio_connection():
    """Test connection to LM Studio"""
    print("\n🤖 Testing LM Studio connection...")

    try:
        from langchain_openai import ChatOpenAI
        from langchain_core.messages import HumanMessage

        llm = ChatOpenAI(
            openai_api_key="lm-studio",
            base_url="http://127.0.0.1:1234/v1",
            model="qwen2.5-7b-instruct",
        )

        response = llm.invoke(
            [HumanMessage(content="Hello, are you working?")]
        )

        if response and response.content:
            print("✅ LM Studio connection successful")
            print(f"   Response: {response.content[:60]}...")
            return True

        print("❌ LM Studio responded but returned no content")
        return False

    except Exception as e:
        print(f"❌ LM Studio connection failed: {e}")
        return False


def test_tavily_connection():
    """Test connection to Tavily API"""
    print("\n🔍 Testing Tavily API connection...")

    try:
        from dotenv import load_dotenv
        from tavily import TavilyClient

        load_dotenv()
        tavily_key = os.getenv("TAVILY_API_KEY")

        if not tavily_key or tavily_key == "your_tavily_api_key_here":
            print("⚠️  Tavily API key not configured")
            return False

        client = TavilyClient(api_key=tavily_key)
        response = client.search(
            query="test search",
            max_results=1,
            timeout=5,
        )

        if response and "results" in response:
            print("✅ Tavily API connection successful")
            return True

        print("❌ Tavily API responded but no results")
        return False

    except Exception as e:
        print(f"❌ Tavily API connection failed: {e}")
        return False


def test_research_pipeline():
    """Test the complete research pipeline with a simple topic"""
    print("\n🔬 Testing research pipeline...")

    try:
        from planner import planner_agent
        from search import search_agent
        from writer import writer_agent

        topic = "What is artificial intelligence?"

        print("   Testing planner agent...")
        sub_questions = planner_agent(topic, num_subquestions=2)
        if not sub_questions:
            print("❌ Planner agent failed")
            return False
        print(f"   ✅ Generated {len(sub_questions)} sub-questions")

        tavily_key = os.getenv("TAVILY_API_KEY")
        if tavily_key and tavily_key != "your_tavily_api_key_here":
            print("   Testing search agent...")
            search_results = search_agent(
                sub_questions[:1], max_results_per_query=1
            )
            if not search_results:
                print("❌ Search agent failed")
                return False
            print("   ✅ Search agent working")

            print("   Testing writer agent...")
            content_blocks = []
            for q, items in search_results.items():
                content_blocks.append(q)
                for item in items:
                    content_blocks.append(item.get("content", ""))

            research_text = "\n".join(content_blocks)
            final_report = writer_agent(topic, research_text)

            if not final_report:
                print("❌ Writer agent failed")
                return False
            print("   ✅ Writer agent working")
        else:
            print("   ⚠️  Skipping search/writer tests (Tavily not configured)")

        print("✅ Research pipeline test completed")
        return True

    except Exception as e:
        print(f"❌ Research pipeline test failed: {e}")
        return False


def main():
    """Run all tests"""
    print("🧠 OpenDeepResearcher Test Suite")
    print("=" * 40)

    tests = [
        ("Import Test", test_imports),
        ("Project Structure", test_project_structure),
        ("Environment Config", test_env_file),
        ("LM Studio Connection", test_lm_studio_connection),
        ("Tavily Connection", test_tavily_connection),
        ("Research Pipeline", test_research_pipeline),
    ]

    results = []
    for name, test in tests:
        try:
            results.append((name, test()))
        except Exception as e:
            print(f"❌ {name} crashed: {e}")
            results.append((name, False))

    print("\n" + "=" * 40)
    print("📊 Test Results Summary:")

    passed = 0
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {name}: {status}")
        if result:
            passed += 1

    print(f"\n🎯 {passed}/{len(results)} tests passed")

    if passed == len(results):
        print("🎉 All tests passed! System is ready to use.")
        print("   Run: streamlit run app.py")
    else:
        print("⚠️  Some tests failed. Check the issues above.")


if __name__ == "__main__":
    main()

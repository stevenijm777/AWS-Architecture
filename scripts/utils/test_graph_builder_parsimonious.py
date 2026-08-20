#!/usr/bin/env python3
"""
test_graph_builder_parsimonious.py — Test script to verify graph building for both Schema A and B.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

# Fix Windows console encoding issues for Unicode characters
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

from scripts.core.graph_builder import create_graph_from_cloudscape_json

def test_schema_a():
    file_path = PROJECT_ROOT / "data" / "raw" / "6CgqEzyWpeA_vision_analysis_parsimonious.json"
    print(f"Testing Schema A file: {file_path}")
    
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    G = create_graph_from_cloudscape_json(data, video_id="6CgqEzyWpeA", video_url="https://www.youtube.com/watch?v=6CgqEzyWpeA")
    
    # Assert nodes and edges counts
    assert G.number_of_nodes() > 0, "Schema A should have more than 0 nodes"
    assert G.number_of_edges() > 0, "Schema A should have more than 0 edges"
    assert G.graph["link"] == "https://www.youtube.com/watch?v=6CgqEzyWpeA", "Link attribute was not overwritten correctly"
    
    print(f"✓ Schema A success! Generated graph with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")

def test_schema_b():
    file_path = PROJECT_ROOT / "data" / "raw" / "FHdtOtznWuA_vision_analysis_parsimonious.json"
    print(f"Testing Schema B file: {file_path}")
    
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    G = create_graph_from_cloudscape_json(data, video_id="FHdtOtznWuA", video_url="https://www.youtube.com/watch?v=FHdtOtznWuA")
    
    # Assert nodes count is 9
    assert G.number_of_nodes() == 9, f"Schema B should have exactly 9 nodes, found {G.number_of_nodes()}"
    assert G.number_of_edges() == 5, f"Schema B should have exactly 5 edges, found {G.number_of_edges()}"
    
    # Check that metadata attributes are preserved
    assert G.graph["video_id"] == "FHdtOtznWuA"
    assert G.graph["prompt_version"] == "v9"
    assert G.graph["model"] == "gemini-3.6-flash"
    assert G.graph["link"] == "https://www.youtube.com/watch?v=FHdtOtznWuA"
    
    # Check normalization of names
    services = [attrs.get("service") for _, attrs in G.nodes(data=True)]
    print(f"Extracted services: {services}")
    
    # Expected normalized service names
    assert "ServerlessApplicationRepository" in services, "ServerlessApplicationRepository should be normalized (no spaces)"
    assert "ApiGateway" in services, "API Gateway should be normalized to ApiGateway"
    assert "IoTCore" in services, "IoT Core should be normalized to IoTCore"
    assert "Greengrass" in services, "IoT Greengrass should be normalized to Greengrass"
    assert "UserConsumerWebMobile" in services, "UserConsumerWebMobile should stay unmodified"
    
    # Verify no spaces in AWS service names
    for s in services:
        if s != "UserConsumerWebMobile":
            assert " " not in s, f"Service name '{s}' has spaces"
            
    print(f"✓ Schema B success! Generated graph with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")

def main():
    try:
        test_schema_a()
        print("-" * 50)
        test_schema_b()
        print("=" * 50)
        print("🎉 ALL TESTS PASSED SUCCESSFULLY!")
        print("=" * 50)
    except AssertionError as e:
        print(f"❌ Test verification failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

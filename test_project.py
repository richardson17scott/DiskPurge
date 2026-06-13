import pytest
import os
from project import scanner, display_largest_files, display_extension_breakdown

@pytest.fixture
def mock_file_list():
    return [("/workspace/project/movie.mp4", 55000000),
            ("/workapace/project/archive.zip", 22000000),
            ("/workspace/project/notes.md", 1024),
            ("/workspace/project/image.jpg", 512000)
            ]

def test_scanner_invalid():
    with pytest.raises(SystemExit):
        scanner("my/cs50/python")

def test_display_largest(mock_file_list):
    result = display_largest_files(mock_file_list, limit=2)
    assert len(result) == 2
    assert result[0][0] == "/workspace/project/movie.mp4"
    assert result[1][0] == "/workapace/project/archive.zip"

def test_display_extension(mock_file_list):
    try:
        display_extension_breakdown(mock_file_list, limit= 5)
    except Exception as error:
        pytest.fail(f"display_extension_breakdown raised an unexpected exception: {error}")




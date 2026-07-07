import pytest
from memtomem.utils.llm_utils import strip_llm_response

class TestStripLLMResponse:
    """Tests for strip_llm_response function."""

    def test_plain_text(self):
        """Test that plain text is returned unchanged."""
        text = "Hello, world!"
        assert strip_llm_response(text) == text

    def test_code_block_without_language(self):
        """Test that a code block without language is stripped."""
        text = "```\nprint('hello')\n```"
        expected = "print('hello')"
        assert strip_llm_response(text) == expected

    def test_code_block_with_language(self):
        """Test that a code block with language is stripped."""
        text = "```python\nprint('hello')\n```"
        expected = "print('hello')"
        assert strip_llm_response(text) == expected

    def test_code_block_with_extra_text(self):
        """Test that a code block with extra text is stripped."""
        text = "Here is the code:\n```python\nprint('hello')\n```\nThat's all."
        expected = "Here is the code:\nprint('hello')\nThat's all."
        assert strip_llm_response(text) == expected

    def test_unclosed_code_block(self):
        """Test that an unclosed code block is handled."""
        text = "```python\nprint('hello')\n"
        expected = "print('hello')\n"
        assert strip_llm_response(text) == expected

    def test_empty_string(self):
        """Test that an empty string returns empty."""
        assert strip_llm_response("") == ""

    def test_whitespace_only(self):
        """Test that whitespace-only input returns whitespace."""
        text = "   "
        assert strip_llm_response(text) == text

    def test_code_block_with_backticks_in_text(self):
        """Test that backticks in the middle of text are handled."""
        text = "Use `print('hello')` to print."
        expected = "Use `print('hello')` to print."
        assert strip_llm_response(text) == expected

    def test_mixed_content(self):
        """Test that mixed content is handled correctly."""
        text = "Text\n```python\nprint('hello')\n```\nMore text"
        expected = "Text\nprint('hello')\nMore text"
        assert strip_llm_response(text) == expected
from types import SimpleNamespace

import app.ask as ask_mod


def test_ask_prints_input_and_output_token_counts(monkeypatch, capsys):
    response = SimpleNamespace(
        text="こんにちは",
        usage_metadata=SimpleNamespace(prompt_token_count=12, candidates_token_count=5),
    )

    class DummyModels:
        def generate_content(self, model, contents):
            assert model == ask_mod.MODEL
            assert contents == "hello"
            return response

    class DummyClient:
        def __init__(self, api_key):
            self.api_key = api_key
            self.models = DummyModels()

    monkeypatch.setattr(ask_mod, "get_api_key", lambda: "test-key")
    monkeypatch.setattr(ask_mod.genai, "Client", lambda api_key: DummyClient(api_key))

    result = ask_mod.ask("hello")

    captured = capsys.readouterr().out
    assert result == "こんにちは"
    assert "[input tokens] 12" in captured
    assert "[output tokens] 5" in captured

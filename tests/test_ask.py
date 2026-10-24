from types import SimpleNamespace

import app.ask as ask_module


def _mock_client(monkeypatch, response):
    client = SimpleNamespace(
        models=SimpleNamespace(generate_content=lambda **kwargs: response)
    )
    monkeypatch.setattr(ask_module.genai, "Client", lambda api_key: client)
    monkeypatch.setattr(ask_module, "get_api_key", lambda: "test-key")


def test_ask_prints_input_and_output_token_counts(monkeypatch, capsys):
    response = SimpleNamespace(
        usage_metadata=SimpleNamespace(
            prompt_token_count=12,
            candidates_token_count=34,
        ),
        text="回答",
    )
    _mock_client(monkeypatch, response)

    assert ask_module.ask("質問") == "回答"
    assert "[usage] 入力トークン数: 12, 出力トークン数: 34" in capsys.readouterr().out


def test_ask_reports_missing_usage_metadata(monkeypatch, capsys):
    response = SimpleNamespace(usage_metadata=None, text="回答")
    _mock_client(monkeypatch, response)

    assert ask_module.ask("質問") == "回答"
    assert "[usage] 入力トークン数: 不明, 出力トークン数: 不明" in capsys.readouterr().out

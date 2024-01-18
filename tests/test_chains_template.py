from fastapi.testclient import TestClient

# def test_chains_settings(client: TestClient, logged_in_headers):
#     response = client.get("api/v1/all", headers=logged_in_headers)
#     assert response.status_code == 200
#     json_response = response.json()
#     chains = json_response["chains"]
#     assert set(chains.keys()) == set(settings.chains)


def test_llm_checker_chain(client: TestClient, logged_in_headers):
    response = client.get("api/v1/all", headers=logged_in_headers)
    assert response.status_code == 200
    json_response = response.json()
    chains = json_response["chains"]
    chain = chains["LLMCheckerChain"]

    # Test the base classes, template, memory, verbose, llm, input_key, output_key, and _type objects
    assert set(chain["base_classes"]) == {
        "Callable",
        "LLMCheckerChain",
        "Chain",
    }

    template = chain["template"]
    assert template["llm"] == {
        "required": True,
        "dynamic": False,
        "placeholder": "",
        "show": True,
        "multiline": False,
        "password": False,
        "name": "llm",
        "type": "BaseLanguageModel",
        "list": False,
        "advanced": False,
        "info": "",
        "fileTypes": [],
    }
    assert template["_type"] == "LLMCheckerChain"

    # Test the description object
    assert chain["description"] == ""


def test_llm_math_chain(client: TestClient, logged_in_headers):
    response = client.get("api/v1/all", headers=logged_in_headers)
    assert response.status_code == 200
    json_response = response.json()
    chains = json_response["chains"]

    chain = chains["LLMMathChain"]
    # Test the base classes, template, memory, verbose, llm, input_key, output_key, and _type objects
    assert set(chain["base_classes"]) == {
        "Callable",
        "LLMMathChain",
        "Chain",
    }

    template = chain["template"]
    assert template["memory"] == {
        "required": False,
        "dynamic": False,
        "placeholder": "",
        "show": True,
        "multiline": False,
        "password": False,
        "name": "memory",
        "type": "BaseMemory",
        "list": False,
        "advanced": False,
        "info": "",
        "fileTypes": [],
    }
    assert template["verbose"] == {
        "required": False,
        "dynamic": False,
        "placeholder": "",
        "show": False,
        "multiline": False,
        "value": False,
        "password": False,
        "name": "verbose",
        "type": "bool",
        "list": False,
        "advanced": True,
        "info": "",
        "fileTypes": [],
    }
    assert template["llm"] == {
        "required": True,
        "dynamic": False,
        "placeholder": "",
        "show": True,
        "multiline": False,
        "password": False,
        "name": "llm",
        "type": "BaseLanguageModel",
        "list": False,
        "advanced": False,
        "info": "",
        "fileTypes": [],
    }
    assert template["input_key"] == {
        "required": True,
        "dynamic": False,
        "placeholder": "",
        "show": True,
        "multiline": False,
        "value": "question",
        "password": False,
        "name": "input_key",
        "type": "str",
        "list": False,
        "advanced": True,
        "info": "",
        "fileTypes": [],
    }
    assert template["output_key"] == {
        "required": True,
        "dynamic": False,
        "placeholder": "",
        "show": True,
        "multiline": False,
        "value": "answer",
        "password": False,
        "name": "output_key",
        "type": "str",
        "list": False,
        "advanced": True,
        "info": "",
        "fileTypes": [],
    }
    assert template["_type"] == "LLMMathChain"

    # Test the description object
    assert chain["description"] == "Chain that interprets a prompt and executes python code to do math."


def test_series_character_chain(client: TestClient, logged_in_headers):
    response = client.get("api/v1/all", headers=logged_in_headers)
    assert response.status_code == 200
    json_response = response.json()
    chains = json_response["chains"]

    chain = chains["SeriesCharacterChain"]

    # Test the base classes, template, memory, verbose, llm, input_key, output_key, and _type objects
    assert set(chain["base_classes"]) == {
        "Callable",
        "LLMChain",
        "BaseCustomChain",
        "Chain",
        "ConversationChain",
        "SeriesCharacterChain",
    }
    template = chain["template"]

    assert template["llm"] == {
        "required": True,
        "dynamic": False,
        "display_name": "LLM",
        "placeholder": "",
        "show": True,
        "multiline": False,
        "password": False,
        "name": "llm",
        "type": "BaseLanguageModel",
        "list": False,
        "advanced": False,
        "info": "",
        "fileTypes": [],
        "file_path": "",
        "value": "",
    }
    assert template["character"] == {
        "required": True,
        "dynamic": False,
        "placeholder": "",
        "show": True,
        "multiline": False,
        "password": False,
        "name": "character",
        "type": "str",
        "list": False,
        "advanced": False,
        "info": "",
        "fileTypes": [],
        "file_path": "",
        "value": "",
    }
    assert template["series"] == {
        "required": True,
        "dynamic": False,
        "placeholder": "",
        "show": True,
        "multiline": False,
        "password": False,
        "name": "series",
        "type": "str",
        "list": False,
        "advanced": False,
        "info": "",
        "fileTypes": [],
        "file_path": "",
        "value": "",
    }
    assert template["_type"] == "SeriesCharacterChain"

    # Test the description object
    assert (
        chain["description"]
        == "SeriesCharacterChain is a chain you can use to have a conversation with a character from a series."
    )


def test_mid_journey_prompt_chain(client: TestClient, logged_in_headers):
    response = client.get("api/v1/all", headers=logged_in_headers)
    assert response.status_code == 200
    json_response = response.json()
    chains = json_response["chains"]
    chain = chains["MidJourneyPromptChain"]
    assert isinstance(chain, dict)

    # Test the base_classes object
    assert set(chain["base_classes"]) == {
        "LLMChain",
        "BaseCustomChain",
        "Chain",
        "ConversationChain",
        "MidJourneyPromptChain",
    }

    # Test the template object
    template = chain["template"]

    assert template["llm"] == {
        "required": True,
        "dynamic": False,
        "display_name": "LLM",
        "placeholder": "",
        "show": True,
        "multiline": False,
        "password": False,
        "name": "llm",
        "type": "BaseLanguageModel",
        "list": False,
        "advanced": False,
        "info": "",
        "file_path": "",
        "fileTypes": [],
        "value": "",
    }
    # Test the description object
    assert chain["description"] == "MidJourneyPromptChain is a chain you can use to generate new MidJourney prompts."


def test_time_travel_guide_chain(client: TestClient, logged_in_headers):
    response = client.get("api/v1/all", headers=logged_in_headers)
    assert response.status_code == 200
    json_response = response.json()
    chains = json_response["chains"]
    chain = chains["TimeTravelGuideChain"]
    assert isinstance(chain, dict)

    # Test the base_classes object
    assert set(chain["base_classes"]) == {
        "LLMChain",
        "BaseCustomChain",
        "TimeTravelGuideChain",
        "Chain",
        "ConversationChain",
    }

    # Test the template object
    template = chain["template"]

    assert template["llm"] == {
        "required": True,
        "dynamic": False,
        "placeholder": "",
        "display_name": "LLM",
        "show": True,
        "multiline": False,
        "password": False,
        "name": "llm",
        "type": "BaseLanguageModel",
        "list": False,
        "advanced": False,
        "info": "",
        "file_path": "",
        "fileTypes": [],
        "value": "",
    }
    assert template["memory"] == {
        "required": False,
        "dynamic": False,
        "placeholder": "",
        "show": True,
        "multiline": False,
        "password": False,
        "name": "memory",
        "type": "BaseChatMemory",
        "list": False,
        "advanced": False,
        "info": "",
        "file_path": "",
        "fileTypes": [],
        "value": "",
    }

    assert chain["description"] == "Time travel guide chain."

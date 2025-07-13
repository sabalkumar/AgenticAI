import json
import os
import gradio as gr
from dotenv import load_dotenv
from openai import OpenAI
import operator
from typing import Callable, Generator, Iterable, List, Mapping, Any
import re

import urllib


def sort_swarams_by_custom_order(swarams):
    base_order = {"SA": 0, "RI": 1, "GA": 2,
                  "MA": 3, "PA": 4, "DA": 5, "NI": 6}
    suffix_order = {"_LOWER": 0, "": 1, "_HIGHER": 2}

    pattern = re.compile(r"^(SA|RI|GA|MA|PA|DA|NI)(\d?)(_LOWER|_HIGHER)?$")

    def extract_sort_key(entry):
        # If entry is a string, use it directly; otherwise, get from dict
        name = entry if isinstance(entry, str) else entry.get("name", "")
        name = name.upper()

        match = pattern.match(name)
        if not match:
            return (999, 999, 999)  # unknowns go last

        base, variant, suffix = match.groups()
        base_rank = base_order.get(base, 999)
        suffix_rank = suffix_order.get(suffix or "", 1)
        variant_rank = int(variant) if variant else 0
        return (suffix_rank, base_rank, variant_rank)

    return sorted(swarams, key=extract_sort_key)


# ----------------------------------------------------------------------
# Shared operator registry and resolver
# ----------------------------------------------------------------------
_OPS: dict[str, Callable[[Any, Any], bool]] = {
    "==": operator.eq,
    "!=": operator.ne,
    "<":  operator.lt,
    "<=": operator.le,
    ">":  operator.gt,
    ">=": operator.ge,
    "in": lambda lhs, rhs: lhs in rhs,
    "contains": lambda lhs, rhs: (
        all(item in lhs for item in rhs)
        if isinstance(rhs, (list, tuple, set, frozenset))
        else rhs in lhs
    ),
}


def _resolve(op: str | Callable[[Any, Any], bool]) -> Callable[[Any, Any], bool]:
    if callable(op):
        return op
    try:
        return _OPS[op]
    except KeyError:
        raise ValueError(f"Unsupported operator: {op!r}") from None

# ----------------------------------------------------------------------
# Helper: fetch a value no matter where it is nested
# ----------------------------------------------------------------------


def _get_nested_value(obj: Any, field: str) -> Any:
    """
    • Supports dotted paths like "signature.aarohanam".
    • If no dots are given, searches *recursively* for a key
      with that name and returns the first match.
    • Returns [] (empty list) when the key can’t be found
      so that “contains” still works safely.
    """
    # 1)  dotted‑path lookup  ------------------------------------------
    if "." in field:
        for part in field.split("."):
            if isinstance(obj, Mapping) and part in obj:
                obj = obj[part]
            else:
                return []          # path breaks ⇒ treat as “nothing here”
        return obj

    # 2)  recursive scan (simple key)  ---------------------------------
    if isinstance(obj, Mapping):
        if field in obj:
            return obj[field]
        for v in obj.values():
            got = _get_nested_value(v, field)
            if got != []:
                return got
    elif isinstance(obj, (list, tuple, set, frozenset)):
        for v in obj:
            got = _get_nested_value(v, field)
            if got != []:
                return got
    return []                       # not found anywhere


def show_ragams_in_chakra(chakra: str):
    ragams = query_collection("ragams", "chakra", "==", chakra)
    if not ragams:
        return []
    print(f"*****Ragams in chakra {chakra}:")
    # print(ragams)
    return ragams[:20]


def play_ragam_aarohanam(ragam: str):
    ragams = query_collection("ragams", "name", "==", ragam)
    if not ragams:
        return None
    swarams = ragams[0]["signature"]["aarohanam"]
    swarams = sort_swarams_by_custom_order(swarams)
    return play_swarams(swarams)


def play_ragam_avarohanam(ragam: str):
    ragams = query_collection("ragams", "name", "==", ragam)
    if not ragams:
        return None
    swarams = ragams[0]["signature"]["avarohanam"]
    swarams = sort_swarams_by_custom_order(swarams)
    return play_swarams(swarams)

# ----------------------------------------------------------------------
# 1‑filter version (unchanged, for reference)
# ----------------------------------------------------------------------


def query_collection(collectionName: str,
                     field: str | None = None,
                     op: str | Callable[[Any, Any], bool] | None = None,
                     value: Any | None = None):
    collection: Iterable[Mapping[str, Any]] = read_file_as_json_array(
        collectionName, f"data/{collectionName}.json")

    if not op:
        return collection[:20]

    cmp = _resolve(op)
    return [
        item
        for item in collection
        if cmp(_get_nested_value(item, field), value)
    ]


# ----------------------------------------------------------------------
# NEW: multi‑filter counter
# ----------------------------------------------------------------------
def count_documents(collectionName: str,
                    filters: List[Mapping[str, Any] | None] = None) -> int:
    """
    *filters* is a list/tuple of dict‑like objects with keys:
        • field  – str
        • op     – str key in _OPS **or** a custom 2‑arg callable
        • value  – value to compare against

    All filters are AND‑ed together (an item must satisfy every filter).
    """
    collection: Iterable[Mapping[str, Any]] = read_file_as_json_array(
        collectionName, f"data/{collectionName}.json")

    # Pre‑compute each filter as (field, cmp‑function, value)
    compiled = [(f["field"], _resolve(f["op"]), f["value"])
                for f in filters] if filters else []

    def matches(item):
        return all(cmp(item[field] if field in item else None, value) for field, cmp, value in compiled)

    return sum(1 for item in collection if matches(item))


def read_file_as_json_array(label, fileName):
    with open(fileName, "r", encoding="utf-8") as f:
        some_str = f.read()

    json_array = json.loads(some_str)
    print(f"Number of {label} loaded = ")
    print(len(json_array))
    return json_array

# ── helper ---------------------------------------------------------------


def get_playlist(swarams):
    results = query_collection(
        "swarams", "name", "in", [s.upper() for s in swarams]
    )
    results = sort_swarams_by_custom_order(results)
    return [
        f"data/audio/swarams/c_ak_{info['fileName']}.mp3"
        for info in results
    ]


def stream_playlist(paths: List[str]) -> Generator[str, None, None]:
    """Yield one filename after another so the player keeps going."""
    for p in paths:
        yield p


def get_audio_update(swarams: list[str]):
    results = query_collection(
        "swarams", "name", "in", [s.upper() for s in swarams]
    )
    results = sort_swarams_by_custom_order(results)

    if not results:
        return None
    elif len(results) == 1:
        return f"data/audio/swarams/c_ak_{results[0]['fileName']}.mp3"
    else:
        return [
            f"data/audio/swarams/c_ak_{r['fileName']}.mp3" for r in results
        ]


def play_swarams(swarams: List):
    # play the swaram using audio library
    return get_audio_update(swarams)


def handle_tool_calls(tool_calls):
    results = []

    for tool_call in tool_calls:
        tool_name = tool_call.function.name
        tool_fn = globals().get(tool_name)
        if not tool_fn:
            print(f"⚠️ Unknown tool: {tool_name}")
            continue

        arguments = json.loads(tool_call.function.arguments)
        print(f"🔧 Invoking tool: {tool_name} with arguments:", arguments)

        try:
            result = tool_fn(**arguments)
            print(f"✅ Result from {tool_name}:", result)

            content = json.dumps(result) if result is not None else "No output"
        except Exception as e:
            print(f"❌ Tool {tool_name} failed:", str(e))
            content = "Tool failed to run"

        results.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": content
        })

    return results


def get_content(message):
    if isinstance(message, dict):
        return message.get("content")
    elif hasattr(message, "content"):
        return message.content
    return None

# ------------------------------------------------------------------
# MAIN CALLBACK  ➜ now a generator
# ------------------------------------------------------------------


def to_dict(m):
    if isinstance(m, dict):
        return m
    return m.model_dump()


# Now remove ones that are invalid (e.g., content=None and no tool_calls)
def is_valid_message(m):
    if isinstance(m["content"], str):
        return True
    if m["role"] == "assistant" and m.get("tool_calls"):
        return True
    return False


def to_openai_message(m):
    if not isinstance(m, dict):
        m = m.model_dump()

    role = m.get("role")
    result = {"role": role}

    if role == "assistant":
        # Always include content, even if it's None
        result["content"] = m.get("content")
        if m.get("tool_calls"):
            result["tool_calls"] = m["tool_calls"]

    elif role == "tool":
        result["tool_call_id"] = m.get("tool_call_id")
        result["content"] = m.get("content")

    else:
        result["content"] = m.get("content")

    return result


def clean_message_fields(message):
    return {
        k: v
        for k, v in message.items()
        # strip empty tool_calls too
        if v is not None and not (k == "tool_calls" and v == [])
    }


def chat(message, history):
    if message.startswith("action:"):
        action_line = message[len("action:"):]
        fn_name, _, query_str = action_line.partition("?")
        args = dict(urllib.parse.parse_qsl(query_str))

        print(f"🧭 Synthetic action trigger: {fn_name} with args {args}")

        tool_fn = globals().get(fn_name)
        if tool_fn:
            try:
                result = tool_fn(**args)
                if isinstance(result, list):
                    if all(isinstance(r, dict) and "name" in r for r in result):
                        formatted = "\n".join(f"- {r['name']}" for r in result)
                    else:
                        formatted = "\n".join(str(r) for r in result)
                else:
                    formatted = str(result)

                new_history = history + \
                    [{"role": "assistant", "content": formatted}]
                print("returning from yield")
                yield "", new_history, None
                return
            except Exception as e:
                new_history = history + \
                    [{"role": "assistant", "content": f"Tool failed: {e}"}]
                yield "", new_history, None
                return

        new_history = history + \
            [{"role": "assistant", "content": f"Unknown action: {fn_name}"}]
        yield "", new_history, None
        return

    # ✅ Proper dummy yield so Gradio sees a valid generator
    yield "", history, None

    chat_history = history + [{"role": "user", "content": message}]
    messages = [{"role": "system", "content": system_prompt}] + history
    messages.append({"role": "user", "content": message})

    messages = [to_dict(m) for m in messages]
    messages = [m for m in messages if is_valid_message(m)]

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=tool_specs,
        tool_choice="auto"
    )

    audio_spec = None

    if response.choices[0].finish_reason == "tool_calls":
        tool_calls = response.choices[0].message.tool_calls
        tool_responses = handle_tool_calls(tool_calls)
        messages.append({
            "role": "assistant",
            "content": None,
            "tool_calls": [tc.model_dump() for tc in response.choices[0].message.tool_calls]
        })  # correct assistant tool_call message
        # follow with your tool responses
        messages.extend(tool_responses)

        # print("🧪 Message chain before cleaning up:")
        # for i, m in enumerate(messages):
        #     print(f"{i}: {m}")

        messages = [to_openai_message(m) for m in messages]

        def is_valid_openai_message(m):
            role = m.get("role")
            if role == "assistant":
                return m.get("content") is not None or m.get("tool_calls")
            if role == "tool":
                return m.get("tool_call_id") is not None and m.get("content") is not None
            return m.get("content") is not None

        messages = [to_openai_message(m) for m in messages]
        messages = [m for m in messages if is_valid_openai_message(m)]

        # messages = [clean_message_fields(m) for m in messages]
        # messages = [m for m in messages if is_valid_message(m)]

        # print("🧾 Final messages being sent:")
        # for i, m in enumerate(messages):
        #     print(f"{i}: {m}")

        followup = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=tool_specs,
            tool_choice="auto"
        )

        chat_history.append({
            "role": "assistant",
            "content": followup.choices[0].message.content
        })

        play_calls = [
            tc for tc in tool_calls if tc.function.name in ["play_swarams", "play_ragam_aarohanam", "play_ragam_avarohanam"]
        ]

        if play_calls:
            for tc in play_calls:
                args = json.loads(tc.function.arguments)
                if tc.function.name == "play_swarams":
                    audio_spec = get_audio_update(**args)
                elif tc.function.name == "play_ragam_aarohanam":
                    audio_spec = play_ragam_aarohanam(**args)
                elif tc.function.name == "play_ragam_avarohanam":
                    audio_spec = play_ragam_avarohanam(**args)

    else:
        chat_history.append({
            "role": "assistant",
            "content": response.choices[0].message.content
        })

    # Remove the dummy yield effect with proper first output
    if audio_spec is None:
        yield "", chat_history, gr.update(visible=False)
    elif isinstance(audio_spec, str):
        yield "", chat_history, gr.update(value=audio_spec, visible=True)
    elif isinstance(audio_spec, list):
        yield "", chat_history, gr.update(value=None, visible=True)
        for track in audio_spec:
            yield "", chat_history, track

    # 👇 FINAL fallback (always yield 3 values)
    yield "", chat_history, None


load_dotenv(override=True)

tool_specs = [
    {
        "type": "function",
        "function": {
            "name": "show_ragams_in_chakra",
            "description": "Show all ragams in a specific chakra",
            "parameters": {
                "type": "object",
                "properties": {
                    "chakra": {
                        "type": "string",
                        "description": "Name of the chakra, e.g., 'Bana'"
                    }
                },
                "required": ["chakra"]
            }
        },
    },
    {
        "type": "function",
        "function": {
            "name": "play_ragam_aarohanam",
            "description": "Play the aarohanam swarams of a given ragam",
            "parameters": {
                "type": "object",
                "properties": {
                    "ragam": {
                        "type": "string",
                        "description": "Name of the ragam, e.g., 'Mohanam'"
                    }
                },
                "required": ["ragam"]
            }
        },
    },
    {
        "type": "function",
        "function": {
            "name": "play_ragam_avarohanam",
            "description": "Play the avarohanam swarams of a given ragam",
            "parameters": {
                "type": "object",
                "properties": {
                    "ragam": {
                        "type": "string",
                        "description": "Name of the ragam, e.g., 'Mohanam'"
                    }
                },
                "required": ["ragam"]
            }
        },
    },
    {
        "type": "function",
        "function": {
            "name": "query_collection",
            "description": "Run a structured filter over Firestore",
            "parameters": {
                "type": "object",
                "properties": {
                    "collectionName":   {"type": "string"},
                    "field":        {"type": "string"},
                    "op":           {"type": "string", "enum": ["==", "<", "<=", ">", ">="]},
                    "value":        {"type": "string"}
                },
                "required": ["collectionName"]
            }
        },
    },
    {
        "type": "function",
        "function": {
            "name": "vector_search",
            "description": "Semantic search over a collection using embeddings",
            "parameters": {
                "type": "object",
                "properties": {
                    "collectionName": {"type": "string"},
                    "query":      {"type": "string"},
                    "top_k":      {"type": "integer", "default": 5}
                },
                "required": ["collectionName", "query"]
            }
        },
    },
    {
        "type": "function",
        "function": {
            "name": "count_documents",
            "description": "Return how many documents satisfy optional filters",
            "parameters": {
                "type": "object",
                "properties": {
                    "collectionName": {"type": "string",
                                       "description": "Firestore collection name"},
                    "filters": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "field": {"type": "string"},
                                "op":    {"type": "string",
                                          "enum": ["==", "<", "<=", ">", ">=", "!="]},
                                "value": {}
                            },
                            "required": ["field", "op", "value"]
                        },
                        "description": "Optional list of field comparisons"
                    }
                },
                "required": ["collectionName"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "play_swarams",
            "description": "Play many swarams using streaming",
            "parameters": {
                "type": "object",
                "properties": {
                    "swarams":   {
                        "type": "array",
                        "description": "Sequence of swarams to be played, e.g. [\"SA\", \"RI1\", \"GA2\"]",
                        "items": {"type": "string"}
                    },
                },
                "required": ["swarams"]
            }
        },
    }

]


openai = OpenAI()
system_prompt = f"""You are an encyclopedia of carnatic music. Users will query you asking questions about various aspects of carnatic music.
    if the user asks about ragams or ragas, use the ragams collection from the database instead of ragas. If you already fetched the data earlier, don't again query from the database.
    If the user asks for a count, total, number of X, etc call count_documents. 
    if user asks for ragams containing some swarams X,Y,Z in aarohanam or avarohanam, use operator contains and pass an array of swarams to it as value.
    If the user asks to play swarams in the aarohanam of a ragam, use play_ragam_aarohanam with the ragam name.
    In ragams collection, the field melakartha is a boolean field. If the user asks to show melakartha ragams, make sure to use boolean true as a filter on this field instead of "true"
    If the user asks details about a particular ragam, in the response, show the chakra as a hyperlink, on click of which, call the tool using this syntax. For example, if chakra is Bana then render **[Bana Chakra](action:show_ragams_in_chakra?chakra=Bana)**.
    For swarams RI,GA,DA and NI, there are 3 variants suffixed by numbers 1,2 and 3. for example RI1,RI2, RI3 etc. So if the user misses to provide the suffix, prompt the user and ask which one they want and then proceed.
    For swaram MA, there are two variants MA1 and MA2. So if the user misses to provide the suffix, prompt the user and ask which one they want and then proceed.
    if the user asks about lessons from any ragam, use the lessons collection with ragam as filter to cater to the request.
    Using ONLY the tools query_collection, count_documents and vector_search as your datasources, please answer the questions. If you don't know the answer to a question, please say so.
    """


# demo = gr.ChatInterface(chat, type="messages")

# demo.launch()

# ----------------------------------
# Interface
# ----------------------------------
with gr.Blocks(title="Rangasudha | Carnatic Music Assistant") as demo:
    chatbot = gr.Chatbot(height=400, type="messages", value=[
                         {"role": "assistant", "content": """Namaskaram! this is Rangasudha - an AI Carnatic Music Assistant created by **[Srirangam Vikram Vasudevan](https://www.youtube.com/@onedayonepasuram6126)**."""},
                         {"role": "assistant", "content": """I am here to answer your questions on carnatic music."""},
                         {"role": "assistant", "content": """For instance, you may ask me questions like 
                          - Tell me about ragam Mohanam or
                          - play aarohanam of Mohanam or even something like
                          - show me some ragams that have RI1 and GA2 in their aarohanam.
                          - show me some ragams that are melakartha.
                          - show me some lessons from Mohanam.
                          """}
                         ])
    audio_out = gr.Audio(interactive=False, autoplay=True,
                         streaming=True, visible=False)
    textbox = gr.Textbox(placeholder="Type here and hit Enter")

    # JS: When chatbot messages are updated, inject click listeners
    def inject_js():
        return """
        () => {
            setTimeout(() => {
                const links = document.querySelectorAll("a[href^='action:']");
                links.forEach(link => {
                    link.onclick = (e) => {
                        e.preventDefault();
                        const action = link.getAttribute("href");

                        // Find the Gradio textbox (adjust selector if you renamed it)
                        const textbox = document.querySelector("textarea");

                        if (textbox) {
                            textbox.focus();
                            textbox.value = action;
                            textbox.dispatchEvent(new Event("input", { bubbles: true }));

                            // Now submit via Enter key (Gradio listens for this)
                            textbox.dispatchEvent(new KeyboardEvent("keydown", {
                                bubbles: true,
                                cancelable: true,
                                key: "Enter",
                                code: "Enter",
                                which: 13,
                                keyCode: 13
                            }));
                        } else {
                            alert("❌ Couldn't find the input box");
                        }
                    };
                });
            }, 300);
        }
        """

    # connect chat submit
    textbox.submit(
        chat,
        inputs=[textbox, chatbot],
        outputs=[textbox, chatbot, audio_out],
    )
    chatbot.change(fn=None, js=inject_js())


demo.launch()

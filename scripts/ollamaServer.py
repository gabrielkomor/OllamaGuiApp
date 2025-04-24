from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse
import ollama
import uvicorn

app = FastAPI()


def generate_stream(prompt: str, temperature: float = 0.7, num_predict: int = 256,
                    top_k: int = 40, top_p: float = 0.9):
    word_buffer = []
    incomplete = ""

    for chunk in ollama.chat(
        model='mistral',
        messages=[{'role': 'user', 'content': prompt}],
        stream=True,
        options={
            "temperature": temperature,
            "num_predict": num_predict,
            "top_k": top_k,
            "top_p": top_p
        }
    ):
        content = chunk.get('message', {}).get('content', '')
        if not content:
            continue

        incomplete += content
        words = incomplete.split()

        # jeśli ostatni znak nie był spacją, to ostatnie słowo może być niepełne
        if not incomplete.endswith(' '):
            incomplete = words.pop() if words else incomplete
        else:
            incomplete = ""

        word_buffer.extend(words)

        while len(word_buffer) >= 1:
            to_yield = ' '.join(word_buffer[:1]) + ' '
            word_buffer = word_buffer[1:]
            yield to_yield

    # Po zakończeniu – zwróć resztę słów i niepełne słowo jeśli zostało
    if word_buffer:
        yield ' '.join(word_buffer) + ' '
    if incomplete:
        yield incomplete


@app.get("/generate")
def generate(
    prompt: str,
    temperature: float = Query(0.7, ge=0.0, le=2.0),
    top_k: int = Query(40, ge=1),
    top_p: float = Query(0.9, ge=0.0, le=1.0),
    num_predict: int = Query(256, ge=1, le=2048)
):
    return StreamingResponse(
        generate_stream(prompt, temperature, num_predict, top_k, top_p),
        media_type='text/plain'
    )


def start_server():
    config = uvicorn.Config(app=app, host="127.0.0.1", port=8000, log_level="error")
    server = uvicorn.Server(config)
    server.run()

# uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="error")

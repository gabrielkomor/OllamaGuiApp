from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import ollama
import uvicorn

app = FastAPI()


def generate_stream(prompt: str):
    word_buffer = []
    incomplete = ""

    for chunk in ollama.chat(
            model='mistral',
            messages=[{'role': 'user', 'content': prompt}],
            stream=True,
            options={"num_predict": 512}  # zwiększ limit jeśli trzeba
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

        while len(word_buffer) >= 3:
            to_yield = ' '.join(word_buffer[:3]) + ' '
            word_buffer = word_buffer[3:]
            yield to_yield

    # Po zakończeniu – zwróć resztę słów i niepełne słowo jeśli zostało
    if word_buffer:
        yield ' '.join(word_buffer) + ' '
    if incomplete:
        yield incomplete


@app.get("/generate")
def generate(prompt: str):
    return StreamingResponse(generate_stream(prompt), media_type='text/plain')


def start_server():
    config = uvicorn.Config(app=app, host="127.0.0.1", port=8000, log_level="error")
    server = uvicorn.Server(config)
    server.run()

# uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="error")

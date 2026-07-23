import json

import httpx
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.config import settings

router = APIRouter(prefix="/api", tags=["Chat"])


class ChatMessage(BaseModel):
    message: str


@router.post("/chat")
async def chat(payload: ChatMessage):
    if not settings.openrouter_api_key:
        raise HTTPException(
            status_code=500,
            detail="Chave de API do OpenRouter não configurada.",
        )

    system_prompt = (
        "Você é o assistente virtual do MarkosDev, um desenvolvedor backend especializado em Python, "
        "FastAPI, Docker e Oracle Cloud. Responda de forma breve, profissional e em português brasileiro. "
        "Seu nome é MarkosBot."
    )

    async def stream_generator():
        try:
            async with httpx.AsyncClient() as client:
                async with client.stream(
                    "POST",
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {settings.openrouter_api_key}",
                        "Content-Type": "application/json",
                        "HTTP-Referer": "https://markosdev.com.br",
                        "X-Title": "MarkosDev Portfolio",
                    },
                    json={
                        "model": settings.openrouter_model,
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": payload.message},
                        ],
                        "stream": True,
                    },
                    timeout=60.0,
                ) as response:
                    if response.status_code != 200:
                        error_body = await response.aread()
                        error_msg = "Erro ao conectar com a IA."
                        try:
                            error_data = json.loads(error_body)
                            error_msg = error_data.get("error", {}).get("message", error_msg)
                        except Exception:
                            pass
                        yield f"data: {json.dumps({'content': error_msg})}\n\n"
                        yield f"data: [DONE]\n\n"
                        return

                    async for line in response.aiter_lines():
                        if line.startswith("data:"):
                            data = line[5:].strip()
                            if data == "[DONE]":
                                yield f"data: [DONE]\n\n"
                                break
                            try:
                                chunk = json.loads(data)
                                if "choices" in chunk and len(chunk["choices"]) > 0:
                                    delta = chunk["choices"][0].get("delta", {})
                                    content = delta.get("content")
                                    if content:
                                        yield f"data: {json.dumps({'content': content})}\n\n"
                            except json.JSONDecodeError:
                                continue
        except httpx.ConnectError:
            yield f"data: {json.dumps({'content': 'Erro de conexão. Verifique sua internet.'})}\n\n"
            yield f"data: [DONE]\n\n"
        except httpx.TimeoutException:
            yield f"data: {json.dumps({'content': 'A requisição expirou. Tente novamente.'})}\n\n"
            yield f"data: [DONE]\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'content': f'Erro interno: {str(e)}'})}\n\n"
            yield f"data: [DONE]\n\n"

    return StreamingResponse(stream_generator(), media_type="text/event-stream")

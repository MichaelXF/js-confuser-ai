from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from agent.main import agent
from pydantic import BaseModel
import asyncio
from typing import AsyncIterator, Generator, TypeVar
from fastapi import HTTPException
from env.main import is_development

router = APIRouter()


class GenerateResponseModel(BaseModel):
    response: str


@router.get("/v1/chat/generate")
async def generate_response(message: str) -> GenerateResponseModel:
    if not is_development():
        raise HTTPException(
            status_code=403, detail="This route is reserved for development purposes."
        )

    response = await agent.arun(message, stream=False)
    return GenerateResponseModel(response=response)


T = TypeVar("T")


def next_or_none(iterator):
    try:
        return next(iterator)
    except StopIteration:
        return None


async def async_iter_over_sync_gen(
    sync_gen: Generator[T, None, None], websocket_send_json
) -> AsyncIterator[T]:
    """
    Converts a synchronous generator into an asynchronous iterator.

    This function allows you to iterate over a synchronous generator in an
    asynchronous context without blocking the asyncio event loop. Each value
    from the synchronous generator is yielded via a coroutine, effectively
    turning it into an async iterator.

    Args:
        sync_gen: The synchronous generator to iterate over.

    Yields:
        Each value from the synchronous generator, asynchronously.
    """
    loop = asyncio.get_running_loop()
    iterator = iter(sync_gen)
    while True:
        try:
            val = await loop.run_in_executor(
                None, next_or_none, iterator
            )  # Pass iterator directly, no need for None
            if val is None:
                break

            yield val
        except StopIteration:
            break
        except Exception as e:  # Catch all errors for robustness
            if (
                "StopIteration interacts badly with generators and cannot be raised into a Future"
                in str(e)
            ):
                break

            await websocket_send_json(
                {"error": str(e)}
            )  # Notify websocket of the error
            break


@router.websocket("/v1/chat/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    messages = []

    try:
        while True:
            # At that point just use ChatGPT
            if len(messages) > 100:
                websocket.close()
                break

            # Receive a message from the client
            user_event = await websocket.receive_json()

            user_event_id = user_event["id"]
            user_message = user_event["content"]

            # Type validation
            if type(user_message) != str or type(user_event_id) != str:
                await websocket.send_json({"error": "Invalid request"})
                continue

            # Length validation
            if len(user_message) > 5000 or len(user_event_id) > 10:
                await websocket.send_json(
                    {"error": "Message is too long. Maximum length is 5000 characters."}
                )
                continue

            messages.append({"role": "user", "content": user_message})
            full_response = ""

            # Use the `phidata` agent to generate a response
            async for delta in async_iter_over_sync_gen(
                agent.run(messages=messages, stream=True), websocket.send_json
            ):
                if delta is None:
                    continue

                print(delta.content, end="")
                full_response += delta.content

                await websocket.send_json(
                    {"id": user_event_id, "content": delta.content}
                )

            # Tell websocket that generating is done
            await websocket.send_json({"done": True})

            # Add to their message history
            messages.append({"role": "assistant", "content": full_response})

            print(user_message)
            print(full_response)

    except WebSocketDisconnect:
        print("WebSocket disconnected")

    except Exception as e:
        print("An error occurred:", e)
        websocket.close()

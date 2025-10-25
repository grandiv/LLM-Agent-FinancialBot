pydantic_core.\_pydantic_core.ValidationError: 1 validation error for JSONRPCMessage
Invalid JSON: expected value at line 1 column 2 [type=json_invalid, input_value='[SearchEngine] Browser B...to try other engines...', input_type=str]
For further information visit https://errors.pydantic.dev/2.12/v/json_invalid
2025-10-25 14:17:46,055 - mcp.client.stdio - ERROR - Failed to parse JSONRPC message from server
Traceback (most recent call last):
File "C:\Projects\ai-agent\venv\Lib\site-packages\mcp\client\stdio\_\_init**.py", line 155, in stdout_reader
message = types.JSONRPCMessage.model_validate_json(line)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Projects\ai-agent\venv\Lib\site-packages\pydantic\main.py", line 766, in model_validate_json
return cls.**pydantic_validator**.validate_json(
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core.\_pydantic_core.ValidationError: 1 validation error for JSONRPCMessage
Invalid JSON: expected value at line 1 column 2 [type=json_invalid, input_value='[SearchEngine] Attempting Browser Brave (2/3)...', input_type=str]
For further information visit https://errors.pydantic.dev/2.12/v/json_invalid
2025-10-25 14:17:46,056 - mcp.client.stdio - ERROR - Failed to parse JSONRPC message from server
Traceback (most recent call last):
File "C:\Projects\ai-agent\venv\Lib\site-packages\mcp\client\stdio\_\_init**.py", line 155, in stdout_reader
message = types.JSONRPCMessage.model_validate_json(line)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Projects\ai-agent\venv\Lib\site-packages\pydantic\main.py", line 766, in model_validate_json
return cls.**pydantic_validator**.validate_json(
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core.\_pydantic_core.ValidationError: 1 validation error for JSONRPCMessage
Invalid JSON: expected value at line 1 column 2 [type=json_invalid, input_value='[SearchEngine] Trying br...th dedicated browser...', input_type=str]
For further information visit https://errors.pydantic.dev/2.12/v/json_invalid
2025-10-25 14:17:46,768 - mcp.client.stdio - ERROR - Failed to parse JSONRPC message from server
Traceback (most recent call last):
File "C:\Projects\ai-agent\venv\Lib\site-packages\mcp\client\stdio\_\_init**.py", line 155, in stdout_reader
message = types.JSONRPCMessage.model_validate_json(line)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Projects\ai-agent\venv\Lib\site-packages\pydantic\main.py", line 766, in model_validate_json
return cls.**pydantic_validator**.validate_json(
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core.\_pydantic_core.ValidationError: 1 validation error for JSONRPCMessage
Invalid JSON: expected value at line 1 column 2 [type=json_invalid, input_value='[SearchEngine] Brave sea... 1/2 with fresh browser', input_type=str]
For further information visit https://errors.pydantic.dev/2.12/v/json_invalid
2025-10-25 14:17:48,061 - mcp.client.stdio - ERROR - Failed to parse JSONRPC message from server
Traceback (most recent call last):
File "C:\Projects\ai-agent\venv\Lib\site-packages\mcp\client\stdio\_\_init**.py", line 155, in stdout_reader
message = types.JSONRPCMessage.model_validate_json(line)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Projects\ai-agent\venv\Lib\site-packages\pydantic\main.py", line 766, in model_validate_json
return cls.**pydantic_validator**.validate_json(
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core.\_pydantic_core.ValidationError: 1 validation error for JSONRPCMessage
Invalid JSON: expected value at line 1 column 2 [type=json_invalid, input_value='[SearchEngine] Browser n...esia%20price&source=web', input_type=str]
For further information visit https://errors.pydantic.dev/2.12/v/json_invalid
2025-10-25 14:17:48 WARNING discord.gateway Shard ID None heartbeat blocked for more than 10 seconds.
Loop thread traceback (most recent call last):
File "C:\Projects\ai-agent\bot.py", line 225, in <module>
main()
File "C:\Projects\ai-agent\bot.py", line 214, in main
bot.run(discord_token)
File "C:\Projects\ai-agent\venv\Lib\site-packages\discord\client.py", line 929, in run
asyncio.run(runner())
File "C:\Python312\Lib\asyncio\runners.py", line 194, in run
return runner.run(main)
File "C:\Python312\Lib\asyncio\runners.py", line 118, in run
return self.\_loop.run_until_complete(task)
File "C:\Python312\Lib\asyncio\base_events.py", line 674, in run_until_complete
self.run_forever()
File "C:\Python312\Lib\asyncio\windows_events.py", line 322, in run_forever
super().run_forever()
File "C:\Python312\Lib\asyncio\base_events.py", line 641, in run_forever
self.\_run_once()
File "C:\Python312\Lib\asyncio\base_events.py", line 1987, in \_run_once
handle.\_run()
File "C:\Python312\Lib\asyncio\events.py", line 88, in \_run
self.\_context.run(self.\_callback, *self.\_args)
File "C:\Projects\ai-agent\venv\Lib\site-packages\discord\client.py", line 504, in \_run_event
await coro(*args, \*\*kwargs)
File "C:\Projects\ai-agent\bot.py", line 126, in on_message
response = self.bot_core.process_message(user_id, username, content)
File "C:\Projects\ai-agent\core\bot_core.py", line 122, in process_message
return self.\_handle_search_price(result)
File "C:\Projects\ai-agent\core\bot_core.py", line 475, in \_handle_search_price
mcp_result = future.result()
File "C:\Python312\Lib\concurrent\futures_base.py", line 451, in result
self.\_condition.wait(timeout)
File "C:\Python312\Lib\threading.py", line 355, in wait
waiter.acquire()

2025-10-25 14:17:48,227 - discord.gateway - WARNING - Shard ID None heartbeat blocked for more than 10 seconds.
Loop thread traceback (most recent call last):
File "C:\Projects\ai-agent\bot.py", line 225, in <module>
main()
File "C:\Projects\ai-agent\bot.py", line 214, in main
bot.run(discord_token)
File "C:\Projects\ai-agent\venv\Lib\site-packages\discord\client.py", line 929, in run
asyncio.run(runner())
File "C:\Python312\Lib\asyncio\runners.py", line 194, in run
return runner.run(main)
File "C:\Python312\Lib\asyncio\runners.py", line 118, in run
return self.\_loop.run_until_complete(task)
File "C:\Python312\Lib\asyncio\base_events.py", line 674, in run_until_complete
self.run_forever()
File "C:\Python312\Lib\asyncio\windows_events.py", line 322, in run_forever
super().run_forever()
File "C:\Python312\Lib\asyncio\base_events.py", line 641, in run_forever
self.\_run_once()
File "C:\Python312\Lib\asyncio\base_events.py", line 1987, in \_run_once
handle.\_run()
File "C:\Python312\Lib\asyncio\events.py", line 88, in \_run
self.\_context.run(self.\_callback, *self.\_args)
File "C:\Projects\ai-agent\venv\Lib\site-packages\discord\client.py", line 504, in \_run_event
await coro(*args, \*\*kwargs)
File "C:\Projects\ai-agent\bot.py", line 126, in on_message
response = self.bot_core.process_message(user_id, username, content)
File "C:\Projects\ai-agent\core\bot_core.py", line 122, in process_message
return self.\_handle_search_price(result)
File "C:\Projects\ai-agent\core\bot_core.py", line 475, in \_handle_search_price
mcp_result = future.result()
File "C:\Python312\Lib\concurrent\futures_base.py", line 451, in result
self.\_condition.wait(timeout)
File "C:\Python312\Lib\threading.py", line 355, in wait
waiter.acquire()

2025-10-25 14:17:53,262 - mcp.client.stdio - ERROR - Failed to parse JSONRPC message from server
Traceback (most recent call last):
File "C:\Projects\ai-agent\venv\Lib\site-packages\mcp\client\stdio\_\_init**.py", line 155, in stdout_reader
message = types.JSONRPCMessage.model_validate_json(line)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Projects\ai-agent\venv\Lib\site-packages\pydantic\main.py", line 766, in model_validate_json
return cls.**pydantic_validator**.validate_json(
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core.\_pydantic_core.ValidationError: 1 validation error for JSONRPCMessage
Invalid JSON: expected value at line 1 column 2 [type=json_invalid, input_value='[SearchEngine] Brave sea... 2/2 with fresh browser', input_type=str]
For further information visit https://errors.pydantic.dev/2.12/v/json_invalid
2025-10-25 14:17:54,357 - mcp.client.stdio - ERROR - Failed to parse JSONRPC message from server
Traceback (most recent call last):
File "C:\Projects\ai-agent\venv\Lib\site-packages\mcp\client\stdio\_\_init**.py", line 155, in stdout_reader
message = types.JSONRPCMessage.model_validate_json(line)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Projects\ai-agent\venv\Lib\site-packages\pydantic\main.py", line 766, in model_validate_json
return cls.**pydantic_validator**.validate_json(
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core.\_pydantic_core.ValidationError: 1 validation error for JSONRPCMessage
Invalid JSON: expected value at line 1 column 2 [type=json_invalid, input_value='[SearchEngine] Browser n...esia%20price&source=web', input_type=str]
For further information visit https://errors.pydantic.dev/2.12/v/json_invalid
2025-10-25 14:17:56,339 - mcp.client.stdio - ERROR - Failed to parse JSONRPC message from server
Traceback (most recent call last):
File "C:\Projects\ai-agent\venv\Lib\site-packages\mcp\client\stdio\_\_init**.py", line 155, in stdout_reader
message = types.JSONRPCMessage.model_validate_json(line)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Projects\ai-agent\venv\Lib\site-packages\pydantic\main.py", line 766, in model_validate_json
return cls.**pydantic_validator**.validate_json(
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core.\_pydantic_core.ValidationError: 1 validation error for JSONRPCMessage
Invalid JSON: expected value at line 1 column 2 [type=json_invalid, input_value='[SearchEngine] Browser B...TML with length: 210071', input_type=str]
For further information visit https://errors.pydantic.dev/2.12/v/json_invalid
2025-10-25 14:17:56,340 - mcp.client.stdio - ERROR - Failed to parse JSONRPC message from server
Traceback (most recent call last):
File "C:\Projects\ai-agent\venv\Lib\site-packages\mcp\client\stdio\_\_init**.py", line 155, in stdout_reader
message = types.JSONRPCMessage.model_validate_json(line)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Projects\ai-agent\venv\Lib\site-packages\pydantic\main.py", line 766, in model_validate_json
return cls.**pydantic_validator**.validate_json(
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core.\_pydantic_core.ValidationError: 1 validation error for JSONRPCMessage
Invalid JSON: expected value at line 1 column 2 [type=json_invalid, input_value='[SearchEngine] Parsing B...TML with length: 210071', input_type=str]
For further information visit https://errors.pydantic.dev/2.12/v/json_invalid
2025-10-25 14:17:56,413 - mcp.client.stdio - ERROR - Failed to parse JSONRPC message from server
Traceback (most recent call last):
File "C:\Projects\ai-agent\venv\Lib\site-packages\mcp\client\stdio\_\_init**.py", line 155, in stdout_reader
message = types.JSONRPCMessage.model_validate_json(line)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Projects\ai-agent\venv\Lib\site-packages\pydantic\main.py", line 766, in model_validate_json
return cls.**pydantic_validator**.validate_json(
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core.\_pydantic_core.ValidationError: 1 validation error for JSONRPCMessage
Invalid JSON: expected value at line 1 column 2 [type=json_invalid, input_value='[SearchEngine] Trying Br...ctor: [data-type="web"]', input_type=str]
For further information visit https://errors.pydantic.dev/2.12/v/json_invalid
2025-10-25 14:17:56,414 - mcp.client.stdio - ERROR - Failed to parse JSONRPC message from server
Traceback (most recent call last):
File "C:\Projects\ai-agent\venv\Lib\site-packages\mcp\client\stdio\_\_init**.py", line 155, in stdout_reader
message = types.JSONRPCMessage.model_validate_json(line)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Projects\ai-agent\venv\Lib\site-packages\pydantic\main.py", line 766, in model_validate_json
return cls.**pydantic_validator**.validate_json(
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core.\_pydantic_core.ValidationError: 1 validation error for JSONRPCMessage
Invalid JSON: expected value at line 1 column 2 [type=json_invalid, input_value='[SearchEngine] Found 20 ...ector [data-type="web"]', input_type=str]
For further information visit https://errors.pydantic.dev/2.12/v/json_invalid
2025-10-25 14:17:56,415 - mcp.client.stdio - ERROR - Failed to parse JSONRPC message from server
Traceback (most recent call last):
File "C:\Projects\ai-agent\venv\Lib\site-packages\mcp\client\stdio\_\_init**.py", line 155, in stdout_reader
message = types.JSONRPCMessage.model_validate_json(line)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Projects\ai-agent\venv\Lib\site-packages\pydantic\main.py", line 766, in model_validate_json
return cls.**pydantic_validator**.validate_json(
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core.\_pydantic_core.ValidationError: 1 validation error for JSONRPCMessage
Invalid JSON: expected value at line 1 column 2 [type=json_invalid, input_value='[SearchEngine] Brave fou... Updates - Assuredzone"', input_type=str]
For further information visit https://errors.pydantic.dev/2.12/v/json_invalid
2025-10-25 14:17:56,416 - mcp.client.stdio - ERROR - Failed to parse JSONRPC message from server
Traceback (most recent call last):
File "C:\Projects\ai-agent\venv\Lib\site-packages\mcp\client\stdio\_\_init**.py", line 155, in stdout_reader
message = types.JSONRPCMessage.model_validate_json(line)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Projects\ai-agent\venv\Lib\site-packages\pydantic\main.py", line 766, in model_validate_json
return cls.**pydantic_validator**.validate_json(
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core.\_pydantic_core.ValidationError: 1 validation error for JSONRPCMessage
Invalid JSON: expected value at line 1 column 2 [type=json_invalid, input_value='[SearchEngine] Brave fou...ne-price-in-indonesia/"', input_type=str]
For further information visit https://errors.pydantic.dev/2.12/v/json_invalid
2025-10-25 14:17:56,419 - mcp.client.stdio - ERROR - Failed to parse JSONRPC message from server
Traceback (most recent call last):
File "C:\Projects\ai-agent\venv\Lib\site-packages\mcp\client\stdio\_\_init**.py", line 155, in stdout_reader
message = types.JSONRPCMessage.model_validate_json(line)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Projects\ai-agent\venv\Lib\site-packages\pydantic\main.py", line 766, in model_validate_json
return cls.**pydantic_validator**.validate_json(
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core.\_pydantic_core.ValidationError: 1 validation error for JSONRPCMessage
Invalid JSON: expected value at line 1 column 2 [type=json_invalid, input_value='[SearchEngine] Brave fou...tember 2025 & Cicil 0%"', input_type=str]
For further information visit https://errors.pydantic.dev/2.12/v/json_invalid
2025-10-25 14:17:56,420 - mcp.client.stdio - ERROR - Failed to parse JSONRPC message from server
Traceback (most recent call last):
File "C:\Projects\ai-agent\venv\Lib\site-packages\mcp\client\stdio\_\_init**.py", line 155, in stdout_reader
message = types.JSONRPCMessage.model_validate_json(line)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Projects\ai-agent\venv\Lib\site-packages\pydantic\main.py", line 766, in model_validate_json
return cls.**pydantic_validator**.validate_json(
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core.\_pydantic_core.ValidationError: 1 validation error for JSONRPCMessage
Invalid JSON: expected value at line 1 column 2 [type=json_invalid, input_value='[SearchEngine] Brave fou.../find/iphone-indonesia"', input_type=str]
For further information visit https://errors.pydantic.dev/2.12/v/json_invalid
2025-10-25 14:17:56,422 - mcp.client.stdio - ERROR - Failed to parse JSONRPC message from server
Traceback (most recent call last):
File "C:\Projects\ai-agent\venv\Lib\site-packages\mcp\client\stdio\_\_init**.py", line 155, in stdout_reader
message = types.JSONRPCMessage.model_validate_json(line)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Projects\ai-agent\venv\Lib\site-packages\pydantic\main.py", line 766, in model_validate_json
return cls.**pydantic_validator**.validate_json(
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core.\_pydantic_core.ValidationError: 1 validation error for JSONRPCMessage
Invalid JSON: expected value at line 1 column 2 [type=json_invalid, input_value='[SearchEngine] Brave fou... Mac Store Indonesia"', input_type=str]
For further information visit https://errors.pydantic.dev/2.12/v/json_invalid
2025-10-25 14:17:56,423 - mcp.client.stdio - ERROR - Failed to parse JSONRPC message from server
Traceback (most recent call last):
File "C:\Projects\ai-agent\venv\Lib\site-packages\mcp\client\stdio\_\_init**.py", line 155, in stdout_reader
message = types.JSONRPCMessage.model_validate_json(line)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Projects\ai-agent\venv\Lib\site-packages\pydantic\main.py", line 766, in model_validate_json
return cls.**pydantic_validator**.validate_json(
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core.\_pydantic_core.ValidationError: 1 validation error for JSONRPCMessage
Invalid JSON: expected value at line 1 column 2 [type=json_invalid, input_value='[SearchEngine] Brave fou...oduct-category/iphone/"', input_type=str]
For further information visit https://errors.pydantic.dev/2.12/v/json_invalid
2025-10-25 14:17:56,424 - mcp.client.stdio - ERROR - Failed to parse JSONRPC message from server
Traceback (most recent call last):
File "C:\Projects\ai-agent\venv\Lib\site-packages\mcp\client\stdio\_\_init**.py", line 155, in stdout_reader
message = types.JSONRPCMessage.model_validate_json(line)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Projects\ai-agent\venv\Lib\site-packages\pydantic\main.py", line 766, in model_validate_json
return cls.**pydantic_validator**.validate_json(
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core.\_pydantic_core.ValidationError: 1 validation error for JSONRPCMessage
Invalid JSON: expected value at line 1 column 2 [type=json_invalid, input_value='[SearchEngine] Brave fou...gkan Penawaran Terbaik"', input_type=str]
For further information visit https://errors.pydantic.dev/2.12/v/json_invalid
2025-10-25 14:17:56,425 - mcp.client.stdio - ERROR - Failed to parse JSONRPC message from server
Traceback (most recent call last):
File "C:\Projects\ai-agent\venv\Lib\site-packages\mcp\client\stdio\_\_init**.py", line 155, in stdout_reader
message = types.JSONRPCMessage.model_validate_json(line)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Projects\ai-agent\venv\Lib\site-packages\pydantic\main.py", line 766, in model_validate_json
return cls.**pydantic_validator**.validate_json(
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core.\_pydantic_core.ValidationError: 1 validation error for JSONRPCMessage
Invalid JSON: expected value at line 1 column 2 [type=json_invalid, input_value='[SearchEngine] Brave fou...artphone/harga-iphone/"', input_type=str]
For further information visit https://errors.pydantic.dev/2.12/v/json_invalid
2025-10-25 14:17:56,426 - mcp.client.stdio - ERROR - Failed to parse JSONRPC message from server
Traceback (most recent call last):
File "C:\Projects\ai-agent\venv\Lib\site-packages\mcp\client\stdio\_\_init**.py", line 155, in stdout_reader
message = types.JSONRPCMessage.model_validate_json(line)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Projects\ai-agent\venv\Lib\site-packages\pydantic\main.py", line 766, in model_validate_json
return cls.**pydantic_validator**.validate_json(
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core.\_pydantic_core.ValidationError: 1 validation error for JSONRPCMessage
Invalid JSON: expected value at line 1 column 2 [type=json_invalid, input_value='[SearchEngine] Brave fou... Allo Allo (Indonesia)"', input_type=str]
For further information visit https://errors.pydantic.dev/2.12/v/json_invalid
2025-10-25 14:17:56,426 - mcp.client.stdio - ERROR - Failed to parse JSONRPC message from server
Traceback (most recent call last):
File "C:\Projects\ai-agent\venv\Lib\site-packages\mcp\client\stdio\_\_init**.py", line 155, in stdout_reader
message = types.JSONRPCMessage.model_validate_json(line)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Projects\ai-agent\venv\Lib\site-packages\pydantic\main.py", line 766, in model_validate_json
return cls.**pydantic_validator**.validate_json(
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core.\_pydantic_core.ValidationError: 1 validation error for JSONRPCMessage
Invalid JSON: expected value at line 1 column 2 [type=json_invalid, input_value='[SearchEngine] Brave fou...o.com/id/cheap-iphone/"', input_type=str]
For further information visit https://errors.pydantic.dev/2.12/v/json_invalid
2025-10-25 14:17:56,427 - mcp.client.stdio - ERROR - Failed to parse JSONRPC message from server
Traceback (most recent call last):
File "C:\Projects\ai-agent\venv\Lib\site-packages\mcp\client\stdio\_\_init**.py", line 155, in stdout_reader
message = types.JSONRPCMessage.model_validate_json(line)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Projects\ai-agent\venv\Lib\site-packages\pydantic\main.py", line 766, in model_validate_json
return cls.**pydantic_validator**.validate_json(
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core.\_pydantic_core.ValidationError: 1 validation error for JSONRPCMessage
Invalid JSON: expected value at line 1 column 2 [type=json_invalid, input_value='[SearchEngine] Brave fou...one 2025 - Mobile57 Id"', input_type=str]
For further information visit https://errors.pydantic.dev/2.12/v/json_invalid
2025-10-25 14:17:56,428 - mcp.client.stdio - ERROR - Failed to parse JSONRPC message from server
Traceback (most recent call last):
File "C:\Projects\ai-agent\venv\Lib\site-packages\mcp\client\stdio\_\_init**.py", line 155, in stdout_reader
message = types.JSONRPCMessage.model_validate_json(line)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Projects\ai-agent\venv\Lib\site-packages\pydantic\main.py", line 766, in model_validate_json
return cls.**pydantic_validator**.validate_json(
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core.\_pydantic_core.ValidationError: 1 validation error for JSONRPCMessage
Invalid JSON: expected value at line 1 column 2 [type=json_invalid, input_value='[SearchEngine] Brave fou...7.com/id/phones/apple/"', input_type=str]
For further information visit https://errors.pydantic.dev/2.12/v/json_invalid
2025-10-25 14:17:56,428 - mcp.client.stdio - ERROR - Failed to parse JSONRPC message from server
Traceback (most recent call last):
File "C:\Projects\ai-agent\venv\Lib\site-packages\mcp\client\stdio\_\_init**.py", line 155, in stdout_reader
message = types.JSONRPCMessage.model_validate_json(line)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Projects\ai-agent\venv\Lib\site-packages\pydantic\main.py", line 766, in model_validate_json
return cls.**pydantic_validator**.validate_json(
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core.\_pydantic_core.ValidationError: 1 validation error for JSONRPCMessage
Invalid JSON: expected value at line 1 column 2 [type=json_invalid, input_value='[SearchEngine] Brave fou...rice in Indonesia 2025"', input_type=str]
For further information visit https://errors.pydantic.dev/2.12/v/json_invalid
2025-10-25 14:17:56,429 - mcp.client.stdio - ERROR - Failed to parse JSONRPC message from server
Traceback (most recent call last):
File "C:\Projects\ai-agent\venv\Lib\site-packages\mcp\client\stdio\_\_init**.py", line 155, in stdout_reader
message = types.JSONRPCMessage.model_validate_json(line)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Projects\ai-agent\venv\Lib\site-packages\pydantic\main.py", line 766, in model_validate_json
return cls.**pydantic_validator**.validate_json(
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core.\_pydantic_core.ValidationError: 1 validation error for JSONRPCMessage
Invalid JSON: expected value at line 1 column 2 [type=json_invalid, input_value='[SearchEngine] Brave fou...obile-prices-indonesia"', input_type=str]
For further information visit https://errors.pydantic.dev/2.12/v/json_invalid
2025-10-25 14:17:56,430 - mcp.client.stdio - ERROR - Failed to parse JSONRPC message from server
Traceback (most recent call last):
File "C:\Projects\ai-agent\venv\Lib\site-packages\mcp\client\stdio\_\_init**.py", line 155, in stdout_reader
message = types.JSONRPCMessage.model_validate_json(line)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Projects\ai-agent\venv\Lib\site-packages\pydantic\main.py", line 766, in model_validate_json
return cls.**pydantic_validator**.validate_json(
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core.\_pydantic_core.ValidationError: 1 validation error for JSONRPCMessage
Invalid JSON: expected value at line 1 column 2 [type=json_invalid, input_value='[SearchEngine] Brave fou...ia 2025 - Electrorates"', input_type=str]
For further information visit https://errors.pydantic.dev/2.12/v/json_invalid
2025-10-25 14:17:56,431 - mcp.client.stdio - ERROR - Failed to parse JSONRPC message from server
Traceback (most recent call last):
File "C:\Projects\ai-agent\venv\Lib\site-packages\mcp\client\stdio\_\_init**.py", line 155, in stdout_reader
message = types.JSONRPCMessage.model_validate_json(line)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Projects\ai-agent\venv\Lib\site-packages\pydantic\main.py", line 766, in model_validate_json
return cls.**pydantic_validator**.validate_json(
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core.\_pydantic_core.ValidationError: 1 validation error for JSONRPCMessage
Invalid JSON: expected value at line 1 column 2 [type=json_invalid, input_value='[SearchEngine] Brave fou...price-in-indonesia.php"', input_type=str]
For further information visit https://errors.pydantic.dev/2.12/v/json_invalid
2025-10-25 14:17:56,431 - mcp.client.stdio - ERROR - Failed to parse JSONRPC message from server
Traceback (most recent call last):
File "C:\Projects\ai-agent\venv\Lib\site-packages\mcp\client\stdio\_\_init**.py", line 155, in stdout_reader
message = types.JSONRPCMessage.model_validate_json(line)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Projects\ai-agent\venv\Lib\site-packages\pydantic\main.py", line 766, in model_validate_json
return cls.**pydantic_validator**.validate_json(
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core.\_pydantic_core.ValidationError: 1 validation error for JSONRPCMessage
Invalid JSON: expected value at line 1 column 2 [type=json_invalid, input_value='[SearchEngine] Brave found 8 results', input_type=str]  
 For further information visit https://errors.pydantic.dev/2.12/v/json_invalid
2025-10-25 14:17:56,432 - mcp.client.stdio - ERROR - Failed to parse JSONRPC message from server
Traceback (most recent call last):
File "C:\Projects\ai-agent\venv\Lib\site-packages\mcp\client\stdio\_\_init**.py", line 155, in stdout_reader
message = types.JSONRPCMessage.model_validate_json(line)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Projects\ai-agent\venv\Lib\site-packages\pydantic\main.py", line 766, in model_validate_json
return cls.**pydantic_validator**.validate_json(
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core.\_pydantic_core.ValidationError: 1 validation error for JSONRPCMessage
Invalid JSON: expected value at line 1 column 2 [type=json_invalid, input_value='[SearchEngine] Browser Brave parsed 8 results', input_type=str]
For further information visit https://errors.pydantic.dev/2.12/v/json_invalid
2025-10-25 14:17:57,623 - mcp.client.stdio - ERROR - Failed to parse JSONRPC message from server
Traceback (most recent call last):
File "C:\Projects\ai-agent\venv\Lib\site-packages\mcp\client\stdio\_\_init**.py", line 155, in stdout_reader
message = types.JSONRPCMessage.model_validate_json(line)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Projects\ai-agent\venv\Lib\site-packages\pydantic\main.py", line 766, in model_validate_json
return cls.**pydantic_validator**.validate_json(
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core.\_pydantic_core.ValidationError: 1 validation error for JSONRPCMessage
Invalid JSON: expected value at line 1 column 2 [type=json_invalid, input_value='[SearchEngine] Found 8 r...ults with Browser Brave', input_type=str]
For further information visit https://errors.pydantic.dev/2.12/v/json_invalid
2025-10-25 14:17:57,623 - mcp.client.stdio - ERROR - Failed to parse JSONRPC message from server
Traceback (most recent call last):
File "C:\Projects\ai-agent\venv\Lib\site-packages\mcp\client\stdio\_\_init**.py", line 155, in stdout_reader
message = types.JSONRPCMessage.model_validate_json(line)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Projects\ai-agent\venv\Lib\site-packages\pydantic\main.py", line 766, in model_validate_json
return cls.**pydantic_validator**.validate_json(
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core.\_pydantic_core.ValidationError: 1 validation error for JSONRPCMessage
Invalid JSON: expected value at line 1 column 2 [type=json_invalid, input_value='[SearchEngine] Quality a...arga, indonesia, price]', input_type=str]
For further information visit https://errors.pydantic.dev/2.12/v/json_invalid
2025-10-25 14:17:57,624 - mcp.client.stdio - ERROR - Failed to parse JSONRPC message from server
Traceback (most recent call last):
File "C:\Projects\ai-agent\venv\Lib\site-packages\mcp\client\stdio\_\_init**.py", line 155, in stdout_reader
message = types.JSONRPCMessage.model_validate_json(line)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Projects\ai-agent\venv\Lib\site-packages\pydantic\main.py", line 766, in model_validate_json
return cls.**pydantic_validator**.validate_json(
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core.\_pydantic_core.ValidationError: 1 validation error for JSONRPCMessage
Invalid JSON: expected value at line 1 column 2 [type=json_invalid, input_value='[SearchEngine] Result "A...ases: 0, penalty: 0.20)', input_type=str]
For further information visit https://errors.pydantic.dev/2.12/v/json_invalid
2025-10-25 14:17:57,625 - mcp.client.stdio - ERROR - Failed to parse JSONRPC message from server
Traceback (most recent call last):
File "C:\Projects\ai-agent\venv\Lib\site-packages\mcp\client\stdio\_\_init**.py", line 155, in stdout_reader
message = types.JSONRPCMessage.model_validate_json(line)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Projects\ai-agent\venv\Lib\site-packages\pydantic\main.py", line 766, in model_validate_json
return cls.**pydantic_validator**.validate_json(
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core.\_pydantic_core.ValidationError: 1 validation error for JSONRPCMessage
Invalid JSON: expected value at line 1 column 2 [type=json_invalid, input_value='[SearchEngine] Result "T...ases: 0, penalty: 0.00)', input_type=str]
For further information visit https://errors.pydantic.dev/2.12/v/json_invalid
2025-10-25 14:17:57,626 - mcp.client.stdio - ERROR - Failed to parse JSONRPC message from server
Traceback (most recent call last):
File "C:\Projects\ai-agent\venv\Lib\site-packages\mcp\client\stdio\_\_init**.py", line 155, in stdout_reader
message = types.JSONRPCMessage.model_validate_json(line)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Projects\ai-agent\venv\Lib\site-packages\pydantic\main.py", line 766, in model_validate_json
return cls.**pydantic_validator**.validate_json(
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core.\_pydantic_core.ValidationError: 1 validation error for JSONRPCMessage
Invalid JSON: expected value at line 1 column 2 [type=json_invalid, input_value='[SearchEngine] Result "M...ases: 0, penalty: 0.40)', input_type=str]
For further information visit https://errors.pydantic.dev/2.12/v/json_invalid
2025-10-25 14:17:57,626 - mcp.client.stdio - ERROR - Failed to parse JSONRPC message from server
Traceback (most recent call last):
File "C:\Projects\ai-agent\venv\Lib\site-packages\mcp\client\stdio\_\_init**.py", line 155, in stdout_reader
message = types.JSONRPCMessage.model_validate_json(line)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Projects\ai-agent\venv\Lib\site-packages\pydantic\main.py", line 766, in model_validate_json
return cls.**pydantic_validator**.validate_json(
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core.\_pydantic_core.ValidationError: 1 validation error for JSONRPCMessage
Invalid JSON: expected value at line 1 column 2 [type=json_invalid, input_value='[SearchEngine] Result "i...ases: 0, penalty: 0.20)', input_type=str]
For further information visit https://errors.pydantic.dev/2.12/v/json_invalid
2025-10-25 14:17:57,627 - mcp.client.stdio - ERROR - Failed to parse JSONRPC message from server
Traceback (most recent call last):
File "C:\Projects\ai-agent\venv\Lib\site-packages\mcp\client\stdio\_\_init**.py", line 155, in stdout_reader
message = types.JSONRPCMessage.model_validate_json(line)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Projects\ai-agent\venv\Lib\site-packages\pydantic\main.py", line 766, in model_validate_json
return cls.**pydantic_validator**.validate_json(
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core.\_pydantic_core.ValidationError: 1 validation error for JSONRPCMessage
Invalid JSON: expected value at line 1 column 2 [type=json_invalid, input_value='[SearchEngine] Result "A...ases: 0, penalty: 0.20)', input_type=str]
For further information visit https://errors.pydantic.dev/2.12/v/json_invalid
2025-10-25 14:17:57,627 - mcp.client.stdio - ERROR - Failed to parse JSONRPC message from server
Traceback (most recent call last):
File "C:\Projects\ai-agent\venv\Lib\site-packages\mcp\client\stdio\_\_init**.py", line 155, in stdout_reader
message = types.JSONRPCMessage.model_validate_json(line)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Projects\ai-agent\venv\Lib\site-packages\pydantic\main.py", line 766, in model_validate_json
return cls.**pydantic_validator**.validate_json(
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core.\_pydantic_core.ValidationError: 1 validation error for JSONRPCMessage
Invalid JSON: expected value at line 1 column 2 [type=json_invalid, input_value='[SearchEngine] Result "M...ases: 0, penalty: 0.20)', input_type=str]
For further information visit https://errors.pydantic.dev/2.12/v/json_invalid
2025-10-25 14:17:57,628 - mcp.client.stdio - ERROR - Failed to parse JSONRPC message from server
Traceback (most recent call last):
File "C:\Projects\ai-agent\venv\Lib\site-packages\mcp\client\stdio\_\_init**.py", line 155, in stdout_reader
message = types.JSONRPCMessage.model_validate_json(line)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Projects\ai-agent\venv\Lib\site-packages\pydantic\main.py", line 766, in model_validate_json
return cls.**pydantic_validator**.validate_json(
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core.\_pydantic_core.ValidationError: 1 validation error for JSONRPCMessage
Invalid JSON: expected value at line 1 column 2 [type=json_invalid, input_value='[SearchEngine] Result "P...ases: 0, penalty: 0.20)', input_type=str]
For further information visit https://errors.pydantic.dev/2.12/v/json_invalid
2025-10-25 14:17:57,629 - mcp.client.stdio - ERROR - Failed to parse JSONRPC message from server
Traceback (most recent call last):
File "C:\Projects\ai-agent\venv\Lib\site-packages\mcp\client\stdio\_\_init**.py", line 155, in stdout_reader
message = types.JSONRPCMessage.model_validate_json(line)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Projects\ai-agent\venv\Lib\site-packages\pydantic\main.py", line 766, in model_validate_json
return cls.**pydantic_validator**.validate_json(
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core.\_pydantic_core.ValidationError: 1 validation error for JSONRPCMessage
Invalid JSON: expected value at line 1 column 2 [type=json_invalid, input_value='[SearchEngine] Result "E...ases: 0, penalty: 0.20)', input_type=str]
For further information visit https://errors.pydantic.dev/2.12/v/json_invalid
2025-10-25 14:17:57,630 - mcp.client.stdio - ERROR - Failed to parse JSONRPC message from server
Traceback (most recent call last):
File "C:\Projects\ai-agent\venv\Lib\site-packages\mcp\client\stdio\_\_init**.py", line 155, in stdout_reader
message = types.JSONRPCMessage.model_validate_json(line)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Projects\ai-agent\venv\Lib\site-packages\pydantic\main.py", line 766, in model_validate_json
return cls.**pydantic_validator**.validate_json(
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core.\_pydantic_core.ValidationError: 1 validation error for JSONRPCMessage
Invalid JSON: expected value at line 1 column 2 [type=json_invalid, input_value='[SearchEngine] Browser B...quality score: 0.55/1.0', input_type=str]
For further information visit https://errors.pydantic.dev/2.12/v/json_invalid
2025-10-25 14:17:57,630 - mcp.client.stdio - ERROR - Failed to parse JSONRPC message from server
Traceback (most recent call last):
File "C:\Projects\ai-agent\venv\Lib\site-packages\mcp\client\stdio\_\_init**.py", line 155, in stdout_reader
message = types.JSONRPCMessage.model_validate_json(line)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Projects\ai-agent\venv\Lib\site-packages\pydantic\main.py", line 766, in model_validate_json
return cls.**pydantic_validator**.validate_json(
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core.\_pydantic_core.ValidationError: 1 validation error for JSONRPCMessage
Invalid JSON: expected value at line 1 column 2 [type=json_invalid, input_value='[SearchEngine] Good qual...Brave, using as primary', input_type=str]
For further information visit https://errors.pydantic.dev/2.12/v/json_invalid
2025-10-25 14:17:57,631 - mcp.client.stdio - ERROR - Failed to parse JSONRPC message from server
Traceback (most recent call last):
File "C:\Projects\ai-agent\venv\Lib\site-packages\mcp\client\stdio\_\_init**.py", line 155, in stdout_reader
message = types.JSONRPCMessage.model_validate_json(line)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Projects\ai-agent\venv\Lib\site-packages\pydantic\main.py", line 766, in model_validate_json
return cls.**pydantic_validator**.validate_json(
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core.\_pydantic_core.ValidationError: 1 validation error for JSONRPCMessage
Invalid JSON: expected value at line 1 column 2 [type=json_invalid, input_value='[EnhancedContentExtracto...o get 3 non-PDF results', input_type=str]
For further information visit https://errors.pydantic.dev/2.12/v/json_invalid
2025-10-25 14:17:57,632 - mcp.client.stdio - ERROR - Failed to parse JSONRPC message from server
Traceback (most recent call last):
File "C:\Projects\ai-agent\venv\Lib\site-packages\mcp\client\stdio\_\_init**.py", line 155, in stdout_reader
message = types.JSONRPCMessage.model_validate_json(line)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Projects\ai-agent\venv\Lib\site-packages\pydantic\main.py", line 766, in model_validate_json
return cls.**pydantic_validator**.validate_json(
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core.\_pydantic_core.ValidationError: 1 validation error for JSONRPCMessage
Invalid JSON: expected value at line 1 column 2 [type=json_invalid, input_value='[EnhancedContentExtracto...DF results concurrently', input_type=str]
For further information visit https://errors.pydantic.dev/2.12/v/json_invalid
2025-10-25 14:17:57,633 - mcp.client.stdio - ERROR - Failed to parse JSONRPC message from server
Traceback (most recent call last):
File "C:\Projects\ai-agent\venv\Lib\site-packages\mcp\client\stdio\_\_init**.py", line 155, in stdout_reader
message = types.JSONRPCMessage.model_validate_json(line)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Projects\ai-agent\venv\Lib\site-packages\pydantic\main.py", line 766, in model_validate_json
return cls.**pydantic_validator**.validate_json(
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core.\_pydantic_core.ValidationError: 1 validation error for JSONRPCMessage
Invalid JSON: expected value at line 1 column 2 [type=json_invalid, input_value='[EnhancedContentExtracto...one-price-in-indonesia/', input_type=str]
For further information visit https://errors.pydantic.dev/2.12/v/json_invalid
2025-10-25 14:17:57,688 - mcp.client.stdio - ERROR - Failed to parse JSONRPC message from server
Traceback (most recent call last):
File "C:\Projects\ai-agent\venv\Lib\site-packages\mcp\client\stdio\_\_init**.py", line 155, in stdout_reader
message = types.JSONRPCMessage.model_validate_json(line)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Projects\ai-agent\venv\Lib\site-packages\pydantic\main.py", line 766, in model_validate_json
return cls.**pydantic_validator**.validate_json(
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core.\_pydantic_core.ValidationError: 1 validation error for JSONRPCMessage
Invalid JSON: expected value at line 1 column 2 [type=json_invalid, input_value='[EnhancedContentExtracto...m/find/iphone-indonesia', input_type=str]
For further information visit https://errors.pydantic.dev/2.12/v/json_invalid
2025-10-25 14:17:57,690 - mcp.client.stdio - ERROR - Failed to parse JSONRPC message from server
Traceback (most recent call last):
File "C:\Projects\ai-agent\venv\Lib\site-packages\mcp\client\stdio\_\_init**.py", line 155, in stdout_reader
message = types.JSONRPCMessage.model_validate_json(line)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Projects\ai-agent\venv\Lib\site-packages\pydantic\main.py", line 766, in model_validate_json
return cls.**pydantic_validator**.validate_json(
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core.\_pydantic_core.ValidationError: 1 validation error for JSONRPCMessage
Invalid JSON: expected value at line 1 column 2 [type=json_invalid, input_value='[EnhancedContentExtracto...roduct-category/iphone/', input_type=str]
For further information visit https://errors.pydantic.dev/2.12/v/json_invalid
2025-10-25 14:17:57,691 - mcp.client.stdio - ERROR - Failed to parse JSONRPC message from server
Traceback (most recent call last):
File "C:\Projects\ai-agent\venv\Lib\site-packages\mcp\client\stdio\_\_init**.py", line 155, in stdout_reader
message = types.JSONRPCMessage.model_validate_json(line)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Projects\ai-agent\venv\Lib\site-packages\pydantic\main.py", line 766, in model_validate_json
return cls.**pydantic_validator**.validate_json(
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core.\_pydantic_core.ValidationError: 1 validation error for JSONRPCMessage
Invalid JSON: expected value at line 1 column 2 [type=json_invalid, input_value='[EnhancedContentExtracto...martphone/harga-iphone/', input_type=str]
For further information visit https://errors.pydantic.dev/2.12/v/json_invalid
2025-10-25 14:17:57,693 - mcp.client.stdio - ERROR - Failed to parse JSONRPC message from server
Traceback (most recent call last):
File "C:\Projects\ai-agent\venv\Lib\site-packages\mcp\client\stdio\_\_init**.py", line 155, in stdout_reader
message = types.JSONRPCMessage.model_validate_json(line)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Projects\ai-agent\venv\Lib\site-packages\pydantic\main.py", line 766, in model_validate_json
return cls.**pydantic_validator**.validate_json(
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core.\_pydantic_core.ValidationError: 1 validation error for JSONRPCMessage
Invalid JSON: expected value at line 1 column 2 [type=json_invalid, input_value='[EnhancedContentExtracto...lo.com/id/cheap-iphone/', input_type=str]
For further information visit https://errors.pydantic.dev/2.12/v/json_invalid
2025-10-25 14:17:57,694 - mcp.client.stdio - ERROR - Failed to parse JSONRPC message from server
Traceback (most recent call last):
File "C:\Projects\ai-agent\venv\Lib\site-packages\mcp\client\stdio\_\_init**.py", line 155, in stdout_reader
message = types.JSONRPCMessage.model_validate_json(line)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Projects\ai-agent\venv\Lib\site-packages\pydantic\main.py", line 766, in model_validate_json
return cls.**pydantic_validator**.validate_json(
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core.\_pydantic_core.ValidationError: 1 validation error for JSONRPCMessage
Invalid JSON: expected value at line 1 column 2 [type=json_invalid, input_value='[EnhancedContentExtracto...57.com/id/phones/apple/', input_type=str]
For further information visit https://errors.pydantic.dev/2.12/v/json_invalid
2025-10-25 14:17:57,960 - mcp.client.stdio - ERROR - Failed to parse JSONRPC message from server
Traceback (most recent call last):
File "C:\Projects\ai-agent\venv\Lib\site-packages\mcp\client\stdio\_\_init**.py", line 155, in stdout_reader
message = types.JSONRPCMessage.model_validate_json(line)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Projects\ai-agent\venv\Lib\site-packages\pydantic\main.py", line 766, in model_validate_json
return cls.**pydantic_validator**.validate_json(
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core.\_pydantic_core.ValidationError: 1 validation error for JSONRPCMessage
Invalid JSON: expected value at line 1 column 2 [type=json_invalid, input_value='[EnhancedContentExtracto...ctor: main (8972 chars)', input_type=str]
For further information visit https://errors.pydantic.dev/2.12/v/json_invalid
2025-10-25 14:17:57,961 - mcp.client.stdio - ERROR - Failed to parse JSONRPC message from server
Traceback (most recent call last):
File "C:\Projects\ai-agent\venv\Lib\site-packages\mcp\client\stdio\_\_init**.py", line 155, in stdout_reader
message = types.JSONRPCMessage.model_validate_json(line)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Projects\ai-agent\venv\Lib\site-packages\pydantic\main.py", line 766, in model_validate_json
return cls.**pydantic_validator**.validate_json(
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core.\_pydantic_core.ValidationError: 1 validation error for JSONRPCMessage
Invalid JSON: expected value at line 1 column 2 [type=json_invalid, input_value='[EnhancedContentExtracto... with axios: 3919 chars', input_type=str]
For further information visit https://errors.pydantic.dev/2.12/v/json_invalid
2025-10-25 14:17:57,962 - mcp.client.stdio - ERROR - Failed to parse JSONRPC message from server
Traceback (most recent call last):
File "C:\Projects\ai-agent\venv\Lib\site-packages\mcp\client\stdio\_\_init**.py", line 155, in stdout_reader
message = types.JSONRPCMessage.model_validate_json(line)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Projects\ai-agent\venv\Lib\site-packages\pydantic\main.py", line 766, in model_validate_json
return cls.**pydantic_validator\_\_.validate_json(
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core.\_pydantic_core.ValidationError: 1 validation error for JSONRPCMessage
Invalid JSON: expected value at line 1 column 2 [type=json_invalid, input_value='[EnhancedContentExtracto...57.com/id/phones/apple/', input_type=str]
For further information visit https://errors.pydantic.dev/2.12/v/json_invalid
2025-10-25 14:17:58 WARNING discord.gateway Shard ID None heartbeat blocked for more than 20 seconds.
Loop thread traceback (most recent call last):
File "C:\Projects\ai-agent\bot.py", line 225, in <module>
main()
File "C:\Projects\ai-agent\bot.py", line 214, in main
bot.run(discord_token)
File "C:\Projects\ai-agent\venv\Lib\site-packages\discord\client.py", line 929, in run
asyncio.run(runner())
File "C:\Python312\Lib\asyncio\runners.py", line 194, in run
return runner.run(main)
File "C:\Python312\Lib\asyncio\runners.py", line 118, in run
return self.\_loop.run_until_complete(task)
File "C:\Python312\Lib\asyncio\base_events.py", line 674, in run_until_complete
self.run_forever()
File "C:\Python312\Lib\asyncio\windows_events.py", line 322, in run_forever
super().run_forever()
File "C:\Python312\Lib\asyncio\base_events.py", line 641, in run_forever
self.\_run_once()
File "C:\Python312\Lib\asyncio\base_events.py", line 1987, in \_run_once
handle.\_run()
File "C:\Python312\Lib\asyncio\events.py", line 88, in \_run
self.\_context.run(self.\_callback, *self.\_args)
File "C:\Projects\ai-agent\venv\Lib\site-packages\discord\client.py", line 504, in \_run_event
await coro(*args, \*\*kwargs)
File "C:\Projects\ai-agent\bot.py", line 126, in on_message
response = self.bot_core.process_message(user_id, username, content)
File "C:\Projects\ai-agent\core\bot_core.py", line 122, in process_message
return self.\_handle_search_price(result)
File "C:\Projects\ai-agent\core\bot_core.py", line 475, in \_handle_search_price
mcp_result = future.result()
File "C:\Python312\Lib\concurrent\futures_base.py", line 451, in result
self.\_condition.wait(timeout)
File "C:\Python312\Lib\threading.py", line 355, in wait
waiter.acquire()

2025-10-25 14:17:58,242 - discord.gateway - WARNING - Shard ID None heartbeat blocked for more than 20 seconds.
Loop thread traceback (most recent call last):
File "C:\Projects\ai-agent\bot.py", line 225, in <module>
main()
File "C:\Projects\ai-agent\bot.py", line 214, in main
bot.run(discord_token)
File "C:\Projects\ai-agent\venv\Lib\site-packages\discord\client.py", line 929, in run
asyncio.run(runner())
File "C:\Python312\Lib\asyncio\runners.py", line 194, in run
return runner.run(main)
File "C:\Python312\Lib\asyncio\runners.py", line 118, in run
return self.\_loop.run_until_complete(task)
File "C:\Python312\Lib\asyncio\base_events.py", line 674, in run_until_complete
self.run_forever()
File "C:\Python312\Lib\asyncio\windows_events.py", line 322, in run_forever
super().run_forever()
File "C:\Python312\Lib\asyncio\base_events.py", line 641, in run_forever
self.\_run_once()
File "C:\Python312\Lib\asyncio\base_events.py", line 1987, in \_run_once
handle.\_run()
File "C:\Python312\Lib\asyncio\events.py", line 88, in \_run
self.\_context.run(self.\_callback, *self.\_args)
File "C:\Projects\ai-agent\venv\Lib\site-packages\discord\client.py", line 504, in \_run_event
await coro(*args, \*\*kwargs)
File "C:\Projects\ai-agent\bot.py", line 126, in on_message
response = self.bot_core.process_message(user_id, username, content)
File "C:\Projects\ai-agent\core\bot_core.py", line 122, in process_message
return self.\_handle_search_price(result)
File "C:\Projects\ai-agent\core\bot_core.py", line 475, in \_handle_search_price
mcp_result = future.result()
File "C:\Python312\Lib\concurrent\futures_base.py", line 451, in result
self.\_condition.wait(timeout)
File "C:\Python312\Lib\threading.py", line 355, in wait
waiter.acquire()

2025-10-25 14:17:58,339 - mcp.client.stdio - ERROR - Failed to parse JSONRPC message from server
Traceback (most recent call last):
File "C:\Projects\ai-agent\venv\Lib\site-packages\mcp\client\stdio\_\_init**.py", line 155, in stdout_reader
message = types.JSONRPCMessage.model_validate_json(line)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Projects\ai-agent\venv\Lib\site-packages\pydantic\main.py", line 766, in model_validate_json
return cls.**pydantic_validator**.validate_json(
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core.\_pydantic_core.ValidationError: 1 validation error for JSONRPCMessage
Invalid JSON: expected value at line 1 column 2 [type=json_invalid, input_value='[EnhancedContentExtracto...r: article (1103 chars)', input_type=str]
For further information visit https://errors.pydantic.dev/2.12/v/json_invalid
2025-10-25 14:17:58,340 - mcp.client.stdio - ERROR - Failed to parse JSONRPC message from server
Traceback (most recent call last):
File "C:\Projects\ai-agent\venv\Lib\site-packages\mcp\client\stdio\_\_init**.py", line 155, in stdout_reader
message = types.JSONRPCMessage.model_validate_json(line)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Projects\ai-agent\venv\Lib\site-packages\pydantic\main.py", line 766, in model_validate_json
return cls.**pydantic_validator**.validate_json(
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core.\_pydantic_core.ValidationError: 1 validation error for JSONRPCMessage
Invalid JSON: expected value at line 1 column 2 [type=json_invalid, input_value='[EnhancedContentExtracto... with axios: 1046 chars', input_type=str]
For further information visit https://errors.pydantic.dev/2.12/v/json_invalid
2025-10-25 14:17:58,341 - mcp.client.stdio - ERROR - Failed to parse JSONRPC message from server
Traceback (most recent call last):
File "C:\Projects\ai-agent\venv\Lib\site-packages\mcp\client\stdio\_\_init**.py", line 155, in stdout_reader
message = types.JSONRPCMessage.model_validate_json(line)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Projects\ai-agent\venv\Lib\site-packages\pydantic\main.py", line 766, in model_validate_json
return cls.**pydantic_validator**.validate_json(
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core.\_pydantic_core.ValidationError: 1 validation error for JSONRPCMessage
Invalid JSON: expected value at line 1 column 2 [type=json_invalid, input_value='[EnhancedContentExtracto...one-price-in-indonesia/', input_type=str]
For further information visit https://errors.pydantic.dev/2.12/v/json_invalid
2025-10-25 14:17:58,608 - mcp.client.stdio - ERROR - Failed to parse JSONRPC message from server
Traceback (most recent call last):
File "C:\Projects\ai-agent\venv\Lib\site-packages\mcp\client\stdio\_\_init**.py", line 155, in stdout_reader
message = types.JSONRPCMessage.model_validate_json(line)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Projects\ai-agent\venv\Lib\site-packages\pydantic\main.py", line 766, in model_validate_json
return cls.**pydantic_validator**.validate_json(
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core.\_pydantic_core.ValidationError: 1 validation error for JSONRPCMessage
Invalid JSON: expected value at line 1 column 2 [type=json_invalid, input_value='[EnhancedContentExtracto...und, using body content', input_type=str]
For further information visit https://errors.pydantic.dev/2.12/v/json_invalid
2025-10-25 14:17:58,609 - mcp.client.stdio - ERROR - Failed to parse JSONRPC message from server
Traceback (most recent call last):
File "C:\Projects\ai-agent\venv\Lib\site-packages\mcp\client\stdio\_\_init**.py", line 155, in stdout_reader
message = types.JSONRPCMessage.model_validate_json(line)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Projects\ai-agent\venv\Lib\site-packages\pydantic\main.py", line 766, in model_validate_json
return cls.**pydantic_validator**.validate_json(
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core.\_pydantic_core.ValidationError: 1 validation error for JSONRPCMessage
Invalid JSON: expected value at line 1 column 2 [type=json_invalid, input_value='[EnhancedContentExtracto...d with axios: 136 chars', input_type=str]
For further information visit https://errors.pydantic.dev/2.12/v/json_invalid
2025-10-25 14:17:58,610 - mcp.client.stdio - ERROR - Failed to parse JSONRPC message from server
Traceback (most recent call last):
File "C:\Projects\ai-agent\venv\Lib\site-packages\mcp\client\stdio\_\_init**.py", line 155, in stdout_reader
message = types.JSONRPCMessage.model_validate_json(line)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Projects\ai-agent\venv\Lib\site-packages\pydantic\main.py", line 766, in model_validate_json
return cls.**pydantic_validator**.validate_json(
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core.\_pydantic_core.ValidationError: 1 validation error for JSONRPCMessage
Invalid JSON: expected value at line 1 column 2 [type=json_invalid, input_value='[EnhancedContentExtracto...martphone/harga-iphone/', input_type=str]
For further information visit https://errors.pydantic.dev/2.12/v/json_invalid
2025-10-25 14:17:58,755 - mcp.client.stdio - ERROR - Failed to parse JSONRPC message from server
Traceback (most recent call last):
File "C:\Projects\ai-agent\venv\Lib\site-packages\mcp\client\stdio\_\_init**.py", line 155, in stdout_reader
message = types.JSONRPCMessage.model_validate_json(line)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Projects\ai-agent\venv\Lib\site-packages\pydantic\main.py", line 766, in model_validate_json
return cls.**pydantic_validator**.validate_json(
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core.\_pydantic_core.ValidationError: 1 validation error for JSONRPCMessage
Invalid JSON: expected value at line 1 column 2 [type=json_invalid, input_value='[EnhancedContentExtracto...ctor: main (1253 chars)', input_type=str]
For further information visit https://errors.pydantic.dev/2.12/v/json_invalid
2025-10-25 14:17:58,756 - mcp.client.stdio - ERROR - Failed to parse JSONRPC message from server
Traceback (most recent call last):
File "C:\Projects\ai-agent\venv\Lib\site-packages\mcp\client\stdio\_\_init**.py", line 155, in stdout_reader
message = types.JSONRPCMessage.model_validate_json(line)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Projects\ai-agent\venv\Lib\site-packages\pydantic\main.py", line 766, in model_validate_json
return cls.**pydantic_validator**.validate_json(
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core.\_pydantic_core.ValidationError: 1 validation error for JSONRPCMessage
Invalid JSON: expected value at line 1 column 2 [type=json_invalid, input_value='[EnhancedContentExtracto... with axios: 1253 chars', input_type=str]
For further information visit https://errors.pydantic.dev/2.12/v/json_invalid
2025-10-25 14:17:58,757 - mcp.client.stdio - ERROR - Failed to parse JSONRPC message from server
Traceback (most recent call last):
File "C:\Projects\ai-agent\venv\Lib\site-packages\mcp\client\stdio\_\_init**.py", line 155, in stdout_reader
message = types.JSONRPCMessage.model_validate_json(line)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Projects\ai-agent\venv\Lib\site-packages\pydantic\main.py", line 766, in model_validate_json
return cls.**pydantic_validator**.validate_json(
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core.\_pydantic_core.ValidationError: 1 validation error for JSONRPCMessage
Invalid JSON: expected value at line 1 column 2 [type=json_invalid, input_value='[EnhancedContentExtracto...m/find/iphone-indonesia', input_type=str]
For further information visit https://errors.pydantic.dev/2.12/v/json_invalid
2025-10-25 14:17:59,309 - mcp.client.stdio - ERROR - Failed to parse JSONRPC message from server
Traceback (most recent call last):
File "C:\Projects\ai-agent\venv\Lib\site-packages\mcp\client\stdio\_\_init**.py", line 155, in stdout_reader
message = types.JSONRPCMessage.model_validate_json(line)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Projects\ai-agent\venv\Lib\site-packages\pydantic\main.py", line 766, in model_validate_json
return cls.**pydantic_validator**.validate_json(
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core.\_pydantic_core.ValidationError: 1 validation error for JSONRPCMessage
Invalid JSON: expected value at line 1 column 2 [type=json_invalid, input_value='[EnhancedContentExtracto...und, using body content', input_type=str]
For further information visit https://errors.pydantic.dev/2.12/v/json_invalid
2025-10-25 14:17:59,310 - mcp.client.stdio - ERROR - Failed to parse JSONRPC message from server
Traceback (most recent call last):
File "C:\Projects\ai-agent\venv\Lib\site-packages\mcp\client\stdio\_\_init**.py", line 155, in stdout_reader
message = types.JSONRPCMessage.model_validate_json(line)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Projects\ai-agent\venv\Lib\site-packages\pydantic\main.py", line 766, in model_validate_json
return cls.**pydantic_validator**.validate_json(
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core.\_pydantic_core.ValidationError: 1 validation error for JSONRPCMessage
Invalid JSON: expected value at line 1 column 2 [type=json_invalid, input_value='[EnhancedContentExtracto... - likely bot detection', input_type=str]
For further information visit https://errors.pydantic.dev/2.12/v/json_invalid
2025-10-25 14:17:59,311 - mcp.client.stdio - ERROR - Failed to parse JSONRPC message from server
Traceback (most recent call last):
File "C:\Projects\ai-agent\venv\Lib\site-packages\mcp\client\stdio\_\_init**.py", line 155, in stdout_reader
message = types.JSONRPCMessage.model_validate_json(line)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Projects\ai-agent\venv\Lib\site-packages\pydantic\main.py", line 766, in model_validate_json
return cls.**pydantic_validator**.validate_json(
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core.\_pydantic_core.ValidationError: 1 validation error for JSONRPCMessage
Invalid JSON: expected value at line 1 column 2 [type=json_invalid, input_value='[EnhancedContentExtracto...roduct-category/iphone/', input_type=str]
For further information visit https://errors.pydantic.dev/2.12/v/json_invalid
2025-10-25 14:17:59,311 - mcp.client.stdio - ERROR - Failed to parse JSONRPC message from server
Traceback (most recent call last):
File "C:\Projects\ai-agent\venv\Lib\site-packages\mcp\client\stdio\_\_init**.py", line 155, in stdout_reader
message = types.JSONRPCMessage.model_validate_json(line)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Projects\ai-agent\venv\Lib\site-packages\pydantic\main.py", line 766, in model_validate_json
return cls.**pydantic_validator**.validate_json(
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core.\_pydantic_core.ValidationError: 1 validation error for JSONRPCMessage
Invalid JSON: expected value at line 1 column 2 [type=json_invalid, input_value='[BrowserPool] Launching new chromium browser', input_type=str]
For further information visit https://errors.pydantic.dev/2.12/v/json_invalid
2025-10-25 14:17:59,588 - mcp.client.stdio - ERROR - Failed to parse JSONRPC message from server
Traceback (most recent call last):
File "C:\Projects\ai-agent\venv\Lib\site-packages\mcp\client\stdio\_\_init**.py", line 155, in stdout_reader
message = types.JSONRPCMessage.model_validate_json(line)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Projects\ai-agent\venv\Lib\site-packages\pydantic\main.py", line 766, in model_validate_json
return cls.**pydantic_validator**.validate_json(
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core.\_pydantic_core.ValidationError: 1 validation error for JSONRPCMessage
Invalid JSON: expected value at line 1 column 2 [type=json_invalid, input_value='[BrowserExtractor] Navig...roduct-category/iphone/', input_type=str]
For further information visit https://errors.pydantic.dev/2.12/v/json_invalid
2025-10-25 14:18:00,871 - mcp.client.stdio - ERROR - Failed to parse JSONRPC message from server
Traceback (most recent call last):
File "C:\Projects\ai-agent\venv\Lib\site-packages\mcp\client\stdio\_\_init**.py", line 155, in stdout_reader
message = types.JSONRPCMessage.model_validate_json(line)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Projects\ai-agent\venv\Lib\site-packages\pydantic\main.py", line 766, in model_validate_json
return cls.**pydantic_validator**.validate_json(
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core.\_pydantic_core.ValidationError: 1 validation error for JSONRPCMessage
Invalid JSON: expected value at line 1 column 2 [type=json_invalid, input_value='[EnhancedContentExtracto...und, using body content', input_type=str]
For further information visit https://errors.pydantic.dev/2.12/v/json_invalid
2025-10-25 14:18:00,872 - mcp.client.stdio - ERROR - Failed to parse JSONRPC message from server
Traceback (most recent call last):
File "C:\Projects\ai-agent\venv\Lib\site-packages\mcp\client\stdio\_\_init**.py", line 155, in stdout_reader
message = types.JSONRPCMessage.model_validate_json(line)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Projects\ai-agent\venv\Lib\site-packages\pydantic\main.py", line 766, in model_validate_json
return cls.**pydantic_validator**.validate_json(
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core.\_pydantic_core.ValidationError: 1 validation error for JSONRPCMessage
Invalid JSON: expected value at line 1 column 2 [type=json_invalid, input_value='[EnhancedContentExtracto... with axios: 3770 chars', input_type=str]
For further information visit https://errors.pydantic.dev/2.12/v/json_invalid
2025-10-25 14:18:00,873 - mcp.client.stdio - ERROR - Failed to parse JSONRPC message from server
Traceback (most recent call last):
File "C:\Projects\ai-agent\venv\Lib\site-packages\mcp\client\stdio\_\_init**.py", line 155, in stdout_reader
message = types.JSONRPCMessage.model_validate_json(line)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Projects\ai-agent\venv\Lib\site-packages\pydantic\main.py", line 766, in model_validate_json
return cls.**pydantic_validator**.validate_json(
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core.\_pydantic_core.ValidationError: 1 validation error for JSONRPCMessage
Invalid JSON: expected value at line 1 column 2 [type=json_invalid, input_value='[EnhancedContentExtracto...lo.com/id/cheap-iphone/', input_type=str]
For further information visit https://errors.pydantic.dev/2.12/v/json_invalid
2025-10-25 14:18:05,190 - mcp.client.stdio - ERROR - Failed to parse JSONRPC message from server
Traceback (most recent call last):
File "C:\Projects\ai-agent\venv\Lib\site-packages\mcp\client\stdio\_\_init**.py", line 155, in stdout_reader
message = types.JSONRPCMessage.model_validate_json(line)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Projects\ai-agent\venv\Lib\site-packages\pydantic\main.py", line 766, in model_validate_json
return cls.**pydantic_validator**.validate_json(
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core.\_pydantic_core.ValidationError: 1 validation error for JSONRPCMessage
Invalid JSON: expected value at line 1 column 2 [type=json_invalid, input_value='[EnhancedContentExtracto...und, using body content', input_type=str]
For further information visit https://errors.pydantic.dev/2.12/v/json_invalid
2025-10-25 14:18:05,195 - mcp.client.stdio - ERROR - Failed to parse JSONRPC message from server
Traceback (most recent call last):
File "C:\Projects\ai-agent\venv\Lib\site-packages\mcp\client\stdio\_\_init**.py", line 155, in stdout_reader
message = types.JSONRPCMessage.model_validate_json(line)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Projects\ai-agent\venv\Lib\site-packages\pydantic\main.py", line 766, in model_validate_json
return cls.**pydantic_validator**.validate_json(
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core.\_pydantic_core.ValidationError: 1 validation error for JSONRPCMessage
Invalid JSON: expected value at line 1 column 2 [type=json_invalid, input_value='[EnhancedContentExtracto...d with browser: 0 chars', input_type=str]
For further information visit https://errors.pydantic.dev/2.12/v/json_invalid
2025-10-25 14:18:05,196 - mcp.client.stdio - ERROR - Failed to parse JSONRPC message from server
Traceback (most recent call last):
File "C:\Projects\ai-agent\venv\Lib\site-packages\mcp\client\stdio\_\_init**.py", line 155, in stdout_reader
message = types.JSONRPCMessage.model_validate_json(line)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Projects\ai-agent\venv\Lib\site-packages\pydantic\main.py", line 766, in model_validate_json
return cls.**pydantic_validator**.validate_json(
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core.\_pydantic_core.ValidationError: 1 validation error for JSONRPCMessage
Invalid JSON: expected value at line 1 column 2 [type=json_invalid, input_value='[EnhancedContentExtracto...roduct-category/iphone/', input_type=str]
For further information visit https://errors.pydantic.dev/2.12/v/json_invalid
2025-10-25 14:18:05,197 - mcp.client.stdio - ERROR - Failed to parse JSONRPC message from server
Traceback (most recent call last):
File "C:\Projects\ai-agent\venv\Lib\site-packages\mcp\client\stdio\_\_init**.py", line 155, in stdout_reader
message = types.JSONRPCMessage.model_validate_json(line)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Projects\ai-agent\venv\Lib\site-packages\pydantic\main.py", line 766, in model_validate_json
return cls.**pydantic_validator**.validate_json(
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core.\_pydantic_core.ValidationError: 1 validation error for JSONRPCMessage
Invalid JSON: expected value at line 1 column 2 [type=json_invalid, input_value='[EnhancedContentExtracto...d 6 successful/0 failed', input_type=str]
For further information visit https://errors.pydantic.dev/2.12/v/json_invalid
2025-10-25 14:18:05,198 - mcp.client.stdio - ERROR - Failed to parse JSONRPC message from server
Traceback (most recent call last):
File "C:\Projects\ai-agent\venv\Lib\site-packages\mcp\client\stdio\_\_init**.py", line 155, in stdout_reader
message = types.JSONRPCMessage.model_validate_json(line)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Projects\ai-agent\venv\Lib\site-packages\pydantic\main.py", line 766, in model_validate_json
return cls.**pydantic_validator**.validate_json(
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core.\_pydantic_core.ValidationError: 1 validation error for JSONRPCMessage
Invalid JSON: expected value at line 1 column 2 [type=json_invalid, input_value='[MCP] Search completed, found 3 results', input_type=str]  
 For further information visit https://errors.pydantic.dev/2.12/v/json_invalid
2025-10-25 14:18:07,234 - core.mcp_manager - INFO - Web search MCP client cleaned up
2025-10-25 14:18:07,235 - **main** - INFO - Response type: <class 'str'>
2025-10-25 14:18:07 INFO discord.gateway Shard ID None has successfully RESUMED session e85cba2dc995cf88e1c7bb940af04a42.
2025-10-25 14:18:07,903 - discord.gateway - INFO - Shard ID None has successfully RESUMED session e85cba2dc995cf88e1c7bb940af04a42.
2025-10-25 14:18:07,957 - **main** - INFO - Response sent to zireael1337

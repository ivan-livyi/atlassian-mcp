#!/usr/bin/env python3

import asyncio
import json
import subprocess
import sys

async def test_cursor_simulation():
    """Test exactly how Cursor calls the MCP server"""
    print("Testing Cursor MCP Communication Simulation")
    print("=" * 45)
    
    # Use exact same command as in mcp.json
    command = ["/Users/ivan/work/atlassian-mcp/.venv/bin/python", "/Users/ivan/work/atlassian-mcp/atlassian_mcp.py"]
    
    try:
        print(f"Starting server with exact Cursor command...")
        
        process = await asyncio.create_subprocess_exec(
            *command,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        print(f"✅ Server started (PID: {process.pid})")
        
        # Step 1: Initialize (exactly like Cursor)
        init_msg = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "roots": {"listChanged": True},
                    "sampling": {}
                },
                "clientInfo": {"name": "cursor", "version": "1.0.0"}
            }
        }
        
        await send_message(process, init_msg)
        init_response = await read_message(process)
        print(f"✅ Initialize response: {init_response.get('result', {}).get('capabilities', {})}")
        
        # Step 2: Send initialized notification (required by MCP protocol)
        initialized_msg = {
            "jsonrpc": "2.0",
            "method": "notifications/initialized",
            "params": {}
        }
        
        await send_message_notification(process, initialized_msg)
        
        # Step 3: Get tools
        tools_msg = {
            "jsonrpc": "2.0", 
            "id": 2,
            "method": "tools/list",
            "params": {}
        }
        
        await send_message(process, tools_msg)
        
        # Capture stderr for debugging
        async def read_stderr():
            try:
                while True:
                    line = await process.stderr.readline()
                    if not line:
                        break
                    print(f"STDERR: {line.decode().strip()}")
            except:
                pass
        
        stderr_task = asyncio.create_task(read_stderr())
        
        try:
            tools_response = await asyncio.wait_for(read_message(process), timeout=10.0)
            tools = tools_response.get('result', {}).get('tools', [])
            print(f"✅ Server returned {len(tools)} tools:")
            for tool in tools:
                print(f"  - {tool.get('name')}")
            
            stderr_task.cancel()
            
            if len(tools) >= 6:
                print("🎉 SUCCESS! Server works exactly like Cursor expects!")
                return True
            else:
                print(f"❌ Server returned {len(tools)} tools, expected 6")
                return False
                
        except asyncio.TimeoutError:
            print("❌ Server is hanging on tools/list without notifications/initialized!")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        if 'process' in locals():
            try:
                process.terminate()
                await process.wait()
            except:
                pass

async def send_message(process, message):
    msg_json = json.dumps(message) + "\n"
    process.stdin.write(msg_json.encode())
    await process.stdin.drain()
    print(f"📤 Sent: {message['method']}")

async def send_message_notification(process, message):
    msg_json = json.dumps(message) + "\n"
    process.stdin.write(msg_json.encode())
    await process.stdin.drain()
    print(f"📤 Sent notification: {message['method']}")

async def read_message(process):
    line = await process.stdout.readline()
    if not line:
        raise Exception("No response from server")
    
    try:
        response = json.loads(line.decode().strip())
        print(f"📥 Received response for: {response.get('id')}")
        return response
    except json.JSONDecodeError as e:
        print(f"❌ Failed to decode JSON response: {line}")
        raise e

if __name__ == "__main__":
    success = asyncio.run(test_cursor_simulation())
    if success:
        print("\n✅ Server works exactly like Cursor expects!")
        print("🔧 Try restarting Cursor now - it should detect 6 tools.")
    else:
        print("\n❌ Server doesn't work like Cursor expects.")
    sys.exit(0 if success else 1) 

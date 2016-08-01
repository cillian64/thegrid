import asyncio
import os.path
import logging
from aiohttp import web
from aiohttp.errors import ClientDisconnectedError

logger = logging.getLogger(__name__)
basepath = os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir))
webpath = os.path.join(basepath, os.pardir, "web")
simpath = os.path.join(basepath, os.pardir, os.pardir, "sim3d")
app = web.Application()
app['sockets'] = []


@asyncio.coroutine
def wshandler(request):
    ws = web.WebSocketResponse()
    yield from ws.prepare(request)
    who = request.transport.get_extra_info('peername')
    logger.info("Websocket connected to %s", who)
    try:
        request.app['sockets'].append(ws)
        while True:
            yield from ws.receive()
    except ClientDisconnectedError:
        pass
    except RuntimeError:
        pass
    finally:
        request.app['sockets'].remove(ws)
        who = request.transport.get_extra_info('peername')
        logger.info("Websocket disconnected from %s", who)
    return ws


@asyncio.coroutine
def simpage(req):
    with open(os.path.join(simpath, "sim3d.html"), "rb") as f:
        return web.Response(body=f.read())


@asyncio.coroutine
def apipage(req):
    with open(os.path.join(webpath, "api.html"), "rb") as f:
        return web.Response(Body=f.read())


@asyncio.coroutine
def on_shutdown(app):
    for ws in app['sockets']:
        yield from ws.close(code=999, message='Server shutdown')


def start_server(host, port):
    app.router.add_route("GET", "/ws", wshandler)
    app.router.add_route("GET", "/sim/", simpage)
    app.router.add_static('/sim/', simpath)
    app.router.add_static('/', webpath)
    app.on_shutdown.append(on_shutdown)
    loop = asyncio.get_event_loop()
    handler = app.make_handler()
    coro = loop.create_server(handler, host, port)
    loop.create_task(coro)
    logger.info("HTTP server running at http://{}:{}/".format(host, port))
    app['handler'] = handler

    # Shut up some of the logging
    weblogger = logging.getLogger("aiohttp.access")
    weblogger.setLevel(logging.WARNING)


def stop_server():
    logger.info("HTTP server shutting down")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(app.shutdown())
    loop.run_until_complete(app['handler'].finish_connections(10.0))
    loop.run_until_complete(app.cleanup())

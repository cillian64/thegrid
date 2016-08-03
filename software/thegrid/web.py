import json
import asyncio
import os.path
import logging
from aiohttp import web
from aiohttp.errors import ClientDisconnectedError

logger = logging.getLogger(__name__)
basepath = os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir))
webpath = os.path.join(basepath, os.pardir, "web")
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
    with open(os.path.join(webpath, "sim", "sim.html"), "rb") as f:
        return web.Response(body=f.read())


@asyncio.coroutine
def simredirect(req):
    return web.Response(status=301, headers={"Location": "/sim/"})


@asyncio.coroutine
def ctrlpage(req):
    with open(os.path.join(webpath, "ctrl.html"), "rb") as f:
        return web.Response(body=f.read())


@asyncio.coroutine
def uipage(req):
    with open(os.path.join(webpath, "ui.html"), "rb") as f:
        return web.Response(body=f.read())


@asyncio.coroutine
def ui(req):
    return web.Response(body=b"OK")


@asyncio.coroutine
def list_patterns(req):
    names = list(iter(req.app['control'].patterns.keys()))
    names.sort()
    return web.Response(body=json.dumps(names).encode())


@asyncio.coroutine
def load_pattern(req):
    name = req.match_info['name']
    if name in req.app['control'].patterns:
        req.app['control'].load_pattern(name)
        return web.Response(body=b"OK")
    else:
        return web.Response(status=404, body=b"Not Found")


@asyncio.coroutine
def on_shutdown(app):
    for ws in app['sockets']:
        yield from ws.close(code=999, message='Server shutdown')


def start_server(host, port, control):
    app.router.add_route("GET", "/ws", wshandler)
    app.router.add_route("GET", "/sim", simredirect)
    app.router.add_route("GET", "/sim/", simpage)
    app.router.add_route("GET", "/ctrl", ctrlpage)
    app.router.add_route("GET", "/", uipage)
    app.router.add_route("GET", "/api/list_patterns", list_patterns)
    load_pattern_resource = app.router.add_resource('/api/load_pattern/{name}')
    load_pattern_resource.add_route('POST', load_pattern)
    app.router.add_route("*", "/ui", ui)
    app.router.add_static('/', webpath)
    app.on_shutdown.append(on_shutdown)
    loop = asyncio.get_event_loop()
    handler = app.make_handler()
    coro = loop.create_server(handler, host, port)
    loop.create_task(coro)
    logger.info("HTTP server running at http://{}:{}/".format(host, port))
    logger.info("Control at http://{}:{}/ctrl".format(host, port))
    logger.info("Simulator at http://{}:{}/sim".format(host, port))
    app['handler'] = handler
    app['control'] = control

    # Shut up some of the logging
    weblogger = logging.getLogger("aiohttp.access")
    weblogger.setLevel(logging.WARNING)


def stop_server():
    logger.info("HTTP server shutting down")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(app.shutdown())
    loop.run_until_complete(app['handler'].finish_connections(10.0))
    loop.run_until_complete(app.cleanup())

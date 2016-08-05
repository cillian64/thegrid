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
def adminpage(req):
    with open(os.path.join(webpath, "admin.html"), "rb") as f:
        return web.Response(body=f.read())


@asyncio.coroutine
def uipage(req):
    with open(os.path.join(webpath, "ui.html"), "rb") as f:
        return web.Response(body=f.read())


@asyncio.coroutine
def homepage(req):
    with open(os.path.join(webpath, "home.html"), "rb") as f:
        return web.Response(body=f.read())


@asyncio.coroutine
def list_patterns(req):
    names = list(iter(req.app['control'].patterns.keys()))
    names.sort()
    return web.Response(body=json.dumps(names).encode())


@asyncio.coroutine
def now_playing(req):
    if req.app['control'].pattern_name is None:
        return web.Response(body="No pattern loaded".encode())
    else:
        return web.Response(body=req.app['control'].pattern_name.encode())


@asyncio.coroutine
def locked(req):
    if req.app['locked']:
        return web.Response(body=b"locked")
    else:
        return web.Response(body=b"unlocked")


@asyncio.coroutine
def lock(req):
    yield from req.post()
    pw = req.POST.get('password')
    if pw == req.app['control'].password:
        req.app['locked'] = True
        return web.Response(body=b"OK")
    else:
        return web.Response(body=b"Auth Err", status=403)


@asyncio.coroutine
def unlock(req):
    yield from req.post()
    pw = req.POST.get('password')
    if pw == req.app['control'].password:
        req.app['locked'] = False
        return web.Response(body=b"OK")
    else:
        return web.Response(body=b"Auth Err", status=403)


@asyncio.coroutine
def reload_patterns(req):
    yield from req.post()
    pw = req.POST.get('password')
    if pw == req.app['control'].password:
        req.app['control'].reload_patterns()
        return web.Response(body=b"OK")
    else:
        return web.Response(body=b"Auth Err", status=403)


@asyncio.coroutine
def load_pattern(req):
    yield from req.post()
    name = req.POST.get('name')
    if req.app['locked']:
        pw = req.POST.get('password')
        if pw != req.app['control'].password:
            return web.Response(body=b"locked", status=403)
    if name in req.app['control'].patterns:
        req.app['control'].load_pattern(name)
        return web.Response(body=b"OK")
    else:
        return web.Response(status=404, body=b"Not Found")


@asyncio.coroutine
def ui(req):
    return web.Response(body=b"")


@asyncio.coroutine
def on_shutdown(app):
    for ws in app['sockets']:
        yield from ws.close(code=999, message='Server shutdown')


def start_server(host, port, control):
    app.router.add_route("GET", "/ws", wshandler)
    app.router.add_route("GET", "/sim", simredirect)
    app.router.add_route("GET", "/sim/", simpage)
    app.router.add_route("GET", "/admin", adminpage)
    app.router.add_route("GET", "/ui", uipage)
    app.router.add_route("GET", "/api/now_playing", now_playing)
    app.router.add_route("GET", "/api/list_patterns", list_patterns)
    app.router.add_route("POST", "/api/reload_patterns", reload_patterns)
    app.router.add_route("POST", "/api/lock", lock)
    app.router.add_route("POST", "/api/unlock", unlock)
    app.router.add_route("GET", "/api/locked", locked)
    app.router.add_route("POST", "/api/load_pattern", load_pattern)
    app.router.add_route("POST", "/api/ui", ui)
    app.router.add_route("GET", "/", homepage)
    app.router.add_static('/', webpath)
    app.on_shutdown.append(on_shutdown)
    loop = asyncio.get_event_loop()
    handler = app.make_handler()
    coro = loop.create_server(handler, host, port)
    loop.create_task(coro)
    logger.info("HTTP server running at http://{}:{}/".format(host, port))
    logger.info("Admin at http://{}:{}/admin".format(host, port))
    logger.info("Simulator at http://{}:{}/sim".format(host, port))
    app['handler'] = handler
    app['control'] = control
    app['locked'] = False

    # Shut up some of the logging
    weblogger = logging.getLogger("aiohttp.access")
    weblogger.setLevel(logging.WARNING)


def stop_server():
    logger.info("HTTP server shutting down")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(app.shutdown())
    loop.run_until_complete(app['handler'].finish_connections(10.0))
    loop.run_until_complete(app.cleanup())

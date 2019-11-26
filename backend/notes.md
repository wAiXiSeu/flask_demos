###流程
##### 启动
`app.run` -> `run_simple` -> _werkzeug middleware_ Start a WSGI application -> `make_server` -> `BaseWSGIServer` -> `request_handler` -> `WSGIRequestHandler` -> `HTTPServer.__init__(self, server_address, handler)`

##### 处理请求
`srv.serve_forever()` -> `HTTPServer.serve_forever(self)` -> `_handle_request_noblock` -> `process_request` -> `finish_request` -> `RequestHandlerClass`(对应前面的requestHandler) -> `BaseRequestHandler.__init()` -> 调用`handle()`方法 -> `handle_one_request` -> `run_wsgi` -> `execute` -> `app(environ, start_response)` -> `flask.__call__()`

##### flask 核心
- `wsgi_app`: 把上下文压入栈，调用路由表对应的处理函数处理相应请求
- `full_dispatch_request`: 处理request, 并将返回结果封装成response `finalize_request`
- hooks:
    - `try_trigger_before_first_request_functions`中处理`before_first_request()`定义的函数
    - `preprocess_request`中处理`before_request`定义的函数
    - `process_response`中处理`after_request`定义的函数
    - `pop`中处理`teardown_request`定义的函数


### 路由
- `app.add_url_rule`: `self.url_map.add(rule)`把 `rule`添加到`url_map`中
```
Here is a small example for matching:
>>> m = Map([
...     Rule('/', endpoint='index'),
...     Rule('/downloads/', endpoint='downloads/index'),
...     Rule('/downloads/<int:id>', endpoint='downloads/show')
... ])
>>> urls = m.bind("example.com", "/")
>>> urls.match("/", "GET")
('index', {})
>>> urls.match("/downloads/42")
('downloads/show', {'id': 42})
```

# callabe - funcao(), objs(), (lambda)(..)
# environ, callback (start_reposnse)
# return iteravel

def application(environ, start_response):
    # faz o que quizer com o requests que em environ
    # print(environ)
    # montar o response
    status = "200 OK"
    headers = [("Content-Type", "text/html")]
    body = b"<stron>Hello World!!!</strong>"
    start_response(status, headers)
    return [body]



#if __name__ == "__main__":
#    from wsgiref.simple_server import make_server
#    server = make_server("0.0.0.0", 8081, application)
#    server.serve_forever()
#

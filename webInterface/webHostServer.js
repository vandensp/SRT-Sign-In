var http = require("http");    //#A
var fs = require('fs');
var index = fs.readFileSync('signInClient.html')
var port = 1444;

// anonymous function - function which handles requests to server
// request - incoming request message
// response - response message to be sent to client
http.createServer(function(request,response){    //#B
    var x;
    var headers = request.headers;
    var trailers = request.trailers;
    console.log('New incoming client request for ' + request.url);
    console.log('Request method: ' + request.method);
    console.log('Headers: ');
    for (x in headers) {
      console.log('\t{' + x + ': \"' + headers[x] + '\"}');
    }
    console.log('Trailers: ');
    for (x in trailers) {
      console.log('\t{' + x + ': \"' + trailers[x] + '\"}');
    }
    response.writeHead(200,    //#C
          {'Content-Type': 'text/html',    //#D
           'Access-Control-Allow-Origin': '*'});    //#E
    //getSRTs();
   
    response.end(index);    //#G
    console.log('Response sent to client\n');
  
  }).listen(port,'');    //#H
  console.log('Server listening on http://localhost:' + port);
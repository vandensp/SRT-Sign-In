var http = require("http");    //#A
var fs = require('fs');
var index
var port = 1444;

// anonymous function - function which handles requests to server
// request - incoming request message
// response - response message to be sent to client
http.createServer(function(request,response){    //#B
    var x;
    var headers = request.headers;
    var trailers = request.trailers;
    var url = request.url;
    var argurl = ''
    var params = ''
    var args = {};
    if (url.includes('?')){
        argurl = url.toString().split('?')[1]
        argurl = argurl.substring(argurl.indexOf('&') + 1);
        if (argurl.includes('&'))
        params = argurl.split('&');
        
    }
    
    
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
    console.log('full url: ');
    console.log(url.toString());
    
    console.log('arg url: ');
    console.log(argurl);
    console.log('Params: ');
    for (x in params) {
        var y = params[x].split('=');
        if (y[0] === 'path') {
            path = y[1].replace('%2F', '/');
            console.log('\t{' + y[0] + ': \"' + path + '\"}');
        }
        else {
            args[y[0]] = y[1];
            console.log('\t{' + y[0] + ': \"' + args[y[0]] + '\"}');
        }
    }
    // separate out parameters from url
    
    if (url.includes('client')){
        response.writeHead(200,    //#C
        {'Content-Type': 'text/html',    //#D
         'Access-Control-Allow-Origin': '*'});    //#E
        index= fs.readFileSync('signInClient.html')
        response.write(index)
    }
    else if (url.includes('srtClient')){
        response.writeHead(200,    //#C
        {'Content-Type': 'text/html',    //#D
         'Access-Control-Allow-Origin': '*'});    //#E
        index = fs.readFileSync('signInSRT.html')
        response.write(index)
    }
    else if (url.includes('studentClient')){
        response.writeHead(200,    //#C
        {'Content-Type': 'text/html',    //#D
         'Access-Control-Allow-Origin': '*'});    //#E
        index = fs.readFileSync('signInStudent.html')
        response.write(index)
    }
    else if (url.includes('jpg')){
        var temp = url.replace('%20', ' ')
        response.writeHead(200,    //#C
        {'Content-Type': 'image/jpeg',    //#D
         'Access-Control-Allow-Origin': '*'});    //#E
        var s = fs.createReadStream('.'+temp);
        s.on('open', function () {
            s.pipe(response);
            });
    }
    else if (url.includes('png')){
        var temp = url.replace('%20', ' ')
        response.writeHead(200,    //#C
        {'Content-Type': 'image/png',    //#D
         'Access-Control-Allow-Origin': '*'});    //#E
        var s = fs.createReadStream('.'+temp);
        s.on('open', function () {
            s.pipe(response);
            });
    }
    else{
        response.writeHead(200,    //#C
        {'Content-Type': 'text/html',    //#D
         'Access-Control-Allow-Origin': '*'})
         
    }
   
    //getSRTs();
   
    response.end();    //#G
    console.log('Response sent to client\n');
  
  }).listen(port,'');    //#H
  console.log('Server listening on http://localhost:' + port);
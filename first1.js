var http=require("http")

http.createServer((request, response)=> {
    console.log("request received");
    response.write("<h1>hello</h1>");
    response.write("<h3>world</h3>");
    response.write("<h6>how</h6>");
    response.end();
}).listen(5060)


    
   
    
    

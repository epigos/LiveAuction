var express = require("express"),
	app 	= express(),
    http    = require("http"),
	server	= http.createServer(app),
	io		= require("socket.io").listen(server),
	cookie_reader = require('cookie'),
    querystring = require('querystring');

	server.listen(4000);

//Configure socket.io to store cookie set by Django
io.configure(function(){
    io.set('authorization', function(data, accept){
        console.log('1');
        if(data.headers.cookie){
            console.log('2');
            data.cookie = cookie_reader.parse(data.headers.cookie);
            return accept(null, true);
        }
        console.log('3');
        return accept('error', false);
    });
    console.log('4');
    io.set('log level', 1);
});

io.sockets.on("connection", function(socket){
    
    socket.on('subscribeAuction', function(auctionId) {
        console.log("Subscribed to room: " + auctionId ); 
        socket.join(auctionId); 
    });

    socket.on('unsubscribeAuction', function(auctionId) { 
        console.log("Unsubscribed to room: " + auctionId ); 
        socket.leave(auctionId); 
    });

    //Client is sendmaking a new bid
    socket.on('newBid', function (data) {
        values = querystring.stringify({
            auctionId: data.auctionId,
            amount: data.amount,
            sessionId: socket.handshake.cookie['sessionid']
        });
        console.log('Sessionid: ' + socket.handshake.cookie['sessionid']);
        var options = {
            host: 'localhost',
            port: 3000,
            path: '/node_api',
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Content-Length': values.length
            }
        };
        
        //Send message to Django server
        var req = http.request(options, function(res){
            res.setEncoding('utf8');
            
            res.on('data', function(resData){
                var response = JSON.parse(resData);
                if(response.success){
                    io.sockets.in(response.auctionId.toString()).emit("notifyNewBid", response);
                }else {
                	console.log('An Error Ocurred: ' + response.message);
                }
            });
        });
        
        req.write(values);
        req.end();
    });
});
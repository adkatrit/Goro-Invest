	//todo: sharpe function and range analysis and storage
	/*
		requires:
		redis
		underscore
		jsftp
	
		This file is meant for hacking around.
		
	
	*/
	var redis_server = 'localhost';
	
	
	//conf is the date range you're pulling from yahoo
	// january is 00 december is 12
	var conf = { 
		'sm':00,
		'sd':1,
		'sy':2011,
		
		'em':11,
		'ed':31,
		'ey':2011,
	};
	var ftp_nasdaq = 'ftp.nasdaqtrader.com';
	var nasdaq_path = '/SymbolDirectory/nasdaqlisted.txt';
	var nasdaq_other_path = '/SymbolDirectory/otherlisted.txt';
	var url = 'http://ichart.finance.yahoo.com/table.csv?a=00&b=1&c=2011&d=11&e=31&f=2011&g=d&ignore=.csv&s='
	var url_YTD = 'http://ichart.finance.yahoo.com/table.csv?a=10&b=8&c=2011&d=10&e=8&f=2012&g=d&ignore=.csv&s='
	
	var http = require('http');
	var redis = require('redis'),
		client = redis.createClient(null,redis_server);
	var _ = require('underscore');
	var Ftp = require('jsftp');
	var ftp = new Ftp({
		host:ftp_nasdaq,
		port:21,
		user:'anonymous',
		pass:'snarf@example.com'
	});
    client.on("error", function (err) {
        console.log("Error " + err);
		process.exit();
    });
	
	/*
		get a file from nasdaq anonymous ftp server
	*/
	getFileFromNasdaq = function(path){
		ftp.get(path,function(err,data){
			if (err)
				return console.error(err);
			console.log('successfully connected to nasdaq ftp server');
			nasdaqFtpToRedis(data.toString());
			ftp.raw.quit();
		});
	}
	/*
		store nasdaq ftp data in redis
	*/
	nasdaqFtpToRedis = function(data){
		_.map(data.split('\n'),function(line){
			var line_vals = line.split('|');
			setRedisStock({
				'name':line_vals[0],
				'description':line_vals[1]
			});
		});
	}
	
	/*
		store stock data by javascript object
		using object['name'] as key
	*/
	setRedisStock = function(stock_data){
		client.select(54,function(){
			client.hmset(stock_data['name'],stock_data);
		});
	}
	/*
		store stock data by symbol,key,value
	*/
	setRedisStockKey = function(symbol,key,value){
		client.select(54,function(){
			client.hset(symbol,key,value);
		});
	}
	/*
		print redis stock by symbol
	*/
	printRedisStock = function(stock_symbol){
		client.select(54,function(){
			if(stock_symbol!=-1){
				client.hgetall(stock_symbol,function(err,replies){
					console.log(replies);
				});
			}
		});
	}
	/*
		using values in redis
		get price data and store back in redis
	*/
	fetchAllStockDataRedis = function(){
		client.select(54,function(){
			client.keys('*',function(err,replies){
				_.map(replies,getStockDataFromYahoo);
			});
		});
	}
	/*
		callback for the calls to yahoo finance
	*/
	
	yahoo_callback = function(response,req){
		var str = '';
		response.on('data', function(chunk){
			str += chunk;
		});
		response.on('end', function(){
			var req_path = this['req']['path'].split('=');
			var current_symbol = req_path[req_path.length-1];			
			_.map(str.split('\n').slice(1),function(line){
				var line_arr = line.split(',');
				//open, high, low, close, volume, adj_close
				var line_str = line_arr.slice(1).join(',');
				var date = line_arr[0]
				var n = Number(line_arr[1]);
				if(!_.isNaN(n)){
					setRedisStockKey(current_symbol,date,line_str);
				}
			});
		});
	}
	/*
		pull a stock's financial data from yahoo using the global conf for date range
	*/
	getStockDataFromYahoo = function(symbol){
		var yahoo_finance_opts = {
			host: 'ichart.finance.yahoo.com',
			path: '/table.csv?a='+conf.sm+'&b='+conf.sd+'&c='+conf.sy+'&d='+conf.em+'&e='+conf.ed+'&f='+conf.ey+'&g=d&ignore=.csv&s='+symbol
		}
		http.request(yahoo_finance_opts,yahoo_callback).end();
	}
	
	


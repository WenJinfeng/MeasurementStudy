
exports.handler = (event, context, callback) => {
    // const eventObj = JSON.parse(event.toString());
    var tm_st = (new Date()).valueOf();
    console.log('hello world');
    
    callback(null, tm_st);
  }
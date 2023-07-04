exports.handler = async(event) => {
    // TODO implement
    var tm_st = (new Date()).valueOf();
    const response = {
        statusCode: 200,
        body: JSON.stringify('Hello from Lambda!'),
    };
    return tm_st;
};

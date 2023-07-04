module.exports = async function (context, req) {
    var tm_st = (new Date()).valueOf();
    context.res = {
        body: ",timepoint:"+tm_st
    };
}
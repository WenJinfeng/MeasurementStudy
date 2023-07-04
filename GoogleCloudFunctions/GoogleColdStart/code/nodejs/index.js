
  exports.handler = (req, res) => {
    var tm_st = (new Date()).valueOf();
    let message = 'Hello World!';
    res.status(200).send(",timepoint:"+tm_st);
  };
  
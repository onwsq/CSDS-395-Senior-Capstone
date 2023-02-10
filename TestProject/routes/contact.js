var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/contact', function(req, res, next) {
  res.render('contact', { title: 'Contact Page' });
});

router.get('/algorithm', function(req, res, next) {
  res.render('algorithm', { title: 'Express' });
});

module.exports = router;

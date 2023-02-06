var express = require('express');
var router = express.Router();

/* GET users listing. */
router.get('/', function(req, res, next) {
  res.render('homepage', { title: 'Express' });
});

router.get('/contact', function(req, res, next) {
  res.render('contact', { title: 'Express' });
});

router.get('/users', function(req, res, next) {
  res.render('users', { title: 'Express' });
});

module.exports = router;

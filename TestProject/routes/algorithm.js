var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('homepage', { title: 'Express' });
});

router.get('/contact', function(req, res, next) {
  res.render('contact', { title: 'Express' });
});

router.get('/users', function(req, res, next) {
  res.render('users', { title: 'Express' });
});

router.get('/newprofile', function(req, res, next) {
  res.render('newprofile', { title: 'Express' });
});

router.get('/algorithm', function(req, res, next) {
    res.render('algorithm', { title: 'Express' });
});

module.exports = router;

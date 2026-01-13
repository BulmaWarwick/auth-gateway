const { Router } = require('express');
const axios = require('axios');

const router = Router();

router.use((req, res, next) => {
  const authHeader = req.get('Authorization');
  if (!authHeader) {
    return res.status(401).send('Unauthorized');
  }
  const [authType, token] = authHeader.split(' ');
  if (authType !== 'Bearer') {
    return res.status(401).send('Unauthorized');
  }
  axios.post('/validate-token', { token })
    .then(response => {
      if (response.status === 200) {
        req.user = response.data;
        next();
      } else {
        return res.status(401).send('Unauthorized');
      }
    })
    .catch(error => {
      return res.status(401).send('Unauthorized');
    });
});

module.exports = router;
const express = require('express');
const axios = require('axios');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json()); // To parse JSON bodies

app.get('/', (req, res) => {
    res.send('Hello from our server!');
});

app.post('/ask', async (req, res) => {
    try {
        const response = await axios.post('http://localhost:5000/invoke', {
            question: req.body.question
        });
        res.send(response.data);
    } catch (error) {
        res.status(500).send({ error: 'Error calling Python API' });
    }
});

app.listen(8080, () => {
    console.log('Server listening on port 8080');
});


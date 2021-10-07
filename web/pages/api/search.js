import { get } from 'axios';

export default (req, res) => {
    console.log('request', req.query.q);
    console.log('process.env.API_ENDPOINT:', process.env.API_ENDPOINT)
    //return res.status(200).json({"status":"ok"});

    return get(`${process.env.API_ENDPOINT}/v1/event/${req.query.q}/spans`)
        .then(function (response) {
            console.log(`response from server: ${JSON.stringify(response.data)}`);
            res.status(200).json(response.data);
        })
        .catch(function (error) {
            console.log(`error calling api: ${error}`);
            res.status(400).json(error);
        })
        .then(function () {
        });
}

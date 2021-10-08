import { get } from 'axios';

export default (req, res) => {
    let endpoint;

    if (req.query.e.length) {
        endpoint = `${process.env.API_ENDPOINT}/v1/event/${req.query.e}/spans`
    }
    else if (req.query.c.length) {
        endpoint = `${process.env.API_ENDPOINT}/v1/context/${req.query.c}/spans`
    }

    return get(endpoint)
        .then(function (response) {
            res.status(200).json(response.data);
        })
        .catch(function (error) {
            res.status(400).json(error);
        })
        .then(function () {
        });
}

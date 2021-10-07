import { get } from 'axios';

export default (req, res) => {
    return get(`${process.env.API_ENDPOINT}/v1/event/${req.query.q}/spans`)
        .then(function (response) {
            res.status(200).json(response.data);
        })
        .catch(function (error) {
            res.status(400).json(error);
        })
        .then(function () {
        });
}

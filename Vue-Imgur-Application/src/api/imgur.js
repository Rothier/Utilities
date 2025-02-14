import qs from 'qs';
import axios from 'axios';

const CLIENT_ID = "c5c4a44a06615b0"
const ROOT_URL = "https://api.imgur.com"

export default {
    login () {
        const querystring = {
            client_id: CLIENT_ID,
            response_type: "token",
        };
        window.location = `${ROOT_URL}/oauth2/authorize?${qs.stringify(querystring)}`
    },
   fetchImages(token) {
        return axios.get(`${ROOT_URL}/3/account/me/images`, {
            headers: {
                Authorization: `Bearer ${token}`
            }
        })
    },
    uploadImages(images, token){
            const promises = Array.from(images).map( image => {
            const formData = new FormData();
            formData.append('image', image)

            return axios.post(`${ROOT_URL}/3/image`, formData, {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            })
        })
        return Promise.all(promises)
    }
};

/* http://localhost:8080/oauth2/callback#
access_token=580169ad85bb352ca9bed288a4bcc1b80e6d7c76&
expires_in=315360000&
token_type=bearer&
refresh_token=0926461d6f8fd288dbc9cedb76571900bc77afdd&
account_username=ARothier&
account_id=142767259 */
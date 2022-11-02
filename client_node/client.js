function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

const axios = require("axios");

const axiosApi = axios.create();

let refresh_token;
let access_token;


axiosApi.interceptors.response.use(
    async (resp) => {
        return resp
    },
    async (error) => {
        const resp = error.response;
        const req_config = error.response.config

        if(resp.status == 401){
            console.log('Try get new access token')
            let config = { headers: { Cookie: refresh_token } };
            let refresh_resp = await axios.post('http://localhost:3001/token/refresh', data={}, config);
            if(refresh_resp.status == 200) {
                console.log(`Retry request to ${req_config.url} - ${req_config}`)
                access_token = refresh_resp.headers['set-cookie'][0];
                req_config.headers = { Cookie: access_token };
                new_resp = await axios(req_config);
                return new_resp
            }
            return refresh_resp
        }
    }
);


async function login(){
    try {
        const resp = await axios.post('http://localhost:3001/login', data={email: 'user1@user.com', password: '123456!!'});

        if(resp.status == 200) {
            access_token = resp.headers['set-cookie'][0];
            refresh_token = resp.headers['set-cookie'][1];
        }
        // return {data: resp.data, status: resp.status, access_token, refresh_token}
        return {data: resp.data, status: resp.status}
    } catch (error){
        return error.response
    }
}

async function refresh(){
    try {
        let config = { headers: { Cookie: refresh_token } };
        const resp = await axios.post('http://localhost:3001/token/refresh', data={}, config);

        let access_token
        if(resp.status == 200) {
            access_token = resp.headers['set-cookie'][0];
        }
        return {data: resp.data, status: resp.status, access_token}
    } catch (error){
        return error.response
    }
}



async function users(){
    try {
        let config = { headers: { Cookie: access_token } };
        let resp = await axios.get('http://localhost:3001/users/', config);
        return {data: resp.data, status: resp.status}
    } catch (error){
        if(error.response.status == 401){
            try {
                let config = { headers: { Cookie: refresh_token } };
                resp = await axios.post('http://localhost:3001/token/refresh', data={}, config);
                config = { headers: { Cookie: resp.headers['set-cookie'][0] } };
                resp = await axios.get('http://localhost:3001/users/', config);
                return {data: resp.data, status: resp.status}
            } catch(erro){
                return error.response
            }
        }else{
            return error.response
        }
    }
}

async function users2(){
    try {
        let config = { headers: { Cookie: access_token } };
        let resp = await axiosApi.get('http://localhost:3001/users/', config);
        return {data: resp.data, status: resp.status}
    } catch (error){
        return error.response
    }
}


async function main(){

    let resp = await login()
    console.log(resp)

    resp = await users2()
    console.log(resp)

    sleep(6000).then( async () => {
            resp = await users2()
            console.log(resp)
        }
    )

}

main()
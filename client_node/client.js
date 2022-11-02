const axios = require("axios");


function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function login(){
    try {
        const resp = await axios.post('http://localhost:3001/login', data={email: 'user1@user.com', password: '123456!!'});
        if(resp.status == 200) {
            access_token = resp.headers['set-cookie'][0]
            refresh_token = resp.headers['set-cookie'][1]
        }
        return {data: resp.data, status: resp.status, access_token, refresh_token}
    } catch (error){
        return error.response
    }
}


async function users(access_token, refresh_token){
    try {
        config = { headers: { Cookie: access_token } };
        let resp = await axios.get('http://localhost:3001/users/', config);
        return {data: resp.data, status: resp.status}
    } catch (error){
        if(error.response.status == 401){
            try {
                resp = await axios.post(
                       'http://localhost:3001/token/refresh',
                        {
                          headers: {
                             Cookie: refresh_token
                            }
                        });
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

async function main(){

    const {data, status, access_token, refresh_token} = await login()

    console.log(data, status, access_token, refresh_token)

    let resp = await users(access_token)
    console.log(resp.status, resp.data)

    sleep(6000).then( async () => {
            resp = await users(access_token, refresh_token)
            console.log(resp.status, resp.data)
        }
    )


}

main()
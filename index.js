const express = require('express');  // Express 모듈을 가져와서 웹 서버를 설정하기 위한 기반으로 사용합니다.
const bodyParser = require('body-parser');  // 요청 본문을 JSON 형식으로 파싱하기 위해 body-parser 미들웨어를 사용합니다.
const axios = require('axios');  // HTTP 요청을 처리하기 위해 axios 모듈을 가져옵니다.
const {
  saveChatAndResponseToFirestore,
} = require('./firebase'); // Firebase 관련 함수들을 불러옵니다. 여기서는 Firestore에 데이터를 저장하는 함수가 포함됩니다.

const app = express();  // Express 애플리케이션을 생성합니다.
const port = 3000;  // 서버가 실행될 포트 번호를 지정합니다.

// JSON 형식의 요청 본문을 처리하기 위해 body-parser 미들웨어를 사용합니다.
app.use(bodyParser.json());

// 카카오 챗봇에서 들어오는 요청을 처리하는 엔드포인트를 설정합니다.
app.post('/kakao', (req, res) => {
    const userRequest = req.body.userRequest.utterance;  // 카카오에서 전달된 사용자의 메시지를 추출합니다.
    const userId = req.body.userRequest.user.id;  // 카카오에서 제공하는 유저의 고유 ID를 추출합니다.
    const chatTokenUsage = calculateTokenUsage(userRequest);  // 유저가 보낸 메시지의 길이를 기반으로 채팅에서 사용된 토큰 수를 계산합니다.

    // Python 서버와 통신하여 유저의 요청을 처리하고, 그 결과를 콜백 함수로 전달합니다.
    processRequestWithPythonServer(userRequest, async (error, pythonResponse) => {
        if (error) {
            console.error('Error communicating with Python server:', error);  // Python 서버와의 통신 중 오류가 발생하면 콘솔에 오류를 출력합니다.
            return res.status(500).json({  // 클라이언트에게 500 서버 오류 응답을 반환합니다.
                version: "2.0",
                template: {
                    outputs: [
                        {
                            simpleText: {
                                text: '서버 에러가 발생했습니다. 잠시 후 다시 시도해주세요.'  // 사용자에게 오류 메시지를 반환합니다.
                            }
                        }
                    ]
                }
            });
        }

        const gptResponse = pythonResponse.template.outputs[0].simpleText.text;  // Python 서버에서 받은 GPT 응답 메시지를 추출합니다.
        const responseTokenUsage = calculateTokenUsage(gptResponse);  // GPT 답장 메시지의 길이를 기반으로 토큰 사용량을 계산합니다.

        // Firestore에 유저 메시지와 GPT 응답, 그리고 각각의 토큰 사용량을 저장합니다.
        await saveChatAndResponseToFirestore(userId, userRequest, gptResponse, chatTokenUsage, responseTokenUsage);

        // Python 서버에서 받은 응답을 클라이언트(카카오 챗봇)로 그대로 반환합니다.
        res.json(pythonResponse);
    });
});

// Python 서버에 요청을 전달하고 응답을 처리하는 함수입니다.
function processRequestWithPythonServer(userRequest, callback) {
    axios.post('http://localhost:5001/process', {  // Python 서버의 /process 엔드포인트로 POST 요청을 보냅니다.
        userRequest: userRequest  // 유저가 보낸 메시지를 요청 본문에 포함시킵니다.
    })
    .then(response => {  // 요청이 성공하면 응답 데이터를 처리합니다.
        callback(null, response.data);  // 콜백 함수를 호출하여 Python 서버의 응답 데이터를 전달합니다.
    })
    .catch(error => {  // 요청 중 오류가 발생하면 오류를 처리합니다.
        callback(error, null);  // 콜백 함수를 호출하여 오류를 전달합니다.
    });
}

// 텍스트의 길이를 기반으로 토큰 사용량을 계산하는 함수입니다.
function calculateTokenUsage(text) {
    // 예시로, 텍스트의 길이(문자 수)를 토큰 사용량으로 간주합니다.
    return text.length;
}

// 서버를 시작하고, 지정된 포트에서 클라이언트 요청을 대기합니다.
app.listen(port, () => {
    console.log(`Kakao chatbot server is running on http://localhost:${port}`);  // 서버가 성공적으로 시작되었음을 콘솔에 출력합니다.
});

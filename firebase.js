// const firebase = require("firebase-admin");
// const serviceAccount = require("./firebase-adminsdk.json");  // 서비스 계정 키 파일 경로

// firebase.initializeApp({
//   credential: firebase.credential.cert(serviceAccount)
// });

// const db = firebase.firestore();


// function saveChatToFirestore(userId, message) {
//   // 'kakao_chatbot' 컬렉션에서 사용자 문서를 참조하고, 해당 문서의 'messages' 서브컬렉션에 접근합니다.
//   const messagesRef = db.collection('kakao_chatbot').doc(userId).collection('messages');
  
//   // 서브컬렉션에 새로운 메시지를 추가합니다. 고유한 문서 ID는 Firestore가 자동으로 생성합니다.
//   return messagesRef.add({
//     message: message, // 저장할 메시지 내용
//     timestamp: firebase.firestore.FieldValue.serverTimestamp(), // 서버 시간을 타임스탬프로 저장
    
//   });
// }

// module.exports = {
//   saveChatToFirestore // saveChatToFirestore 함수를 모듈로 내보냅니다.
// };


// function getMessagesFromFirestore(userId) {
//   // 특정 사용자의 메시지 서브컬렉션을 참조합니다.
//   const messagesRef = db.collection('kakao_chatbot').doc(userId).collection('messages');

//   // 서브컬렉션의 모든 메시지를 가져옵니다.
//   return messagesRef.orderBy('timestamp').get().then(snapshot => {
//     const messages = [];
//     snapshot.forEach(doc => {
//       messages.push({
//         id: doc.id, // 메시지 문서의 ID
//         message: doc.data().message, // 메시지 내용
//         timestamp: doc.data().timestamp // 타임스탬프
        
        
//       });
//     });
//     return (messages, tokenUsage);
//   });

//   function saveTokenUsageToFirestore(userId, prompt, tokensUsed) {
//     const tokenUsageRef = db.collection("gpt_token_usage").doc(userId).collection("usages");
  
//     tokenUsageRef.add({
//       prompt: prompt,
//       tokensUsed: tokensUsed,
//       timestamp: firebase.firestore.FieldValue.serverTimestamp(),
//     });
  
//     console.log(`Saved token usage for user ${userId}`);
//   }


// }








//기능: massage 내용이랑, 카톡 보낸 시간, open ai api 사용한 토큰 수 보기

const firebase = require("firebase-admin");
const serviceAccount = require("./firebase-adminsdk.json");  // 서비스 계정 키 파일 경로

firebase.initializeApp({
  credential: firebase.credential.cert(serviceAccount)
});

const db = firebase.firestore();

// Firestore에 메시지 저장
function saveChatToFirestore(userId, message) {
  const messagesRef = db.collection('kakao_chatbot').doc(userId).collection('messages');
  
  return messagesRef.add({
    message: message, // 저장할 메시지 내용
    timestamp: firebase.firestore.FieldValue.serverTimestamp(), // 서버 시간을 타임스탬프로 저장
  });
}

// Firestore에 사용한 토큰 수 저장
function saveTokenUsageToFirestore(userId, prompt, tokensUsed) {
  const tokenUsageRef = db.collection("gpt_token_usage").doc(userId).collection("usages");
  
  return tokenUsageRef.add({
    prompt: prompt,
    tokensUsed: tokensUsed,
    timestamp: firebase.firestore.FieldValue.serverTimestamp(),
  }).then(() => {
    console.log(`Saved token usage for user ${userId}`);
  }).catch((error) => {
    console.error("Error saving token usage: ", error);
  });
}

// Firestore에서 메시지와 토큰 사용량 가져오기
function getMessagesFromFirestore(userId) {
  const messagesRef = db.collection('kakao_chatbot').doc(userId).collection('messages');
  
  return messagesRef.orderBy('timestamp').get().then(snapshot => {
    const messages = [];
    snapshot.forEach(doc => {
      messages.push({
        id: doc.id, // 메시지 문서의 ID
        message: doc.data().message, // 메시지 내용
        timestamp: doc.data().timestamp // 타임스탬프
      });
    });
    return messages;
  });
}

// Firestore에서 토큰 사용량 가져오기
function getTokenUsageFromFirestore(userId) {
  const tokenUsageRef = db.collection("gpt_token_usage").doc(userId).collection("usages");

  return tokenUsageRef.orderBy("timestamp").get().then(snapshot => {
    const tokenUsages = [];
    snapshot.forEach(doc => {
      tokenUsages.push({
        id: doc.id,
        prompt: doc.data().prompt,
        tokensUsed: doc.data().tokensUsed,
        timestamp: doc.data().timestamp,
      });
    });
    return tokenUsages;
  });
}

// 메시지와 토큰 사용량을 가져와 함께 출력하기
async function getMessagesAndTokenUsage(userId) {
  const messages = await getMessagesFromFirestore(userId);
  const tokenUsage = await getTokenUsageFromFirestore(userId);

  console.log("Messages:", messages);
  console.log("Token Usage:", tokenUsage);

  return { messages, tokenUsage };
}

module.exports = {
  saveChatToFirestore,
  saveTokenUsageToFirestore,
  getMessagesAndTokenUsage,
};

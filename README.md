## Azure 기반 OpenAI 채팅 에이전트
이 프로젝트는 Microsoft Azure의 다양한 서버리스 서비스와 OpenAI의 GPT 모델을 결합하여 구축한 실시간 웹 채팅 애플리케이션입니다. 사용자의 메시지에 대해 AI가 응답하고, 대화 내용은 Cosmos DB에 저장됩니다.

## 주요 아키텍처
![제목 없는 다이어그램](https://github.com/user-attachments/assets/c5a20c26-cb13-47be-895f-18d68a219302)

### Frontend (HTML, JS)
- 사용자는 웹 브라우저를 통해 메시지를 입력합니다.
- 정적 파일(html, css, favicon 등)은 Azure Blob Storage에서 제공됩니다.

### Azure Web PubSub
- 프론트엔드와 백엔드 간의 실시간 양방향 통신을 담당합니다.

### Azure Functions (Python)
- 사용자의 요청을 받아 처리하는 핵심 비즈니스 로직이 실행됩니다.
- API Functions - FastAPI를 통해 Pubsub 토큰 생성, 채널 생성, 사용자의 메세지를 DB, ServiceBus에 전달합니다.
- Agent Function - ServiceBus의 request 큐에 메세지가 들어왔을 경우 해당 메세지를 OpenAI의 API를 통해 답변을 전달, 받아옵니다
- Response Function - ServiceBus의 response 큐에 메세지가 들어왔을 경우 해당 메세지를 DB에 저장하고 Azure PubSub에 메세지를 전달합니다.

### Azure Service Bus
- 메시지를 비동기적으로 전달하거나 처리할 수 있습니다.

### Azure Cosmos DB (MongoDB)
- 대화 기록, 채팅 정보 등 주요 데이터를 저장하고 관리하는 MongoDB 데이터베이스입니다.

### OpenAI API
- 사용자의 질문에 대한 답변을 생성하는 AI 모델입니다.

## 웹페이지 화면
![image](https://github.com/user-attachments/assets/f32364db-6a46-45db-b5aa-360cd2ca4b37)


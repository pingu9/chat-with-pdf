# 금융 마이데이터 Q&A 에이전트

## 소개

이 어플리케이션은 금융 마이데이터 관련 PDF 문서에서 정보를 추출하고, 해당 내용을 바탕으로 질문에 답변하는 애플리케이션입니다. 이 프로젝트는 LLM(chatGPT-4o-mini) 어플리케이션이며, 다음 2개의 PDF를 텍스트 청킹하여 RAG 파이프라인을 구성합니다. 

1. [(221115 수정배포) (2022.10) 금융분야 마이데이터 기술 가이드라인.pdf](https://www.mydatacenter.or.kr:3441/cmmn/fileBrDownload?id=JHuKqjlWK0e%2FH9Yi7ed09GsZWL6TiRKp9yg4qGj%2FKFmV9RC6j8RJdh6I8JAqzoFv&type=2)  

2. [(수정게시) 금융분야 마이데이터 표준 API 규격 v1.pdf](https://www.mydatacenter.or.kr:3441/cmmn/fileBrDownload?id=dKi%2B7cAM4PO8JA4z7jwm4AoM07vmQIbSKQ9EvM0DPRYokFCd%2BhLigsDUZ0hQopjD&type=2)

이 때 벡터 DB로는 ChromaDB를 이용합니다.
또한 멀티턴으로 동작하여 이전 대화 내용을 기억합니다.
프론트엔드는 streamlit으로 구성되어 있습니다.


프로젝트 내 파일에 대한 간략한 설명은 다음과 같습니다.

document_processor.py: pymupdf 모듈을 이용하여 PDF 문서를 document로 변환합니다.

retriever.py: chromaDB와 openAIEmbedding을 이용하여 벡터 스토어에 pdf문서를 저장합니다.

models.py  주어진 사용자 입력, 그 동안의 채팅 히스토리, 벡터 스토어에 저장된 내용을 이용해 답변을 생성합니다.

streamlit_ui.py: streamlit을 이용하여 멀티 턴 채팅 형태의 ui를 구성합니다.


## 프로젝트 실행 방법
1. 배포된 프로젝트 위치
   - 다음 위치에서 어플리케이션을 실행해볼 수 있습니다.
   - http://ec2-3-39-253-229.ap-northeast-2.compute.amazonaws.com/
2. 로컬 빌드 시
    - 아래 가이드를 참조하여 로컬 빌드 및 실행할 수 있습니다.

## 로컬 실행 시 사전 준비 사항

프로젝트를 실행하기 전에 아래와 같은 환경이 필요합니다:

- **Docker**: 이 프로젝트는 Docker 컨테이너에서 실행됩니다. Docker가 설치되어 있어야 합니다.
- **Docker Compose**: docker와 함께 설치가 필요합니다.
- **OpenAI API Key**: 벡터 임베딩, gpt 모델 실행을 위해 OpenAI API 키가 필요합니다.

## 로컬 실행하기

프로젝트를 설정하고 실행하려면 다음 단계를 따르세요.

### 리포지토리 클론 및 디렉토리 이동

먼저, 프로젝트 리포지토리를 로컬 머신에 클론한 후 해당 디렉토리로 이동합니다.

### make 명령어를 이용하여 프로젝트 실행
미리 설정된 Makefile을 이용하여 프로젝트를 실행할 수 있습니다.
이용할 수 있는 커맨드는 다음과 같습니다.
1. make: 해당 커맨드 입력시 쉘에서 OPENAI_API_KEY와 STREAMLIT_PORT를 입력받습니다. 이후 컨테이너를 빌드하고 실행합니다. 만약 해당 환경변수를 설정해놓은 상태라면 입력 과정은 생략됩니다. 실행된 이후 웹 브라우저 창에서 localhost:${STREAMLIT_PORT} 창에 접속해 결과를 확인할 수 있습니다.
2. make clean: 해당 커맨드 입력 시 프로그램을 종료합니다.
3. make shell: 해당 프로젝트가 실행중인 상태라면 쉘에 접속할 수 있습니다.

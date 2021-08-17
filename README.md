# RPC_example
RPC를 통한 WorkerServer 함수 Invoke 예제 코드 수록 및 실행시간 테스트

## Usage

1. Prepare `secret_params.py` file and put it into the `/worker_server` directory.

2. Install the prerequisite packages via pip.
    ```
    pip install -r requirements.txt
    ```
3. Run the job_consumer server daemon.
    ```
    python worker_server/job_consumer.py
    ```
4. Run the test code. (fibonacci 32)
    ```
    python time_test.py
    ```

## Results

> CASE 1: LOCAL INVOKE (함수를 직접 import 하여 코드 실행)

> CASE 2: MSG_QUEUE INVOKE - RPC Pattern 
(job_consumer daemon이 메세지 큐의 인자를 전달받아 실행 후 반환)

- CASE 1의 경우 0.64초 가량 수행
- CASE 2의 경우 0.68초 가량 수행

MSG QUEUE가 완전히 다른 네트워크에 있는 상태에서
네트워크에 의한 지연 0.04초 가량이 추가된다고 볼 수 있다.
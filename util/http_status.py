def get_http_status(code):
    options = {
        200: "OK", # 요청 성공
        201: "CREATED", # 요청 성공, 생성됨
        202: "ACCEPTED", # 요청 수신 했지만 처리되지 않음
        204: "NO_CONTENT", # 요청 성공, 내용 없음
        205: "RESET_CONTENT", # 요청 성공, 내용 초기화
        301: "MOVED_PERMANENTLY", # 요청한 자원이 영구적으로 이동됨
        302: "FOUND", # 요청한 자원이 임시로 이동됨
        304: "NOT_MODIFIED", # 요청한 자원이 기존과 동일하여 변경되지 않음
        400: "BAD_REQUEST", # 잘못된 요청
        401: "UNAUTHORIZED", # 인증되지 않음
        403: "FORBIDDEN", # 접근 금지
        404: "NOT_FOUND", # 요청한 자원을 찾을 수 없음
        405: "METHOD_NOT_ALLOWED", # 허용되지 않는 메소드
        406: "NOT_ACCEPTABLE", # 허용되지 않는 요청
        408: "REQUEST_TIMEOUT", # 요청 시간 초과
        409: "CONFLICT", # 요청 충돌
        410: "GONE", # 요청한 자원이 삭제됨
        422: "UNPROCESSABLE_ENTITY", # 요청 처리 불가
        423: "LOCKED", # 리소스 접근 금지
        429: "TOO_MANY_REQUESTS", # 너무 많은 요청
        500: "INTERNAL_SERVER_ERROR", # 서버 내부 오류
        501: "NOT_IMPLEMENTED", # 서버가 요청을 수행할 수 없음
        502: "BAD_GATEWAY", # 잘못된 게이트웨이
        503: "SERVICE_UNAVAILABLE", # 서비스를 사용할 수 없음
        504: "GATEWAY_TIMEOUT", # 게이트웨이 시간 초과
    }
    
    return options[code]
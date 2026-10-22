# KBO 데이터룸

네이버 스포츠 문자중계를 원천 데이터로 수집하고, KBO 공식 기록실을 마스터 대조에 사용하며, 스탯티즈는 수동 검증에만 사용하는 KBO 분석 프로젝트입니다.

- 웹 대시보드: <https://baseball-data-room.leeminseo2249.chatgpt.site/>
- GitHub 저장소: <https://github.com/Leeminseo0718/KBO_baseball>

## 데이터 원칙

- 네이버 JSON 원본은 `source_snapshot`과 파일에 수정 없이 보존합니다.
- 네이버 `pcode`는 KBO 공식 `playerId` 페이지에서 선수명과 표본 대조합니다.
- KBO 선수 등록 현황을 기준으로 10개 구단의 등록 명단, 등번호, 포지션을 제공합니다.
- 스탯티즈 콘텐츠는 자동 수집하거나 재배포하지 않습니다.
- 수집기는 종료 경기를 기본 대상으로 하며, 요청 간격과 재시도를 적용합니다.
- Text-to-SQL은 성적 조회, 선수 비교, 시계열 추이, 순위 조회만 허용합니다.
- SQL은 읽기 전용 단일 문장, 허용 뷰, 행 수 제한을 통과해야 실행됩니다.

## VS Code에서 프로젝트 열기

### VS Code 화면에서 Clone하기

1. VS Code를 실행합니다.
2. `Cmd + Shift + P`(Windows는 `Ctrl + Shift + P`)를 눌러 명령 팔레트를 엽니다.
3. `Git: Clone`을 선택합니다.
4. 아래 저장소 주소를 입력합니다.

   ```text
   https://github.com/Leeminseo0718/KBO_baseball.git
   ```

5. 프로젝트를 저장할 폴더를 고른 뒤 `Open`을 선택합니다.
6. VS Code 상단 메뉴에서 `Terminal > New Terminal`을 선택해 실행 명령을 입력합니다.

### 터미널에서 Clone한 뒤 열기

```bash
git clone https://github.com/Leeminseo0718/KBO_baseball.git
cd KBO_baseball
code .
```

macOS에서 `code` 명령을 찾을 수 없다면 VS Code 명령 팔레트에서 `Shell Command: Install 'code' command in PATH`를 실행하거나, `File > Open Folder`에서 `KBO_baseball` 폴더를 선택합니다.

## 대시보드 빠르게 확인하기

별도 패키지 설치 없이 정적 대시보드만 확인하려면 다음 명령을 실행합니다.

```bash
python3 -m http.server 4173 --directory dist
```

브라우저에서 <http://127.0.0.1:4173>을 열면 됩니다.

## 데이터 파이프라인과 API 실행하기

Python 3.11 이상과 Docker Desktop이 필요합니다.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
cp .env.example .env
docker compose up -d postgres
python -m kbo_data.pipeline --date 2026-09-09 --game-id 20260909KTSS02026 --verify-player 69446:원태인
uvicorn kbo_data.api:app --reload
```

Windows PowerShell에서는 가상환경 활성화 명령으로 아래 명령을 사용합니다.

```powershell
.venv\Scripts\Activate.ps1
```

API가 실행되면 <http://127.0.0.1:8000/health>에서 상태를 확인할 수 있습니다. PostgreSQL 연결 정보나 OpenAI API 키가 필요하면 `.env`에 값을 설정하세요. 비밀 키가 들어간 `.env` 파일은 Git에 올리지 않습니다.

매일 수집은 `.github/workflows/daily-pipeline.yml`과 같은 명령을 실행합니다. PostgreSQL과 API는 브라우저에 직접 노출하지 않고, 대시보드는 API만 호출합니다.

`OPENAI_API_KEY`가 없을 때는 검증 가능한 템플릿 플래너가 네 가지 질문 유형을 처리합니다. 키가 준비되면 Responses API Structured Outputs 어댑터를 활성화할 수 있도록 경계를 분리했습니다.

## 검증 기준

`python -m kbo_data.eval_runner`는 `evals/text_to_sql_cases.jsonl`의 50개 질문을 검사합니다. 목표는 지원 질문 정확도 89% 이상, 위험하거나 범위를 벗어난 질문 거절률 100%입니다.

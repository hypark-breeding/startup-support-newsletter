# 정부 창업지원사업 뉴스레터

한국 정부와 공공기관의 창업지원사업 공고를 에이전트가 찾아보고, 지역별 브리핑, 일자별 일정표, 뉴스레터, 사업계획서 fit 분석 형태로 정리할 수 있게 만든 스킬 프로젝트입니다.

기본 범위는 전국입니다. 사용자가 URL을 제공하지 않아도 GPT Researcher와 Crawl4AI로 공식 출처 후보를 찾고 검증합니다.

예상 질문은 이런 형태입니다.

- "전국에서 올해 열린 창업지원사업과 반복 가능성이 높은 사업 모아줘"
- "부산/경남 AI 스타트업이 볼 만한 지원사업, 행사, 수주 공고 찾아줘"
- "URL은 모르는데 이번 주 창업지원사업 뉴스레터 만들어줘"

## 접근 방식

이 프로젝트는 MCP 서버보다 Skill을 먼저 중심에 둡니다.

- `skills/government-startup-support/SKILL.md`: 에이전트가 지원사업을 검색, 검증, 정규화, 요약하는 방법을 설명합니다.
- `skill-manifest.json`: 코딩 에이전트가 읽을 수 있는 설치용 매니페스트입니다.
- `scripts/install_skill.sh`: 스킬을 에이전트 홈 디렉터리에 설치합니다.
- `data/sources.yaml`: 전국 공식 소스 시드와 지역별 확장 후보를 관리합니다.
- `data/regions.yaml`: 전국, 시도, 서울 자치구 alias를 관리합니다.
- `data/keywords.yaml`: 공고 검색에 필요한 한국어 키워드를 관리합니다.
- `docs/`: 수집 정책, 첨부 공문 분석, 일정표, 뉴스레터 형식, MCP 확장 방향을 설명합니다.
- `calendar-view/`: 정규화된 수집 일정을 보여주는 정적 캘린더 UI입니다.

반복 수집, 변경 감지, DB 저장, 자동 발송이 필요해지면 그때 MCP 서버를 추가합니다.

## 첨부 공문과 사업계획서 분석

공고에 첨부 공문이 있으면 에이전트는 웹페이지 요약만 보지 않고 첨부파일을 우선 확인합니다. 파일 타입 우선순위는 `pdf > hwpx > word`입니다. 다운로드한 공문과 사용자의 사업계획서는 로컬에만 두고 Git에 커밋하지 않습니다.

## 빠른 검증

```bash
python3 scripts/validate_sources.py
python3 scripts/validate_skill_package.py
```

## 스킬로 설치하기

홈 디렉터리 기반 스킬을 지원하는 에이전트에서는 다음처럼 설치할 수 있습니다.

```bash
git clone https://github.com/Malko-potatos/startup-support-newsletter.git
cd startup-support-newsletter
bash scripts/install_skill.sh
```

설치 스크립트는 `skills/government-startup-support`, HWPX companion skill, 필수 Python 패키지 `gpt-researcher`와 `crawl4ai`를 함께 설치합니다. `crawl4ai-setup`까지 실행하며, 두 도구가 준비되지 않으면 발견형 리서치를 지원한다고 표시하지 않습니다.

설치 대상은 아래 위치입니다.

- `~/.agents/skills/government-startup-support`
- `~/.codex/skills/government-startup-support`: `~/.codex/skills`가 이미 있을 때
- `~/.claude/skills/government-startup-support`: `~/.claude/skills`가 이미 있을 때

에이전트는 `skill-manifest.json`을 읽고 `skill_path`를 직접 복사해 설치할 수도 있습니다.

## 현재 상태

현재 범위는 전국입니다. 서울 소스는 고품질 지역 시드로 유지하고, 전국/지자체/공공기관 소스는 GPT Researcher와 Crawl4AI 기반 발견 모드로 확장합니다.

## skill-installer로 GitHub 경로 설치

GitHub 경로로 직접 설치할 때는 self-contained 스킬 디렉터리 경로를 사용합니다.

```text
https://github.com/Malko-potatos/startup-support-newsletter/tree/main/skills/government-startup-support
```

Codex 내부 옵션 기준으로는 다음 경로입니다.

```text
--repo Malko-potatos/startup-support-newsletter --path skills/government-startup-support
```

설치 후에는 Codex를 재시작해 스킬 인덱스를 다시 로드하세요.

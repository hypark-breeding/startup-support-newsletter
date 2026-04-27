# 정부 창업지원사업 뉴스레터

한국 정부와 공공기관의 창업지원사업 공고를 에이전트가 찾아보고, 지역별 브리핑이나 뉴스레터 형태로 정리할 수 있게 만든 스킬 프로젝트입니다.

초기 범위는 서울 권역입니다.

예상 질문은 이런 형태입니다.

- "서울 창업지원 정보 알려줘"
- "마포구 예비창업자가 신청할 수 있는 지원사업 모아줘"
- "이번 주 서울권 창업지원사업 뉴스레터 만들어줘"

## 접근 방식

이 프로젝트는 MCP 서버보다 Skill을 먼저 중심에 둡니다.

- `skills/government-startup-support/SKILL.md`: 에이전트가 지원사업을 검색, 검증, 정규화, 요약하는 방법을 설명합니다.
- `skill-manifest.json`: 코딩 에이전트가 읽을 수 있는 설치용 매니페스트입니다.
- `scripts/install_skill.sh`: 스킬을 에이전트 홈 디렉터리에 설치합니다.
- `data/sources.yaml`: 서울 권역 공식/준공식 사이트 목록입니다.
- `data/regions.yaml`: 서울 지역과 자치구 alias를 관리합니다.
- `data/keywords.yaml`: 공고 검색에 필요한 한국어 키워드를 관리합니다.
- `docs/`: 수집 정책, 뉴스레터 형식, MCP 확장 방향을 설명합니다.

반복 수집, 변경 감지, DB 저장, 자동 발송이 필요해지면 그때 MCP 서버를 추가합니다.

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

설치 스크립트는 `skills/government-startup-support`를 아래 위치에 복사합니다.

- `~/.agents/skills/government-startup-support`
- `~/.codex/skills/government-startup-support`: `~/.codex/skills`가 이미 있을 때
- `~/.claude/skills/government-startup-support`: `~/.claude/skills`가 이미 있을 때

에이전트는 `skill-manifest.json`을 읽고 `skill_path`를 직접 복사해 설치할 수도 있습니다.

## 현재 상태

초기 범위는 서울입니다. 첫 버전은 전국 단위의 넓은 수집보다, 공식 소스 품질과 유지보수성을 우선합니다.

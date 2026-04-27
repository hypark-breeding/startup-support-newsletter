const DEFAULT_EVENTS = [
  {
    type: "application_deadline",
    title: "Example Startup Program",
    date: "2026-02-02",
    time: "23:59",
    timezone: "Asia/Seoul",
    organization: "Example public agency",
    region: "seoul",
    districts: [],
    source_url: "https://example.go.kr/notice",
    apply_url: "https://example.go.kr/apply",
    status: "open",
    confidence: "high",
    notes: "Example event only."
  },
  {
    type: "briefing",
    title: "Example Program Briefing",
    date: "2026-02-10",
    time: "14:00",
    timezone: "Asia/Seoul",
    organization: "Example startup hub",
    region: "seoul",
    districts: ["마포구"],
    source_url: "https://example.go.kr/briefing",
    apply_url: "",
    status: "upcoming",
    confidence: "medium",
    notes: "Example event only."
  },
  {
    type: "application_open",
    title: "AI Startup Space Application",
    date: "2026-02-16",
    time: "",
    timezone: "Asia/Seoul",
    organization: "Seoul startup hub",
    region: "seoul",
    districts: ["서초구"],
    source_url: "https://example.go.kr/open",
    apply_url: "https://example.go.kr/apply",
    status: "upcoming",
    confidence: "high",
    notes: "Example event only."
  }
];

const TYPE_LABELS = {
  application_deadline: "마감",
  application_open: "접수 시작",
  briefing: "설명회",
  interview: "평가",
  result_announcement: "결과 발표",
  event: "행사"
};

const state = {
  events: DEFAULT_EVENTS,
  currentDate: new Date("2026-02-01T00:00:00+09:00"),
  typeFilter: "all"
};

const calendarGrid = document.querySelector("#calendarGrid");
const agendaList = document.querySelector("#agendaList");
const monthLabel = document.querySelector("#monthLabel");
const todayLabel = document.querySelector("#todayLabel");
const totalEvents = document.querySelector("#totalEvents");
const deadlineEvents = document.querySelector("#deadlineEvents");
const highConfidenceEvents = document.querySelector("#highConfidenceEvents");
const typeFilter = document.querySelector("#typeFilter");
const jsonInput = document.querySelector("#jsonInput");

function toDateKey(date) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

function parseDate(value) {
  return new Date(`${value}T00:00:00+09:00`);
}

function monthName(date) {
  return new Intl.DateTimeFormat("ko-KR", {
    year: "numeric",
    month: "long"
  }).format(date);
}

function filteredEvents() {
  return state.events
    .filter((event) => state.typeFilter === "all" || event.type === state.typeFilter)
    .filter((event) => event.date)
    .sort((a, b) => `${a.date} ${a.time || ""}`.localeCompare(`${b.date} ${b.time || ""}`));
}

function eventsByDate(events) {
  return events.reduce((map, event) => {
    map[event.date] = map[event.date] || [];
    map[event.date].push(event);
    return map;
  }, {});
}

function eventClass(event) {
  if (event.type === "application_deadline") return "deadline";
  if (event.type === "application_open") return "open";
  return "";
}

function renderSummary(events) {
  totalEvents.textContent = String(events.length);
  deadlineEvents.textContent = String(events.filter((event) => event.type === "application_deadline").length);
  highConfidenceEvents.textContent = String(events.filter((event) => event.confidence === "high").length);
}

function renderCalendar() {
  const events = filteredEvents();
  const grouped = eventsByDate(events);
  const year = state.currentDate.getFullYear();
  const month = state.currentDate.getMonth();
  const first = new Date(year, month, 1);
  const startOffset = (first.getDay() + 6) % 7;
  const start = new Date(year, month, 1 - startOffset);
  const todayKey = toDateKey(new Date());

  monthLabel.textContent = monthName(state.currentDate);
  todayLabel.textContent = todayKey;
  calendarGrid.innerHTML = "";

  for (let index = 0; index < 42; index += 1) {
    const date = new Date(start);
    date.setDate(start.getDate() + index);
    const key = toDateKey(date);
    const dayEvents = grouped[key] || [];
    const cell = document.createElement("article");
    cell.className = [
      "day-cell",
      date.getMonth() === month ? "" : "outside",
      key === todayKey ? "today" : ""
    ]
      .filter(Boolean)
      .join(" ");
    cell.style.animationDelay = `${Math.min(index * 12, 260)}ms`;

    const number = document.createElement("div");
    number.className = "day-number";
    number.innerHTML = `<span>${date.getDate()}</span><span>${dayEvents.length ? dayEvents.length : ""}</span>`;
    cell.appendChild(number);

    dayEvents.slice(0, 3).forEach((event) => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = `event-pill ${eventClass(event)}`;
      button.textContent = `${TYPE_LABELS[event.type] || "일정"} · ${event.title}`;
      button.addEventListener("click", () => {
        document.querySelector(`[data-event-id="${event.date}-${event.title}"]`)?.scrollIntoView({
          behavior: "smooth",
          block: "center"
        });
      });
      cell.appendChild(button);
    });

    if (dayEvents.length > 3) {
      const more = document.createElement("div");
      more.className = "more-count";
      more.textContent = `+${dayEvents.length - 3} more`;
      cell.appendChild(more);
    }

    calendarGrid.appendChild(cell);
  }

  renderSummary(events);
  renderAgenda(events);
}

function renderAgenda(events) {
  if (!events.length) {
    agendaList.innerHTML = '<div class="empty-state">선택한 조건에 맞는 일정이 없습니다.</div>';
    return;
  }

  agendaList.innerHTML = events
    .map((event) => {
      const type = TYPE_LABELS[event.type] || "일정";
      const tags = [
        `<span class="tag ${eventClass(event)}">${type}</span>`,
        `<span class="tag">${event.date}${event.time ? ` ${event.time}` : ""}</span>`,
        event.confidence ? `<span class="tag ${event.confidence === "high" ? "verified" : ""}">${event.confidence}</span>` : ""
      ].join("");
      const districts = event.districts?.length ? ` · ${event.districts.join(", ")}` : "";
      const url = event.source_url || event.apply_url;
      return `
        <article class="agenda-item" data-event-id="${event.date}-${event.title}">
          <div class="agenda-meta">${tags}</div>
          <strong>${event.title}</strong>
          <p>${event.organization || "기관 미상"}${districts}</p>
          ${event.notes ? `<p>${event.notes}</p>` : ""}
          ${url ? `<a href="${url}" target="_blank" rel="noreferrer">공식 링크</a>` : ""}
        </article>
      `;
    })
    .join("");
}

function moveMonth(delta) {
  state.currentDate = new Date(state.currentDate.getFullYear(), state.currentDate.getMonth() + delta, 1);
  renderCalendar();
}

function normalizeEvents(input) {
  if (Array.isArray(input)) return input;
  if (Array.isArray(input?.calendar_events)) return input.calendar_events;
  if (Array.isArray(input?.events)) return input.events;
  return [];
}

document.querySelector("#prevMonth").addEventListener("click", () => moveMonth(-1));
document.querySelector("#nextMonth").addEventListener("click", () => moveMonth(1));

typeFilter.addEventListener("change", (event) => {
  state.typeFilter = event.target.value;
  renderCalendar();
});

jsonInput.addEventListener("change", async (event) => {
  const file = event.target.files?.[0];
  if (!file) return;
  const text = await file.text();
  const events = normalizeEvents(JSON.parse(text));
  if (events.length) {
    state.events = events;
    state.currentDate = parseDate(events[0].date);
    renderCalendar();
  }
});

renderCalendar();

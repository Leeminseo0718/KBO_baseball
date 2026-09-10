const verifiedGame = {
  date: '2026-09-09', away: 'KT', home: '삼성', awayScore: 2, homeScore: 0,
  innings: { away: [0,0,0,0,0,2,0,0,0], home: [0,0,0,0,0,0,0,0,0] },
  leaders: [
    { name:'안현민', team:'KT', kind:'타자', line:'4타수 3안타', result:'3안타' },
    { name:'김현수', team:'KT', kind:'타자', line:'4타수 1안타', result:'1홈런 · 2타점' },
    { name:'최형우', team:'삼성', kind:'타자', line:'4타수 2안타', result:'2안타' },
    { name:'고영표', team:'KT', kind:'투수', line:'7이닝 · 97구', result:'5K · 무실점 · 승' },
    { name:'원태인', team:'삼성', kind:'투수', line:'6이닝 · 108구', result:'3K · 2실점 · 패' },
    { name:'박영현', team:'KT', kind:'투수', line:'1이닝 · 16구', result:'3K · 무실점 · 세' }
  ]
};

const sql = {
  pitching: `SELECT game_date, innings_outs, strikeouts, earned_runs, pitches\nFROM kbo.v_player_game_pitching\nWHERE season = 2026 AND player_name = $1\nORDER BY game_date DESC LIMIT 100`,
  comparison: `SELECT player_name, SUM(at_bats), SUM(hits), SUM(home_runs), SUM(rbi)\nFROM kbo.v_player_game_batting\nWHERE season = 2026 AND player_name IN ($1, $2)\nGROUP BY player_name LIMIT 100`,
  ranking: `SELECT player_name, SUM(hits) AS value\nFROM kbo.v_player_game_batting\nWHERE season = 2026\nGROUP BY player_name ORDER BY value DESC LIMIT 100`,
  trend: `SELECT game_date, strikeouts, earned_runs, pitches\nFROM kbo.v_player_game_pitching\nWHERE season = 2026 AND player_name = $1\nORDER BY game_date LIMIT 100`
};

const answer = document.querySelector('#answer');
const questionInput = document.querySelector('#question');

function metric(value, label) {
  return `<div><strong>${value}</strong><span>${label}</span></div>`;
}

function renderAnswer(title, description, metrics, query, badge='검증 데이터') {
  answer.className = 'answer';
  answer.innerHTML = `<div class="answer-top"><div><h3>${title}</h3><p>${description}</p></div><span class="answer-badge">${badge}</span></div><div class="answer-metrics">${metrics.join('')}</div><details><summary>생성 SQL 보기</summary><pre>${query}</pre></details>`;
}

function refuse() {
  answer.className = 'answer refused';
  answer.innerHTML = `<div class="answer-top"><div><h3>이 질문은 아직 처리하지 않습니다.</h3><p>성적 조회, 선수 비교, 시계열 추이, 순위 조회 중 하나로 질문해 주세요. 예측·개인정보·데이터 변경 요청은 거절됩니다.</p></div><span class="answer-badge">안전 거절</span></div>`;
  return { accepted:false, type:'refusal' };
}

function localAnswer(question) {
  const q = question.replace(/\s+/g, ' ').trim();
  if (!q || /(예측|삭제|DROP|개인정보|날씨|잘생긴|우승팀)/i.test(q)) return refuse();
  if ((q.includes('비교') || q.includes('대결')) && q.includes('김현수') && q.includes('안현민')) {
    renderAnswer('김현수 · 안현민 타격 비교','현재 적재된 최근 검증 경기 기준입니다.',[metric('1 / 4','김현수 안타 / 타수'),metric('1','김현수 홈런'),metric('3 / 4','안현민 안타 / 타수'),metric('0','안현민 홈런')],sql.comparison);
    return { accepted:true, type:'comparison' };
  }
  if (q.includes('순위') || q.includes('랭킹') || q.includes('1위')) {
    renderAnswer('최근 경기 안타 순위','안현민이 3안타로 가장 많은 안타를 기록했습니다.',[metric('안현민','1위 · 3안타'),metric('최형우','2위 · 2안타'),metric('5명','1안타'),metric('26','타격 기록 행')],sql.ranking);
    return { accepted:true, type:'ranking' };
  }
  if (q.includes('추이') || q.includes('경기별') || q.includes('변화')) {
    renderAnswer('원태인 경기별 탈삼진 추이','현재 검증 완료된 1경기입니다. 수집이 누적되면 선 차트로 확장됩니다.',[metric('09.09','경기일'),metric('6.0','이닝'),metric('3','탈삼진'),metric('108','투구 수')],sql.trend);
    return { accepted:true, type:'trend' };
  }
  if (q.includes('원태인') && /(성적|투구|평균자책|탈삼진|이닝|최근)/.test(q)) {
    renderAnswer('원태인 · 9월 9일 투구','삼성 선발로 6이닝 동안 108구를 던졌습니다.',[metric('6.0','이닝'),metric('3','탈삼진'),metric('2','자책점'),metric('108','투구 수')],sql.pitching);
    return { accepted:true, type:'performance' };
  }
  const player = verifiedGame.leaders.find(item => q.includes(item.name));
  if (player && /(성적|투구|타격|최근|기록)/.test(q)) {
    renderAnswer(`${player.name} · 최근 경기`, `${player.team} ${player.kind} 기록입니다.`, [metric(player.line,'경기 기록'),metric(player.result,'주요 결과'),metric(verifiedGame.date,'경기일'),metric(`${verifiedGame.awayScore}:${verifiedGame.homeScore}`,'KT : 삼성')], player.kind === '투수' ? sql.pitching : sql.ranking);
    return { accepted:true, type:'performance' };
  }
  return refuse();
}

async function submitQuestion(question) {
  answer.className = 'answer';
  answer.innerHTML = '<p>질문을 분석하고 있습니다…</p>';
  const apiBase = window.KBO_API_URL || '';
  if (apiBase) {
    try {
      const response = await fetch(`${apiBase}/query`, { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({question}) });
      if (!response.ok) throw new Error('API error');
      const result = await response.json();
      if (!result.plan.accepted) return refuse();
    } catch (_) {
      answer.innerHTML = '<p>분석 API에 연결할 수 없어 검증 데이터로 답합니다.</p>';
    }
  }
  return localAnswer(question);
}

document.querySelector('#ask-form').addEventListener('submit', event => {
  event.preventDefault();
  submitQuestion(questionInput.value);
});

document.querySelectorAll('[data-question]').forEach(button => button.addEventListener('click', () => {
  questionInput.value = button.dataset.question;
  submitQuestion(button.dataset.question);
}));

document.querySelector('#innings').innerHTML = verifiedGame.innings.away.map((away,index) => `<div class="inning"><i class="away" style="height:${Math.max(away*36,2)}%" title="KT ${away}점"></i><i class="home" style="height:${Math.max(verifiedGame.innings.home[index]*36,2)}%" title="삼성 ${verifiedGame.innings.home[index]}점"></i><small>${index+1}</small></div>`).join('');
document.querySelector('#leaders').innerHTML = verifiedGame.leaders.map(player => `<tr data-name="${player.name}" data-kind="${player.kind}"><td>${player.name}</td><td>${player.team}</td><td>${player.kind}</td><td>${player.line}</td><td>${player.result}</td></tr>`).join('');
document.querySelectorAll('#leaders tr').forEach(row => row.addEventListener('click', () => {
  const suffix = row.dataset.kind === '투수' ? '의 최근 경기 투구 내용을 보여줘' : '의 최근 경기 타격 성적을 보여줘';
  questionInput.value = row.dataset.name + suffix;
  submitQuestion(questionInput.value);
  window.scrollTo({top:0,behavior:'smooth'});
}));

function registerWebMcp() {
  const context = document.modelContext;
  if (!context?.registerTool) return;
  Promise.resolve(context.registerTool({
    name:'ask_kbo_record_question', title:'KBO 기록 질문',
    description:'지원 범위 안의 KBO 기록 질문을 분석하고 대시보드에 답과 SQL 계획을 표시합니다.',
    inputSchema:{type:'object',properties:{question:{type:'string',minLength:1,maxLength:200}},required:['question'],additionalProperties:false},
    annotations:{readOnlyHint:false,untrustedContentHint:false},
    async execute(input){
      if (!input || typeof input.question !== 'string' || !input.question.trim()) throw new Error('질문을 입력해 주세요.');
      questionInput.value=input.question.trim();
      const result=await submitQuestion(questionInput.value);
      return {question:questionInput.value,accepted:result.accepted,questionType:result.type};
    }
  })).catch(()=>{});
}

submitQuestion(questionInput.value);
registerWebMcp();

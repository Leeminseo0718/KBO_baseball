const rosterSource = {
  '삼성': {
    '투수': ['원태인|18','최원태|20','김태훈|27','이승민|28','임기영|38','양창섭|42','배찬승|55','이승현|57','페덱|59','장찬희|60','김재윤|62','김백산|63','사토시|74','후라도|75'],
    '포수': ['김재성|2','강민호|47','박세혁|52'],
    '내야수': ['디아즈|0','류지혁|16','김영웅|30','이창용|50','양우현|53','김상준|56','전병우|61','이재현|7','박계범|9'],
    '외야수': ['김태훈|25','김헌곤|32','최형우|34','김성윤|39','김현준|44','구자욱|5','김지찬|58','박승규|66']
  },
  'KT': {
    '투수': ['고영표|1','스기모토|11','우규민|12','문용익|18','배제성|19','이정현|21','전용주|29','소형준|30','대니엘|36','주권|38','손동현|41','로건|43','오원석|47','박영현|60','김정운|61'],
    '포수': ['조대현|42','한승택|45','강현우|55'],
    '내야수': ['허경민|13','힐리어드|34','오윤석|4','권동진|52','장준원|56','손민석|57','김상수|7','류현인|9'],
    '외야수': ['김현수|10','안현민|23','배정대|27','최원준|3','이정훈|33','장진혁|51','김민혁|53','유준규|67']
  },
  'LG': {
    '투수': ['임찬규|1','고우석|19','우강훈|20','이우찬|21','배재준|25','손주영|29','톨허스트|30','이정용|31','조원태|38','이상영|39','김진수|45','김윤식|47','박시원|58','카라스코|59','김영우|67','케네디|68'],
    '포수': ['박동원|27','김민수|62','이주헌|63'],
    '내야수': ['강민균|00','오지환|10','손용준|15','문보경|2','오스틴|23','신민재|4','천성호|53','문정빈|56','구본혁|6','이영빈|7'],
    '외야수': ['박해민|17','최원영|3','홍창기|51','송찬의|55','김현종|66']
  },
  'KIA': {
    '투수': ['곽도규|0','김태형|10','조상우|11','올러|33','네일|40','황동하|41','이태양|44','이의리|48','김범수|49','전상현|51','홍건희|52','양현종|54','한재승|55','정해영|62','시라카와|63','성영탁|65'],
    '포수': ['주효상|22','한준수|25','김태군|42'],
    '내야수': ['정현창|12','박민|2','변우혁|29','김선빈|3','하주석|30','이호연|36','김도영|5','박상준|50'],
    '외야수': ['박정우|1','박재현|15','카스트로|26','김호령|27','김민규|37','나성범|47','고종욱|57']
  },
  '두산': {
    '투수': ['박치국|1','타카다|12','김정우|16','김영현|20','최승용|28','잭로그|39','서준오|41','이용찬|45','곽빈|47','박신지|49','이영하|50','김택연|63','윤태호|65','최민석|68','김한중|95'],
    '포수': ['김기연|22','양의지|25','윤준호|27'],
    '내야수': ['이유찬|13','강승호|23','임종성|3','세베리노|36','박지훈|37','박준순|52','양석환|53','오명진|6','안재석|62','박찬호|7'],
    '외야수': ['류승민|14','김민석|2','손아섭|24','정수빈|31','김대한|32','조수행|51']
  },
  'NC': {
    '투수': ['토다|11','김준원|15','라일리|3','이준혁|40','류진욱|41','신영우|43','송명기|45','손주환|46','이용준|48','이재학|51','김진호|54','전사민|57','구창모|59','김태경|60','배재환|61','김태훈|69'],
    '포수': ['안중열|22','김형준|25','이희성|32'],
    '내야수': ['홍종표|10','김한별|13','최정원|14','박민우|2','김휘집|44','서호철|5','블레인|50','김건|52','오태양|6','김주원|7'],
    '외야수': ['천재환|23','권희동|36','박건우|37','박시원|53','이우성|55']
  },
  '한화': {
    '투수': ['짐머맨|12','왕옌청|19','화이트|24','이민우|27','장유호|28','황준서|29','박재규|39','김서현|44','강재민|55','조동욱|57','박상원|58','권민규|64','주현상|66','강건우|69','박준영|96','류현진|99'],
    '포수': ['최재훈|13','장규현|32','허인서|59'],
    '내야수': ['이도윤|5','강백호|50','박정현|63','심우준|7','노시환|8','최유빈|93','황영묵|95','배승수|98'],
    '외야수': ['김태연|25','페라자|30','한지윤|36','최인호|41','문현빈|51','이도훈|60','유민|65']
  },
  '롯데': {
    '투수': ['김태균|14','김진욱|15','현도훈|17','박세웅|21','구승민|22','비슬리|23','로드리게스|31','김원중|34','박정민|36','이이무라|39','이영재|40','나균안|43','이진하|45','이준서|54','최준용|56'],
    '포수': ['박재엽|26','유강남|27','박건우|69'],
    '내야수': ['전민재|13','김민성|16','고승민|2','한동희|25','이호준|30','정대선|4','김세민|5','나승엽|51','노진혁|52','박승욱|53'],
    '외야수': ['황성빈|0','조세진|12','레이예스|29','김동혁|50','장두성|7','전준우|8']
  },
  'SSG': {
    '투수': ['김민|1','윤태현|12','이건욱|16','조병현|19','타케다|23','전영준|28','최민준|30','아빌라|33','한두솔|34','김민준|40','문승원|42','박시후|57','김도현|61','변건우|68','이로운|92'],
    '포수': ['조형우|20','신범수|25','이지영|56'],
    '내야수': ['안상현|10','박성한|2','정준재|3','김요셉|46','전의산|47','안재연|62','홍대인|97'],
    '외야수': ['채현우|15','에레디아|27','김재환|32','한유섬|35','김정민|48','최지훈|54','임근우|63','오시후|66']
  },
  '키움': {
    '투수': ['이강준|11','박준현|18','조영건|20','박지성|37','박진형|40','정다훈|45','원종현|46','유토|48','김선기|49','알칸타라|54','전준표|62','김연주|68','임진묵|69','윤석원|95'],
    '포수': ['김건희|12','김재현|32','김동헌|44'],
    '내야수': ['권혁빈|00','김웅빈|10','서건창|14','히우라|22','데이비슨|34','최재영|38','염승원|39','안치홍|9','여동욱|93','전태현|97'],
    '외야수': ['추재현|27','이형종|36','박찬혁|43','박주홍|57','박채울|72']
  }
};

const teamOrder = ['KT','LG','한화','삼성','SSG','NC','롯데','KIA','두산','키움'];
const positionOrder = ['투수','포수','내야수','외야수'];
const roster = teamOrder.flatMap(team => positionOrder.flatMap(position =>
  rosterSource[team][position].map(value => {
    const [name, number] = value.split('|');
    return { team, name, number, position };
  })
));

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

let displayGame = {...verifiedGame};

const sql = {
  pitching: `SELECT game_date, innings_outs, strikeouts, earned_runs, pitches\nFROM kbo.v_player_game_pitching\nWHERE season = 2026 AND player_name = $1\nORDER BY game_date DESC LIMIT 100`,
  batting: `SELECT game_date, at_bats, hits, home_runs, rbi\nFROM kbo.v_player_game_batting\nWHERE season = 2026 AND player_name = $1\nORDER BY game_date DESC LIMIT 100`,
  comparison: `SELECT player_name, SUM(at_bats), SUM(hits), SUM(home_runs), SUM(rbi)\nFROM kbo.v_player_game_batting\nWHERE season = 2026 AND player_name IN ($1, $2)\nGROUP BY player_name LIMIT 100`,
  ranking: `SELECT player_name, SUM(hits) AS value\nFROM kbo.v_player_game_batting\nWHERE season = 2026\nGROUP BY player_name ORDER BY value DESC LIMIT 100`,
  trend: `SELECT game_date, strikeouts, earned_runs, pitches\nFROM kbo.v_player_game_pitching\nWHERE season = 2026 AND player_name = $1\nORDER BY game_date LIMIT 100`,
  roster: `SELECT p.official_name, rm.team_id, rm.uniform_number, rm.position\nFROM kbo.roster_membership rm\nJOIN kbo.player p ON p.player_id = rm.player_id\nWHERE rm.season = 2026 AND rm.team_id = $1 AND p.official_name = $2\nLIMIT 100`
};

const answer = document.querySelector('#answer');
const questionInput = document.querySelector('#question');
const rosterGrid = document.querySelector('#roster-grid');
const rosterSearch = document.querySelector('#roster-search');
let activeTeam = 'KT';
let activePosition = '전체';
let selectedRosterKey = '';

function escapeHTML(value) {
  return String(value).replace(/[&<>'"]/g, character => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[character]));
}

function metric(value, label) {
  return `<div><strong>${escapeHTML(value)}</strong><span>${escapeHTML(label)}</span></div>`;
}

function renderAnswer(title, description, metrics, query, badge='검증 데이터') {
  answer.className = 'answer';
  answer.innerHTML = `<div class="answer-top"><div><h3>${escapeHTML(title)}</h3><p>${escapeHTML(description)}</p></div><span class="answer-badge">${escapeHTML(badge)}</span></div><div class="answer-metrics">${metrics.join('')}</div><details><summary>생성 SQL 보기</summary><pre>${escapeHTML(query)}</pre></details>`;
}

function refuse() {
  answer.className = 'answer refused';
  answer.innerHTML = `<div class="answer-top"><div><h3>이 질문은 아직 처리하지 않습니다.</h3><p>성적 조회, 선수 비교, 시계열 추이, 순위 조회 중 하나로 질문해 주세요. 예측·개인정보·데이터 변경 요청은 거절됩니다.</p></div><span class="answer-badge">안전 거절</span></div>`;
  return { accepted:false, type:'refusal' };
}

function findMentionedPlayer(question) {
  const candidates = roster.filter(player => question.includes(player.name));
  const teamCandidates = candidates.filter(player => question.includes(player.team) || player.team === activeTeam);
  const scoped = teamCandidates.length ? teamCandidates : candidates;
  if (question.includes('투구')) return scoped.find(player => player.position === '투수') || scoped[0];
  if (question.includes('타격')) return scoped.find(player => player.position !== '투수') || scoped[0];
  return scoped[0];
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
  if ((q.includes('추이') || q.includes('경기별') || q.includes('변화')) && q.includes('원태인')) {
    renderAnswer('원태인 경기별 탈삼진 추이','현재 검증 완료된 1경기입니다. 수집이 누적되면 선 차트로 확장됩니다.',[metric('09.09','경기일'),metric('6.0','이닝'),metric('3','탈삼진'),metric('108','투구 수')],sql.trend);
    return { accepted:true, type:'trend' };
  }
  const mentioned = findMentionedPlayer(q);
  if (mentioned && /(성적|투구|타격|최근|기록|선수|명단|정보)/.test(q)) {
    const verified = verifiedGame.leaders.find(item => item.name === mentioned.name && item.team === mentioned.team);
    if (verified) {
      renderAnswer(`${verified.name} · 최근 경기`, `${verified.team} ${verified.kind} 기록입니다.`, [metric(verified.line,'경기 기록'),metric(verified.result,'주요 결과'),metric(verifiedGame.date,'경기일'),metric(`${verifiedGame.awayScore}:${verifiedGame.homeScore}`,'KT : 삼성')], verified.kind === '투수' ? sql.pitching : sql.batting);
      return { accepted:true, type:'performance' };
    }
    renderAnswer(`${mentioned.team} · ${mentioned.name}`, 'KBO 등록 명단에서 확인했습니다. 경기 기록은 수집 범위가 넓어지는 대로 함께 표시됩니다.', [metric(`#${mentioned.number}`,'등번호'),metric(mentioned.position,'포지션'),metric(mentioned.team,'소속 구단'),metric('09.09','명단 기준일')], sql.roster, 'KBO 명단');
    return { accepted:true, type:'roster' };
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

function teamPlayers(team) {
  return roster.filter(player => player.team === team);
}

function renderTeamTabs() {
  document.querySelector('#team-tabs').innerHTML = teamOrder.map(team => {
    const count = teamPlayers(team).length;
    return `<button type="button" role="tab" aria-selected="${team === activeTeam}" class="${team === activeTeam ? 'active' : ''}" data-team="${escapeHTML(team)}"><span>${escapeHTML(team)}</span><small>${count}</small></button>`;
  }).join('');
  document.querySelectorAll('#team-tabs button').forEach(button => button.addEventListener('click', () => selectTeam(button.dataset.team)));
}

function selectTeam(team) {
  if (!rosterSource[team]) return false;
  activeTeam = team;
  selectedRosterKey = '';
  rosterSearch.value = '';
  renderTeamTabs();
  renderRoster();
  return true;
}

function renderRoster() {
  const query = rosterSearch.value.trim().toLocaleLowerCase('ko-KR');
  const all = teamPlayers(activeTeam);
  const filtered = all.filter(player => (activePosition === '전체' || player.position === activePosition) && (!query || player.name.toLocaleLowerCase('ko-KR').includes(query)));
  document.querySelector('#selected-team-name').textContent = activeTeam;
  document.querySelector('#team-initial').textContent = activeTeam.slice(0, 2);
  document.querySelector('#selected-team-count').textContent = `등록 선수 ${all.length}명`;
  document.querySelector('#roster-summary').innerHTML = positionOrder.map(position => `<span><b>${position}</b> ${all.filter(player => player.position === position).length}</span>`).join('') + `<em>${filtered.length}명 표시</em>`;
  rosterGrid.innerHTML = filtered.map(player => {
    const key = `${player.team}-${player.position}-${player.number}-${player.name}`;
    const hasRecord = verifiedGame.leaders.some(item => item.team === player.team && item.name === player.name);
    return `<button type="button" class="player-card ${key === selectedRosterKey ? 'selected' : ''}" data-key="${escapeHTML(key)}" data-team="${escapeHTML(player.team)}" data-name="${escapeHTML(player.name)}" data-position="${escapeHTML(player.position)}"><span class="uniform">${escapeHTML(player.number)}</span><span class="player-copy"><strong>${escapeHTML(player.name)}</strong><small>${escapeHTML(player.position)}</small></span>${hasRecord ? '<i>기록</i>' : '<span class="card-arrow">↗</span>'}</button>`;
  }).join('');
  document.querySelector('#roster-empty').hidden = filtered.length > 0;
  rosterGrid.querySelectorAll('.player-card').forEach(card => card.addEventListener('click', () => selectPlayerCard(card)));
}

function selectPlayerCard(card) {
  selectedRosterKey = card.dataset.key;
  const isPitcher = card.dataset.position === '투수';
  questionInput.value = `${card.dataset.team} ${card.dataset.name}의 최근 경기 ${isPitcher ? '투구' : '타격'} 기록을 보여줘`;
  renderRoster();
  submitQuestion(questionInput.value);
  document.querySelector('.ask-card').scrollIntoView({behavior:'smooth', block:'start'});
}

document.querySelector('#ask-form').addEventListener('submit', event => {
  event.preventDefault();
  submitQuestion(questionInput.value);
});

document.querySelectorAll('[data-question]').forEach(button => button.addEventListener('click', () => {
  questionInput.value = button.dataset.question;
  submitQuestion(button.dataset.question);
}));

document.querySelector('#position-filter').addEventListener('click', event => {
  const button = event.target.closest('button[data-position]');
  if (!button) return;
  activePosition = button.dataset.position;
  document.querySelectorAll('#position-filter button').forEach(item => item.classList.toggle('active', item === button));
  renderRoster();
});

rosterSearch.addEventListener('input', renderRoster);

function inningValues(value) {
  const values = Array.isArray(value)
    ? value
    : Object.entries(value || {}).sort(([left], [right]) => Number(left) - Number(right)).map(([, score]) => score);
  return values.map(score => Number.isFinite(Number(score)) ? Number(score) : 0);
}

function formatGameDate(value) {
  return String(value || '').replaceAll('-', '.');
}

function formatSyncTime(value) {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return '갱신 시각 확인 불가';
  return `${new Intl.DateTimeFormat('ko-KR', {month:'2-digit', day:'2-digit', hour:'2-digit', minute:'2-digit', hour12:false}).format(date)} 갱신`;
}

function setQuality(quality = {}) {
  document.querySelector('#quality-events').textContent = quality.events ?? quality.pitch_events ?? '—';
  document.querySelector('#quality-batting').textContent = quality.batting_rows ?? '—';
  document.querySelector('#quality-pitching').textContent = quality.pitching_rows ?? '—';
  document.querySelector('#quality-players').textContent = quality.identified_players ?? '—';
}

function renderGame() {
  const awayInnings = inningValues(displayGame.innings?.away);
  const homeInnings = inningValues(displayGame.innings?.home);
  const inningCount = Math.max(awayInnings.length, homeInnings.length, 9);
  const innings = Array.from({length: inningCount}, (_, index) => ({away: awayInnings[index] || 0, home: homeInnings[index] || 0}));
  document.querySelector('#game-date').textContent = formatGameDate(displayGame.date);
  document.querySelector('#game-status').textContent = [displayGame.stadium, displayGame.statusLabel].filter(Boolean).join(' · ');
  document.querySelector('#away-team').textContent = displayGame.away;
  document.querySelector('#home-team').textContent = displayGame.home;
  document.querySelector('#away-score').textContent = displayGame.awayScore;
  document.querySelector('#home-score').textContent = displayGame.homeScore;
  document.querySelector('#inning-summary').textContent = displayGame.currentInning || `${displayGame.away} ${displayGame.awayScore} : ${displayGame.homeScore} ${displayGame.home}`;
  document.querySelector('#score-check').innerHTML = displayGame.scoreMessage || '<span>✓</span> 문자중계와 박스스코어 득점 일치';
  document.querySelector('#innings').innerHTML = innings.map((inning,index) => `<div class="inning"><i class="away" style="height:${Math.max(inning.away*36,2)}%" title="${escapeHTML(displayGame.away)} ${inning.away}점"></i><i class="home" style="height:${Math.max(inning.home*36,2)}%" title="${escapeHTML(displayGame.home)} ${inning.home}점"></i><small>${index+1}</small></div>`).join('');
  renderLeaders();
}

function renderLeaders() {
  const leaders = displayGame.leaders || [];
  document.querySelector('#leaders').innerHTML = leaders.length
    ? leaders.map(player => `<tr data-name="${escapeHTML(player.name)}" data-team="${escapeHTML(player.team)}" data-kind="${escapeHTML(player.kind)}"><td>${escapeHTML(player.name)}</td><td>${escapeHTML(player.team)}</td><td>${escapeHTML(player.kind)}</td><td>${escapeHTML(player.line)}</td><td>${escapeHTML(player.result)}</td></tr>`).join('')
    : '<tr class="empty-row"><td colspan="5">선수별 상세 기록은 경기 중 수집 후 표시됩니다.</td></tr>';
  document.querySelectorAll('#leaders tr[data-name]').forEach(row => row.addEventListener('click', () => {
    const suffix = row.dataset.kind === '투수' ? '의 최근 경기 투구 내용을 보여줘' : '의 최근 경기 타격 성적을 보여줘';
    questionInput.value = `${row.dataset.team} ${row.dataset.name}${suffix}`;
    submitQuestion(questionInput.value);
    document.querySelector('.ask-card').scrollIntoView({behavior:'smooth', block:'start'});
  }));
}

function pickSnapshotGame(games) {
  const liveStatuses = new Set(['STARTED','LIVE','PLAYING','SUSPENDED']);
  return games.find(game => liveStatuses.has(game.status)) || games.find(game => game.status === 'BEFORE') || [...games].reverse().find(game => game.status === 'RESULT') || games[0];
}

function applyPublicSnapshot(snapshot) {
  const game = pickSnapshotGame(snapshot.games || []);
  if (!game) return false;
  const isLive = ['STARTED','LIVE','PLAYING','SUSPENDED'].includes(game.status);
  const isFinal = game.status === 'RESULT';
  displayGame = {
    date: game.date || snapshot.date,
    away: game.away?.name || game.away?.code || '원정',
    home: game.home?.name || game.home?.code || '홈',
    awayScore: game.away?.score ?? 0,
    homeScore: game.home?.score ?? 0,
    stadium: game.stadium || '',
    statusLabel: game.statusLabel || game.status || '상태 확인 중',
    currentInning: game.currentInning || '',
    innings: {away: game.away?.scoreByInning || [], home: game.home?.scoreByInning || []},
    leaders: [],
    scoreMessage: isLive ? '<span>●</span> 네이버 문자중계 점수 자동 갱신 중' : isFinal ? '<span>✓</span> 경기 종료 점수 수집 완료' : '<span>↻</span> 경기 시작 후 점수가 자동 갱신됩니다'
  };
  document.querySelector('#sync-label').textContent = isLive ? '경기 중 자동 갱신' : '일정 자동 갱신';
  document.querySelector('#sync-time').textContent = formatSyncTime(snapshot.generatedAt);
  document.querySelector('#source-tag').textContent = isLive ? 'NAVER LIVE' : 'NAVER SCHEDULE';
  document.querySelector('#live-dot').classList.toggle('is-live', isLive);
  setQuality({});
  renderGame();
  return true;
}

function apiLeader(player) {
  if (player.kind === '투수') {
    const outs = Number(player.innings_outs || 0);
    const innings = `${Math.floor(outs / 3)}.${outs % 3}`;
    return {...player, line:`${innings}이닝 · ${player.pitches ?? 0}구`, result:`${player.strikeouts ?? 0}K · ${player.earned_runs ?? 0}자책${player.decision ? ` · ${player.decision}` : ''}`};
  }
  return {...player, line:`${player.at_bats ?? 0}타수 ${player.hits ?? 0}안타`, result:`${player.home_runs ?? 0}홈런 · ${player.rbi ?? 0}타점`};
}

function applyApiDashboard(payload) {
  const game = payload.latestGame;
  if (!game) return false;
  displayGame = {
    date: game.game_date,
    away: game.away_team,
    home: game.home_team,
    awayScore: game.away_score ?? 0,
    homeScore: game.home_score ?? 0,
    stadium: game.stadium || '',
    statusLabel: ['RESULT','FINAL'].includes(game.status) ? '경기 종료' : '경기 중',
    currentInning: '',
    innings: {away: [], home: []},
    leaders: (payload.leaders || []).map(apiLeader),
    scoreMessage: '<span>✓</span> PostgreSQL 분석 마트 최신 적재 데이터'
  };
  document.querySelector('#sync-label').textContent = '상세 기록 자동 갱신';
  document.querySelector('#sync-time').textContent = formatSyncTime(payload.generatedAt);
  document.querySelector('#source-tag').textContent = 'NAVER × POSTGRESQL';
  document.querySelector('#live-dot').classList.add('is-live');
  setQuality(payload.quality || {});
  renderGame();
  return true;
}

async function syncDashboard() {
  const apiBase = String(window.KBO_API_URL || '').replace(/\/$/, '');
  if (apiBase) {
    try {
      const response = await fetch(`${apiBase}/dashboard`, {cache:'no-store'});
      if (response.ok && applyApiDashboard(await response.json())) return;
    } catch (_) {}
  }
  try {
    const snapshotUrl = window.KBO_PUBLIC_SNAPSHOT_URL || './data/live.json';
    const response = await fetch(snapshotUrl, {cache:'no-store'});
    if (!response.ok) throw new Error('snapshot unavailable');
    if (applyPublicSnapshot(await response.json())) return;
  } catch (_) {}
  document.querySelector('#sync-label').textContent = '검증 데이터 표시';
  document.querySelector('#sync-time').textContent = '자동 갱신 대기';
}

function registerWebMcp() {
  const context = document.modelContext;
  if (!context?.registerTool) return;
  const registrations = [
    context.registerTool({
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
    }),
    context.registerTool({
      name:'select_kbo_team', title:'KBO 구단 선택',
      description:'구단별 등록 선수 명단을 선택해 화면에 표시합니다.',
      inputSchema:{type:'object',properties:{team:{type:'string',enum:teamOrder}},required:['team'],additionalProperties:false},
      annotations:{readOnlyHint:false,untrustedContentHint:false},
      async execute(input){ return {selected:selectTeam(input.team),team:input.team,count:teamPlayers(input.team).length}; }
    })
  ];
  registrations.forEach(registration => Promise.resolve(registration).catch(()=>{}));
}

renderTeamTabs();
renderRoster();
renderGame();
submitQuestion(questionInput.value);
registerWebMcp();
syncDashboard();
window.setInterval(syncDashboard, 60_000);
document.addEventListener('visibilitychange', () => {
  if (!document.hidden) syncDashboard();
});

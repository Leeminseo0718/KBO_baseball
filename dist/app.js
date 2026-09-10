const teams = [
  { id: 'foxes', name: '서울 레드폭스', rank: 2, wins: 68, draws: 4, losses: 51, rate: .571, avg: .282, era: 3.71, hr: 119, ops: .781, form: [[6,3],[2,5],[7,2],[4,1],[3,4],[8,6],[5,2],[1,3],[6,4],[4,2]] },
  { id: 'waves', name: '부산 블루웨이브', rank: 1, wins: 72, draws: 3, losses: 47, rate: .605, avg: .276, era: 3.42, hr: 126, ops: .774, form: [[5,2],[4,3],[2,1],[7,4],[1,2],[6,3],[8,2],[3,5],[4,0],[6,2]] },
  { id: 'bears', name: '대전 문베어스', rank: 4, wins: 62, draws: 5, losses: 58, rate: .517, avg: .267, era: 4.08, hr: 101, ops: .738, form: [[3,6],[5,2],[2,4],[7,5],[4,3],[2,1],[3,7],[6,5],[1,2],[5,4]] },
  { id: 'stars', name: '광주 골든스타즈', rank: 7, wins: 54, draws: 4, losses: 66, rate: .450, avg: .259, era: 4.61, hr: 93, ops: .711, form: [[2,5],[1,4],[6,3],[3,7],[5,4],[2,6],[4,3],[1,2],[7,5],[3,6]] }
];

const players = [
  { team:'foxes', name:'김도윤', number:7, role:'타자', position:'유격수', hand:'우투좌타', a:.318, b:18, c:.891, skills:[88,72,91,78,84], summary:[['.318','타율'],['18','홈런'],['27','도루']] },
  { team:'foxes', name:'박준혁', number:25, role:'타자', position:'1루수', hand:'좌투좌타', a:.291, b:31, c:.934, skills:[81,94,68,73,88], summary:[['.291','타율'],['31','홈런'],['.934','OPS']] },
  { team:'foxes', name:'이성우', number:41, role:'투수', position:'선발투수', hand:'우투우타', a:2.84, b:142, c:1.12, skills:[92,82,76,89,79], summary:[['2.84','ERA'],['142','탈삼진'],['1.12','WHIP']] },
  { team:'foxes', name:'최민석', number:19, role:'투수', position:'마무리', hand:'우투우타', a:1.97, b:34, c:.96, skills:[88,95,71,84,91], summary:[['1.97','ERA'],['34','세이브'],['0.96','WHIP']] },
  { team:'waves', name:'한유진', number:33, role:'타자', position:'중견수', hand:'우투좌타', a:.326, b:14, c:.876, skills:[91,69,94,86,83], summary:[['.326','타율'],['14','홈런'],['38','도루']] },
  { team:'waves', name:'오지훈', number:11, role:'투수', position:'선발투수', hand:'좌투좌타', a:2.51, b:167, c:1.04, skills:[94,89,81,91,86], summary:[['2.51','ERA'],['167','탈삼진'],['1.04','WHIP']] },
  { team:'bears', name:'정태현', number:52, role:'타자', position:'포수', hand:'우투우타', a:.278, b:22, c:.819, skills:[75,84,62,93,81], summary:[['.278','타율'],['22','홈런'],['.819','OPS']] },
  { team:'bears', name:'문재호', number:16, role:'투수', position:'불펜투수', hand:'우투우타', a:3.08, b:71, c:1.18, skills:[83,86,73,78,87], summary:[['3.08','ERA'],['71','탈삼진'],['1.18','WHIP']] },
  { team:'stars', name:'윤하람', number:3, role:'타자', position:'3루수', hand:'우투우타', a:.304, b:25, c:.874, skills:[84,88,70,77,85], summary:[['.304','타율'],['25','홈런'],['.874','OPS']] },
  { team:'stars', name:'서강민', number:28, role:'투수', position:'선발투수', hand:'좌투좌타', a:3.76, b:128, c:1.29, skills:[79,84,76,82,74], summary:[['3.76','ERA'],['128','탈삼진'],['1.29','WHIP']] }
];

let currentPosition = '전체';
let selectedPlayer = players[0];

const teamSelect = document.querySelector('#team');
teams.forEach(team => teamSelect.add(new Option(team.name, team.id)));

function render(team) {
  document.querySelector('#team-name').textContent = team.name;
  document.querySelector('#team-record').textContent = `${team.wins}승 ${team.draws}무 ${team.losses}패`;
  document.querySelector('#team-rank').textContent = team.rank;
  document.querySelector('#win-rate').textContent = team.rate.toFixed(3).replace(/^0/, '');
  const ring = document.querySelector('#win-ring');
  ring.style.background = `conic-gradient(var(--orange) 0 ${team.rate * 100}%, #1d2b40 ${team.rate * 100}%)`;
  ring.setAttribute('aria-label', `승률 ${team.rate.toFixed(3)}`);

  const metrics = [
    ['팀 타율', team.avg.toFixed(3).replace(/^0/, ''), '리그 2위'],
    ['팀 평균자책', team.era.toFixed(2), '리그 3위'],
    ['홈런', `${team.hr}`, '리그 1위'],
    ['OPS', team.ops.toFixed(3).replace(/^0/, ''), '리그 2위']
  ];
  document.querySelector('#metrics').innerHTML = metrics.map(([label, value, rank]) =>
    `<article class="metric"><span class="metric-label">${label}</span><strong class="metric-value">${value}</strong><span class="metric-rank">${rank}</span></article>`
  ).join('');
  document.querySelector('#form-chart').innerHTML = team.form.map(([score, allow], index) =>
    `<div class="game-bars" title="${index + 1}경기 전: ${score}득점 ${allow}실점"><i class="bar score" style="height:${score * 11}%"></i><i class="bar allow" style="height:${allow * 11}%"></i><small>${10-index}</small></div>`
  ).join('');
  renderPlayers();
}

function formatValue(value) {
  return value < 1 ? value.toFixed(3).replace(/^0/, '') : Number.isInteger(value) ? String(value) : value.toFixed(2);
}

function renderPlayers() {
  const query = document.querySelector('#player-search').value.trim().toLowerCase();
  const list = players.filter(player =>
    player.team === teamSelect.value &&
    (currentPosition === '전체' || player.role === currentPosition) &&
    (!query || `${player.name} ${player.position}`.toLowerCase().includes(query))
  );
  document.querySelector('#player-count').textContent = list.length;
  document.querySelector('#empty-state').hidden = list.length > 0;
  document.querySelector('.table-scroll').hidden = list.length === 0;
  const mixed = currentPosition === '전체';
  document.querySelector('#stat-a-head').textContent = mixed ? '핵심 1' : currentPosition === '타자' ? '타율' : 'ERA';
  document.querySelector('#stat-b-head').textContent = mixed ? '핵심 2' : currentPosition === '타자' ? '홈런' : '탈삼진';
  document.querySelector('#stat-c-head').textContent = mixed ? '핵심 3' : currentPosition === '타자' ? 'OPS' : 'WHIP';
  document.querySelector('#player-rows').innerHTML = list.map(player => `
    <tr tabindex="0" data-player="${player.name}" class="${selectedPlayer.name === player.name ? 'selected' : ''}">
      <td>${player.name}</td><td>${player.position}</td><td>${formatValue(player.a)}</td><td>${formatValue(player.b)}</td><td>${formatValue(player.c)}</td>
    </tr>`).join('');
  document.querySelectorAll('[data-player]').forEach(row => {
    const choose = () => { selectedPlayer = players.find(player => player.name === row.dataset.player); renderPlayers(); renderPlayerDetail(); };
    row.addEventListener('click', choose);
    row.addEventListener('keydown', event => { if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); choose(); } });
  });
  if (list.length && !list.some(player => player.name === selectedPlayer.name)) {
    selectedPlayer = list[0];
    renderPlayerDetail();
  }
}

function radarPoints(values, radius, cx=130, cy=108) {
  return values.map((value, index) => {
    const angle = -Math.PI / 2 + index * Math.PI * 2 / values.length;
    const r = radius * value / 100;
    return `${cx + Math.cos(angle) * r},${cy + Math.sin(angle) * r}`;
  }).join(' ');
}

function renderPlayerDetail() {
  const player = selectedPlayer;
  document.querySelector('#player-number').textContent = `#${player.number}`;
  document.querySelector('#player-initial').textContent = player.name[0];
  document.querySelector('#player-name').textContent = player.name;
  document.querySelector('#player-meta').textContent = `${player.position} · ${player.hand}`;
  const axes = ['정확도','파워','주루','수비','기여도'];
  const grid = [25,50,75,100].map(level => `<polygon points="${radarPoints(Array(5).fill(level), 82)}" fill="none" stroke="#25354a" stroke-width="1"/>`).join('');
  const labels = axes.map((label,index) => {
    const angle = -Math.PI/2 + index*Math.PI*2/5;
    return `<text x="${130+Math.cos(angle)*104}" y="${112+Math.sin(angle)*99}" text-anchor="middle" fill="#8291a6" font-size="10">${label}</text>`;
  }).join('');
  const dots = player.skills.map((value,index) => {
    const angle = -Math.PI/2 + index*Math.PI*2/5;
    return `<circle cx="${130+Math.cos(angle)*82*value/100}" cy="${108+Math.sin(angle)*82*value/100}" r="3" fill="#ff9f43"/>`;
  }).join('');
  document.querySelector('#radar').innerHTML = `${grid}<polygon points="${radarPoints(player.skills,82)}" fill="rgba(119,231,255,.18)" stroke="#77e7ff" stroke-width="2"/>${dots}${labels}`;
  document.querySelector('#player-summary').innerHTML = player.summary.map(([value,label]) => `<div class="summary-stat"><strong>${value}</strong><span>${label}</span></div>`).join('');
}

document.querySelector('#filter-form').addEventListener('submit', event => {
  event.preventDefault();
  render(teams.find(team => team.id === teamSelect.value));
});
teamSelect.addEventListener('change', () => render(teams.find(team => team.id === teamSelect.value)));
document.querySelector('#player-search').addEventListener('input', renderPlayers);
document.querySelectorAll('[data-position]').forEach(button => button.addEventListener('click', () => {
  currentPosition = button.dataset.position;
  document.querySelectorAll('[data-position]').forEach(item => item.classList.toggle('active', item === button));
  renderPlayers();
}));

function registerWebMcp() {
  const context = document.modelContext;
  if (!context?.registerTool) return;
  const teamIds = teams.map(team => team.id);
  Promise.resolve(context.registerTool({
    name: 'select_baseball_team',
    title: '야구 팀 선택',
    description: '대시보드에서 분석할 팀을 선택하고 화면의 기록과 선수 목록을 갱신합니다.',
    inputSchema: { type: 'object', properties: { teamId: { type: 'string', enum: teamIds } }, required: ['teamId'], additionalProperties: false },
    annotations: { readOnlyHint: false, untrustedContentHint: false },
    execute(input) {
      if (!input || !teamIds.includes(input.teamId)) throw new Error('지원하지 않는 팀 ID입니다.');
      teamSelect.value = input.teamId;
      const team = teams.find(item => item.id === input.teamId);
      render(team);
      return { teamId: team.id, teamName: team.name, playerCount: players.filter(player => player.team === team.id).length };
    }
  })).catch(() => {});
}

render(teams[0]);
renderPlayerDetail();
registerWebMcp();

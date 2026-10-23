const SCORE_KEY = 'quiz_scores';
const { escapeHtml, filterLevels, renderLevelCards, createQuizSession } = typeof module !== 'undefined'
  ? require('./quiz-page-logic')
  : globalThis.quizPageLogic;

function getScores() {
  try {
    return JSON.parse(localStorage.getItem(SCORE_KEY) || '{}');
  } catch (error) {
    return {};
  }
}

function saveScore(levelPath, score, max) {
  const scores = getScores();
  const previous = scores[levelPath];
  if (!previous || score > previous.best) {
    scores[levelPath] = { best: score, max, date: new Date().toISOString() };
    localStorage.setItem(SCORE_KEY, JSON.stringify(scores));
  }
  return scores[levelPath] || previous;
}

function setText(id, value) {
  const element = document.getElementById(id);
  if (element) element.textContent = value;
}

function show(element, visible) {
  if (element) element.classList.toggle('hidden', !visible);
}

function formatPoints(points) {
  const value = Number(points || 0);
  if (value === 1) return '1 bod';
  if (value >= 2 && value <= 4) return `${value} body`;
  return `${value} bodů`;
}

async function fetchJson(url) {
  const response = await fetch(url);
  if (!response.ok) throw new Error(`Request failed: ${response.status}`);
  return response.json();
}

function levelUrl(levelPath) {
  const cleanPath = String(levelPath || '');
  const segments = cleanPath.split('/');

  if (
    !cleanPath.endsWith('.json')
    || cleanPath.startsWith('/')
    || /^[a-z][a-z0-9+.-]*:/i.test(cleanPath)
    || cleanPath.includes('\\')
    || segments.includes('..')
  ) {
    throw new Error('Neplatná cesta k levelu.');
  }

  return `levels/${segments.map(encodeURIComponent).join('/')}`;
}

function initLevelsPage() {
  const grid = document.getElementById('levels-grid');
  const empty = document.getElementById('empty-state');
  const count = document.getElementById('level-count');
  const scores = getScores();
  const filters = Array.from(document.querySelectorAll('[data-difficulty-filter]'));
  let allLevels = [];
  let activeDifficulty = 'all';
  const renderLevels = () => renderLevelsView({ grid, empty, count, allLevels, activeDifficulty, scores });

  filters.forEach((button) => {
    button.addEventListener('click', () => {
      activeDifficulty = button.dataset.difficultyFilter || 'all';
      filters.forEach((filter) => filter.classList.toggle('active', filter === button));
      renderLevels();
    });
  });

  fetchJson('levels/index.json')
    .then((levels) => {
      allLevels = levels;
      renderLevels();
    })
    .catch((error) => {
      count.textContent = 'Offline';
      grid.innerHTML = `<section class="panel state-panel">Nepodařilo se načíst levely: ${escapeHtml(error.message)}</section>`;
    });
}

function renderLevelsView({ grid, empty, count, allLevels, activeDifficulty, scores }) {
  const levels = filterLevels(allLevels, activeDifficulty);
  count.textContent = activeDifficulty === 'all'
    ? `${allLevels.length} level${allLevels.length === 1 ? '' : 's'}`
    : `${levels.length}/${allLevels.length} level${levels.length === 1 ? '' : 's'}`;
  show(empty, levels.length === 0);
  grid.innerHTML = renderLevelCards(levels, scores);
}

function sameSelection(selected, correct) {
  if (selected.length !== correct.length) return false;
  const selectedSet = new Set(selected);
  return correct.every((index) => selectedSet.has(index));
}

function initQuizPage() {
  const params = new URLSearchParams(window.location.search);
  const levelPath = params.get('level');
  const loading = document.getElementById('quiz-loading');
  const errorBox = document.getElementById('quiz-error');
  const quizScreen = document.getElementById('quiz-screen');
  const resultsScreen = document.getElementById('results-screen');
  const form = document.getElementById('answers-form');
  const feedback = document.getElementById('feedback');
  const submitButton = document.getElementById('submit-answer');
  const nextButton = document.getElementById('next-question');
  if (!levelPath) return showQuizError(loading, errorBox, 'Chybí parametr level. Vrať se na výběr levelů.');
  let url;
  try { url = levelUrl(levelPath); } catch (error) { return showQuizError(loading, errorBox, error.message); }
  const page = { levelPath, loading, errorBox, quizScreen, resultsScreen, form, feedback, submitButton, nextButton };
  fetchJson(url).then((level) => startQuiz(page, level)).catch((error) => showQuizError(loading, errorBox, `Nepodařilo se načíst level: ${error.message}`));
}

function showQuizError(loading, errorBox, message) {
  show(loading, false); show(errorBox, true); errorBox.textContent = message; setText('quiz-status', 'Error');
}

function startQuiz(page, level) {
  if (!Array.isArray(level.questions) || level.questions.length === 0) return showQuizError(page.loading, page.errorBox, 'Level neobsahuje žádné otázky.');
  const session = createQuizSession({ levelPath: page.levelPath, questions: level.questions, saveScore });
  const context = { ...page, level, session };
  bindQuizActions(context);
  renderLevelHeader(context);
  show(page.loading, false); show(page.quizScreen, true); renderQuizQuestion(context);
}

function bindQuizActions(context) {
  context.submitButton.addEventListener('click', () => submitQuizAnswer(context));
  context.nextButton.addEventListener('click', () => advanceQuiz(context));
}

function renderLevelHeader({ level }) {
  const thumb = document.getElementById('quiz-thumb');
  thumb.src = level.thumbnail || ''; thumb.alt = `${level.title || 'Video'} thumbnail`;
  setText('quiz-title', level.title || 'Untitled Level');
  setText('quiz-channel', `${level.channel || 'Unknown Channel'}${level.date ? ` · ${level.date}` : ''}`);
}

function renderQuizQuestion({ form, feedback, submitButton, nextButton, session }) {
  const { index, total, score, max } = session.progress();
  const question = session.current();
  feedback.innerHTML = ''; show(feedback, false); show(submitButton, true); show(nextButton, false);
  document.getElementById('progress-bar').style.width = `${((index + 1) / total) * 100}%`;
  setText('quiz-status', `${score}/${max} pts`); setText('question-counter', `Otázka ${index + 1} z ${total}`);
  setText('question-type', question.type === 'multi' ? 'multi-select' : 'single-select');
  setText('question-points', formatPoints(question.points)); setText('question-text', question.question || 'Bez textu otázky');
  const type = question.type === 'multi' ? 'checkbox' : 'radio';
  form.innerHTML = (question.options || []).map((option, index) => `<label class="answer-option" data-index="${index}"><input type="${type}" name="answer" value="${index}"><span>${escapeHtml(option)}</span></label>`).join('');
}

function submitQuizAnswer(context) {
  const { form, feedback, submitButton, nextButton, session } = context;
  const selected = Array.from(form.querySelectorAll('input:checked')).map((input) => Number(input.value));
  const answer = session.submit(selected);
  if (answer.message) {
    feedback.textContent = answer.message; feedback.className = 'feedback fail'; show(feedback, true); return;
  }
  form.querySelectorAll('.answer-option').forEach((option) => {
    const index = Number(option.dataset.index); const input = option.querySelector('input'); input.disabled = true;
    if (answer.correctIndexes.includes(index)) option.classList.add('correct');
    if (selected.includes(index) && !answer.correctIndexes.includes(index)) option.classList.add('incorrect');
  });
  const explanation = answer.explanation ? `<div class="feedback-explanation">${escapeHtml(answer.explanation)}</div>` : '';
  feedback.innerHTML = `${escapeHtml(answer.feedback)}${explanation}`;
  feedback.className = `feedback ${answer.correct ? 'success' : 'fail'}`;
  show(feedback, true); show(submitButton, false); show(nextButton, true);
}

function advanceQuiz(context) {
  const result = context.session.next();
  if (!result.complete) return renderQuizQuestion(context);
  renderQuizResults(context, result);
}

function renderQuizResults({ quizScreen, resultsScreen }, result) {
  show(quizScreen, false); show(resultsScreen, true); setText('quiz-status', 'Complete');
  setText('final-score', `${result.score} / ${result.max}`);
  setText('best-score', `Nejlepší skóre: ${result.best.best} / ${result.best.max}`);
  document.getElementById('results-list').innerHTML = result.results.map((item, index) => `<div class="result-row"><strong>${index + 1}. ${escapeHtml(item.question || 'Otázka')}</strong><span class="${item.correct ? 'score-chip' : 'chip'}">${item.earned}/${item.max}</span></div>`).join('');
}

if (typeof document !== 'undefined') {
  if (document.body.dataset.page === 'levels') {
    initLevelsPage();
  } else if (document.body.dataset.page === 'quiz') {
    initQuizPage();
  }
}

if (typeof module !== 'undefined') {
  module.exports = { sameSelection, levelUrl, initQuizPage };
}
